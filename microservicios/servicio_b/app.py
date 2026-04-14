from flask import Flask, request, jsonify
import mysql.connector
import time
import os

app = Flask(__name__)

db_config = {
    'host': os.environ.get('DB_HOST'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'database': os.environ.get('DB_NAME')
}

@app.route('/auditar', methods=['POST'])
def auditar():
    data = request.get_json()
    consola = data.get('consola')
    
    # Tarea pesada simulación 
    time.sleep(7) 
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # Guarda en tabla diferente 
        cursor.execute("INSERT INTO auditoria_stock (nombre_consola, mensaje_log) VALUES (%s, %s)", 
                       (consola, "LOG_SEGURIDAD_GENERADO"))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error en B: {e}")

    return jsonify({"status": "auditoria_completada"}), 200 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=True) 
