import pymysql
import sys
import os
from tabulate import tabulate

config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': 'Cruz1825258.',              
    'port': 3306,
    'db': 'escuela_primaria'
}

miConexion = None
# Guarda el reporte en tu escritorio
RUTA_LOG = os.path.join(os.path.expanduser("~"), "Desktop", "salida_visual.txt")

# ======================
# SISTEMA ESPEJO
# ======================
class DobleSalida(object):
    def __init__(self):
        self.terminal = sys.__stdout__
        self.log = open(RUTA_LOG, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()

    def flush(self):
        self.terminal.flush()
        self.log.flush()

# Arrancamos el espejo automático
sys.stdout = DobleSalida()

def conectar():
    global miConexion
    if miConexion is None or not miConexion.open:
        miConexion = pymysql.connect(**config)
        print("🚀 Conexión abierta.")

def cerrar():
    global miConexion
    if miConexion and miConexion.open:
        miConexion.close()
        print("🔒 Conexión cerrada.")
        if isinstance(sys.stdout, DobleSalida):
            sys.stdout.log.close()


# =====================================================================
# TUS FUNCIONES PARA CONSULTAS Y ACCIONES EN LA BASE DE DATOS 
# =====================================================================

def consultar_tabla(sql, valores=None):
    """Ejecuta cualquier comando SQL """
    try:
        with miConexion.cursor() as cur:
            cur.execute(sql, valores)
            datos = cur.fetchall()
            
            if not datos:
                print("ℹ️ No se encontraron registros o el comando se ejecutó sin retornar datos.")
                return

            sql_upper = sql.strip().upper()

            # Mapeo manual ultra-seguro para los comandos especiales
            if sql_upper.startswith("DESCRIBE"):
                columnas = ["Field", "Type", "Null", "Key", "Default", "Extra"]
            elif sql_upper.startswith("SHOW TABLES"):
                columnas = [f"Tables_in_{config['db']}"]
            else:
                # Para cualquier SELECT, extrae el string de la posición 0 limpiando el (253, None, False)
                columnas = [col for col in cur.description]
            
            # Imprime la estructura psql completamente limpia
            print(tabulate(datos, headers=columnas, tablefmt="psql"))
    except Exception as e:
        print(f"❌ Error en consulta: {e}")

def ejecutar_accion(sql, valores=None):
    """Para INSERT, UPDATE, DELETE con transacciones seguras"""
    try:
        with miConexion.cursor() as cur:
            cur.execute(sql, valores)
            miConexion.commit()
            print("💾 Cambios guardados (Commit).")
    except Exception as e:
        print(f"❌ Error de Integridad: {e}")
        miConexion.rollback()


# =========================
# INTERFAZ DEL FRONTEND 
# =========================

def menu_frontend():
    conectar()
    print(f"📋 Salida en paralelo activa en: {RUTA_LOG}\n")
    
    while True:
        print("\n======================================")
        print("     🖥️  FRONTEND INTERACTIVO")
        print("========================================")
        print(" 1. Consulta General (SELECT * FROM estudiante)")
        print(" 2. Funciones Dinámicas (SHOW TABLES / DESCRIBE)")
        print(" 3. Prueba de Filtros Específicos (WHERE)")
        print(" 4. Manejo de Campos Vacíos o NULL")
        print(" 5. Probar Integridad del Sistema (INSERT)")
        print(" 6. Salir")
        print("==========================================")
        
        opcion = input("Seleccione el punto de la guía a evaluar: ").strip()

        if opcion == "1":
            print("\n📋 CONSULTA GENERAL DE LA TABLA:")
            consultar_tabla("SELECT * FROM estudiante;")

        elif opcion == "2":
            print("\n🔄 FUNCIONES DINÁMICAS DEL SISTEMA:")
            print("\n-> Tablas en la base de datos:")
            consultar_tabla("SHOW TABLES;")
            print("\n-> Estructura dinámica de campos en 'estudiante':")
            consultar_tabla("DESCRIBE estudiante;")

        elif opcion == "3":
            print("\n🔍 PRUEBA DE FILTROS ESPECÍFICOS:")
            print("Campos válidos: CI_Estudiante, Nombre_Completo, ID_Curso")
            columna = input("Nombre exacto de la columna para filtrar: ").strip()
            valor = input(f"Ingrese el valor a buscar para '{columna}': ").strip()
            
            if columna not in ['CI_Estudiante', 'Nombre_Completo', 'ID_Curso']:
                print("❌ Campo no permitido por seguridad.")
                continue
                
            query = f"SELECT * FROM estudiante WHERE {columna} = %s;"
            consultar_tabla(query, (valor,))

        elif opcion == "4":
            print("\n🛑 MANEJO DE CAMPOS VACÍOS O NULL:")
            query = """SELECT CI_Estudiante, Nombre_Completo, Direccion, ID_Curso 
                       FROM estudiante 
                       WHERE Direccion IS NULL OR Telefono IS NULL OR Celular IS NULL OR ID_Curso IS NULL;"""
            consultar_tabla(query)

        elif opcion == "5":
            print("\n🛡️  PRUEBA DE INTEGRIDAD DEL SISTEMA:")
            ci = input("CI del estudiante (Obligatorio): ").strip()
            nombre = input("Nombre Completo (Obligatorio): ").strip()
            fecha_nac = input("Fecha de Nacimiento (AAAA-MM-DD - Obligatorio): ").strip()
            id_curso = input("ID Curso (Presione ENTER para enviar NULL): ").strip()
            
            id_curso_val = None if id_curso == "" else int(id_curso)
            
            query = "INSERT INTO estudiante (CI_Estudiante, Nombre_Completo, Fecha_Nacimiento, ID_Curso) VALUES (%s, %s, %s, %s);"
            ejecutar_accion(query, (ci, nombre, fecha_nac, id_curso_val))

        elif opcion == "6":
            print("👋 ¡Consulta finalizada con éxito!")
            cerrar()
            open(RUTA_LOG, "w", encoding="utf-8").close()
            break
        else:
            print("⚠️ Opción inválida.")

if __name__ == "__main__":
    menu_frontend()