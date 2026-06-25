
#app_escuela.py  —  Backend Flask con conexión robusta a MySQL

import os
import logging
from flask import Flask, jsonify, render_template
import mysql.connector
from mysql.connector import pooling, errors

# ============================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[
        logging.StreamHandler(),                         # consola
        logging.FileHandler("escuela.log", encoding="utf-8")  # archivo
    ]
)
log = logging.getLogger("escuela")

# ============================================================
# LECTURA DE CREDENCIALES DESDE VARIABLES DE ENTORNO
# Crea un archivo .env en la misma carpeta con:
#   DB_HOST=localhost
#   DB_PORT=3306
#   DB_USER=root
#   DB_PASSWORD=Cruz1825258.
#   DB_NAME=Escuela_Primaria
# ============================================================
try:
    from dotenv import load_dotenv
    load_dotenv()
    log.info("Archivo .env cargado correctamente.")
except ImportError:
    log.warning("python-dotenv no instalado. Usando variables de entorno del sistema.")

DB_CONFIG = {
    "host":     os.getenv("DB_HOST",     "localhost"),
    "port":     int(os.getenv("DB_PORT", "3306")),
    "user":     os.getenv("DB_USER",     "root"),
    "password": os.getenv("DB_PASSWORD", "Cruz1825258."),
    "database": os.getenv("DB_NAME",     "buwyia053asdepnw2mwk"),
    "charset":  "utf8mb4",
    "use_unicode": True,
    "connection_timeout": 10,
}

# ============================================================
# POOL DE CONEXIONES 
# ============================================================
def crear_pool():
    """Crea o recrea el pool de conexiones."""
    try:
        pool = pooling.MySQLConnectionPool(
            pool_name="escuela_pool",
            pool_size=2,
            pool_reset_session=True,   # limpia cursores/transacciones al devolver al pool
            **DB_CONFIG
        )
        log.info("Pool MySQL creado con 2 conexiones. Host: %s:%s — BD: %s",
                 DB_CONFIG["host"], DB_CONFIG["port"], DB_CONFIG["database"])
        return pool
    except errors.Error as e:
        log.critical("No se pudo crear el pool MySQL: %s", e)
        raise

pool_conexiones = crear_pool()


def obtener_conexion():
    """
    Extrae una conexión del pool con reconexión automática.
    Si el pool está agotado o MySQL reinició, lo recrea.
    """
    global pool_conexiones
    try:
        conexion = pool_conexiones.get_connection()
        # Verificar que la conexión siga viva (envía un ping liviano)
        conexion.ping(reconnect=True, attempts=3, delay=1)
        return conexion
    except errors.PoolError:
        log.warning("Pool agotado — recreando pool.")
        pool_conexiones = crear_pool()
        return pool_conexiones.get_connection()
    except errors.Error as e:
        log.error("Error al obtener conexión del pool: %s", e)
        raise


# ============================================================
# APLICACIÓN FLASK
# ============================================================
app = Flask(__name__)


# ---- Utilidad: ejecutar query y devolver filas como dicts ----
def ejecutar_query(query: str, params: tuple = None) -> list:
    """
    Abre una conexión del pool, ejecuta la query y la devuelve al pool.
    params debe ser una tupla para queries parametrizadas (evita SQL injection).
    """
    conexion = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(query, params or ())
        resultados = cursor.fetchall()
        cursor.close()
        return resultados
    except errors.Error as e:
        log.error("Error en query → %s | params=%s | error=%s", query[:80], params, e)
        raise
    finally:
        if conexion and conexion.is_connected():
            conexion.close()   # devuelve al pool, no cierra realmente


# ============================================================
# RUTA PRINCIPAL
# ============================================================
@app.route("/")
def inicio():
    return render_template("index.html")


# ============================================================
# ENDPOINT DE SALUD — útil para monitoreo o Docker healthcheck
# ============================================================
@app.route("/api/health")
def health():
    try:
        ejecutar_query("SELECT 1")
        return jsonify({"estado": "OK", "base_datos": DB_CONFIG["database"]}), 200
    except Exception as e:
        return jsonify({"estado": "ERROR", "detalle": str(e)}), 503


