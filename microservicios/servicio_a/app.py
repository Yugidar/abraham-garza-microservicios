from flask import Flask, request, jsonify, render_template_string
import mysql.connector
import requests
import os

app = Flask(__name__)

db_config = {
    'host': os.environ.get('DB_HOST'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'database': os.environ.get('DB_NAME')
}

HTML_FORM = """
<!DOCTYPE html><html><body>
<h2>Panel de Inventario Gaming</h2>
<form method="POST" action="/registrar">
    Consola/Videojuego: <input name="consola"><br><br>
    Cantidad: <input name="cantidad" type="number"><br><br>
    <input type="submit" value="Dar de Alta">
</form>
</body></html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_FORM)

@app.route('/registrar', methods=['POST'])
def registrar():
    consola = request.form.get('consola')
    cantidad = request.form.get('cantidad')
    if not consola or not cantidad:
        return jsonify({"error": "Faltan datos"}), 400
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (nombre_consola, stock_inicial) VALUES (%s, %s)", (consola, cantidad))
        conn.commit()
        conn.close()
        status_b = ""
        try:
            r = requests.post('http://servicio_b:5001/auditar', json={"consola": consola, "accion": "ALTA_INVENTARIO"}, timeout=5)
            status_b = "Notificación enviada al Servicio B"
        except Exception:
            status_b = "Servicio de auditoria en mantenimiento. Registro guardado."
        return jsonify({"mensaje": "Producto registrado en inventario.", "notificacion": status_b, "consola": consola}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
