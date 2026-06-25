"""
test_conexion_clevercloud.py
-----------------------------
Prueba AISLADA de conexión a MySQL (Clever Cloud), sin Flask ni pool.
Objetivo: confirmar si el problema es de credenciales/red, o de la app.

Uso:
    pip install mysql-connector-python python-dotenv --break-system-packages
    python test_conexion_clevercloud.py
"""

import os
import sys
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errors

load_dotenv()  # lee el archivo .env de la carpeta actual

cfg = {
    "host":     os.getenv("DB_HOST"),
    "port":     int(os.getenv("DB_PORT", "3306")),
    "user":     os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "connection_timeout": 10,
}

print("Intentando conectar con:")
print(f"  host     = {cfg['host']}")
print(f"  port     = {cfg['port']}")
print(f"  user     = {cfg['user']}")
print(f"  password = {'*' * len(cfg['password']) if cfg['password'] else '(VACÍA)'}  (largo: {len(cfg['password']) if cfg['password'] else 0})")
print(f"  database = {cfg['database']}")
print("-" * 50)

if not all([cfg["host"], cfg["user"], cfg["password"], cfg["database"]]):
    print("❌ Falta una o más variables en el .env (host/user/password/database vacíos).")
    sys.exit(1)

try:
    conn = mysql.connector.connect(**cfg)
    print("✅ CONEXIÓN EXITOSA.")
    cur = conn.cursor()
    cur.execute("SHOW TABLES;")
    tablas = [t[0] for t in cur.fetchall()]
    print(f"Tablas encontradas en la base ({len(tablas)}): {tablas}")
    if not tablas:
        print("⚠️  La base de datos está VACÍA. Falta importar el esquema (Curso, Estudiante, etc.).")
    cur.close()
    conn.close()

except errors.ProgrammingError as e:
    if e.errno == 1045:
        print("❌ ERROR 1045 — ACCESO DENEGADO: usuario o contraseña incorrectos.")
        print("   -> Vuelve a copiar el usuario y la contraseña EXACTOS desde el panel de")
        print("      Clever Cloud (pestaña 'Environment variables' del add-on MySQL).")
        print("      No los reescribas a mano: copia y pega para evitar errores de tipeo.")
    elif e.errno == 1049:
        print("❌ ERROR 1049 — La base de datos indicada no existe en ese servidor.")
        print("   -> Revisa el valor de DB_NAME contra el panel de Clever Cloud.")
    else:
        print(f"❌ ERROR {e.errno}: {e}")

except errors.InterfaceError as e:
    print(f"❌ ERROR DE RED/CONEXIÓN: {e}")
    print("   -> Revisa DB_HOST y DB_PORT, y tu conexión a internet.")

except Exception as e:
    print(f"❌ ERROR INESPERADO: {type(e).__name__}: {e}")
