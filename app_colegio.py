from flask import Flask, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Función de conexión a tu base de datos MySQL
def conectar_base_datos():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="Cruz1825258.",  
        database="Escuela_Primaria"
    )

# ==========================================
# NUEVA RUTA WEB: Sirve para mostrar el HTML
# ==========================================
@app.route('/')
def inicio():
    return render_template('index.html')


# ==========================================
# TU API REST: Jala los datos de MySQL
# ==========================================
@app.route('/api/estudiantes', methods=['GET'])
def obtener_estudiantes():
    try:
        conexion = conectar_base_datos()
        cursor = conexion.cursor(dictionary=True)
        
        # Tu consulta SQL exacta
        query = """
            SELECT e.CI_Estudiante AS ci, e.Nombre_Completo AS nombre, 
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
        return jsonify({"error": f"Fallo interno en MySQL: {err}"}), 500

if __name__ == '__main__':
    # Iniciamos el servidor local en el puerto 5000
    app.run(debug=True, port=5000)