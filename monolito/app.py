from flask import Flask, request, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# CONFIGURACIÓN (Cambia los datos con tu endpoint de AWS)
USER = 'admin'
PASS = 'admin123'
HOST = 'db-actividades.czbooez4f39o.us-east-1.rds.amazonaws.com'
DB = 'sistema_clase'

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USER}:{PASS}@{HOST}/{DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.String(255))
    longitud_logica = db.Column(db.Integer)

# INTERFAZ Y LÓGICA
HTML_TEMPLATE = '''
<h1>App Monolítica - Registro</h1>
<form method="POST">
    Nombre: <input type="text" name="nombre"><br>
    Descripción: <input type="text" name="desc"><br>
    <input type="submit" value="Enviar">
</form>
<hr>
<a href="/ver">Ver Base de Datos</a>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nom = request.form['nombre']
        desc = request.form['desc']
        # LÓGICA: Calcular longitud de la descripción
        resultado = len(desc) 
        
        # ACCESO A BD
        nuevo_reg = Registro(nombre=nom, descripcion=desc, longitud_logica=resultado)
        db.session.add(nuevo_reg)
        db.session.commit()
        return f"Dato guardado. Lógica aplicada: Longitud de descripción = {resultado}. <a href='/'>Volver</a>"
    return render_template_string(HTML_TEMPLATE)

@app.route('/ver')
def ver():
    registros = Registro.query.all()
    output = "<ul>"
    for r in registros:
        output += f"<li>{r.nombre} - {r.descripcion} (Log: {r.longitud_logica})</li>"
    return output + "</ul><br><a href='/'>Volver</a>"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, threaded=True)
