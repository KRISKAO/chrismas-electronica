from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

def conectar_base_datos():
    return mysql.connector.connect(
        host="localhost",          # O puedes usar "127.0.0.1"
        port=3306,                 # Especificamos el puerto explícitamente
        user="root",               # Tu usuario de MySQL
        password="Cruz182558.",  # ¡Aquí pon la contraseña real de tu MySQL!
        database="escuela_primaria"
    )

@app.route('/api/estudiantes', methods=['GET'])
def obtener_estudiantes():
    try:
        conexion = conectar_base_datos()
        cursor = conexion.cursor(dictionary=True) # Mapea las columnas directamente a formato JSON
        
        # Consulta adaptada a tus tablas 'Estudiante' y 'Curso'
        query = """
            SELECT 
                e.CI_Estudiante AS ci,
                e.Nombre_Completo AS nombre,
                CONCAT(c.Nivel, ' ', c.Letra) AS curso
            FROM Estudiante e
            INNER JOIN Curso c ON e.ID_Curso = c.ID_Curso;
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        cursor.close()
        conexion.close()
        
        return jsonify(resultados), 200

    except mysql.connector.Error as err:
        # Control de errores: Si la base de datos se detiene
        return jsonify({"error": f"Fallo interno en MySQL: {err}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)