# ============================================================
# ENDPOINTS EXISTENTES
# ============================================================
@app.route("/api/cursos")
def obtener_cursos():
    try:
        rows = ejecutar_query(
            "SELECT ID_Curso AS id, CONCAT(Nivel, ' ', Letra) AS nombre_curso "
            "FROM Curso ORDER BY Nivel, Letra;"
        )
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/estudiantes")
@app.route("/api/estudiantes/<int:id_curso>")
def obtener_estudiantes(id_curso=None):
    try:
        base = """
            SELECT e.CI_Estudiante AS ci, e.Nombre_Completo AS nombre,
                   CONCAT(c.Nivel, ' ', c.Letra) AS curso,
                   COALESCE(e.Celular, 'S/N') AS celular
            FROM Estudiante e
            INNER JOIN Curso c ON e.ID_Curso = c.ID_Curso
        """
        if id_curso:
            # Parámetro posicional — nunca interpolado directo (SQL injection corregido)
            rows = ejecutar_query(base + " WHERE e.ID_Curso = %s ORDER BY e.Nombre_Completo;", (id_curso,))
        else:
            rows = ejecutar_query(base + " ORDER BY e.Nombre_Completo;")
        return jsonify(rows), 200
    except Exception as e:
        log.error("Error en /api/estudiantes: %s", e)
        return jsonify({"error": str(e)}), 500


@app.route("/api/notas/<string:ci_estudiante>")
def obtener_notas(ci_estudiante):
    try:
        rows = ejecutar_query(
            """
            SELECT m.Nombre_Materia AS materia, n.Periodo AS trimestre,
                   n.Nota_Valor AS nota, n.Comentario AS comentario
            FROM Nota n
            INNER JOIN Materia m ON n.ID_Materia = m.ID_Materia
            WHERE n.CI_Estudiante = %s
            ORDER BY n.Periodo, m.Nombre_Materia;
            """,
            (ci_estudiante,)
        )
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/plantel-docente")
def obtener_plantel():
    try:
        rows = ejecutar_query(
            """
            SELECT p.Nombre_Completo AS profesor, m.Nombre_Materia AS materia,
                   CONCAT(c.Nivel, ' ', c.Letra) AS curso, h.Aula AS aula,
                   CASE
                       WHEN h.Dia_Semana IS NULL THEN 'Pendiente'
                       ELSE CONCAT(h.Dia_Semana, ' (',
                            TIME_FORMAT(h.Hora_Inicio, '%H:%i'), ' - ',
                            TIME_FORMAT(h.Hora_Fin,    '%H:%i'), ')')
                   END AS horario
            FROM Asignacion a
            INNER JOIN Profesor p  ON a.CI_Profesor = p.CI_Profesor
            INNER JOIN Materia m   ON a.ID_Materia  = m.ID_Materia
            INNER JOIN Curso c     ON a.ID_Curso    = c.ID_Curso
            LEFT  JOIN Horario h   ON a.ID_Asignacion = h.ID_Asignacion
            WHERE a.Gestion = 2026
            ORDER BY p.Nombre_Completo;
            """
        )
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# ENDPOINTS DE DASHBOARD
# ============================================================
@app.route("/api/dashboard/kpis")
def obtener_kpis():
    try:
        e = ejecutar_query("SELECT COUNT(*) AS total FROM Estudiante")[0]["total"]
        p = ejecutar_query("SELECT COUNT(*) AS total FROM Profesor")[0]["total"]
        c = ejecutar_query("SELECT COUNT(*) AS total FROM Curso")[0]["total"]
        return jsonify({"estudiantes": e, "profesores": p, "cursos": c}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500


@app.route("/api/dashboard/grafica")
def obtener_datos_grafica():
    try:
        rows = ejecutar_query(
            """
            SELECT CONCAT(c.Nivel, ' ', c.Letra) AS curso,
                   COUNT(e.CI_Estudiante) AS cantidad
            FROM Curso c
            LEFT JOIN Estudiante e ON c.ID_Curso = e.ID_Curso
            GROUP BY c.ID_Curso, c.Nivel, c.Letra
            ORDER BY c.Nivel, c.Letra;
            """
        )
        return jsonify(rows), 200
    except Exception as e:
        log.error("Error en /api/dashboard/grafica: %s", e)
        return jsonify({"error": str(e)}), 500


# ============================================================
# INICIO DEL SERVIDOR
# ============================================================
if __name__ == "__main__":
    # debug=False en producción; usa Gunicorn/Waitress para despliegue real
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)

