from flask import Flask,redirect,render_template
from models.db import init_app, mysql
from rutas.ordenes import ordenes_bp
from rutas.productores import productores_bp
from rutas.campos import campos_bp
from rutas.lotes import lotes_bp


app = Flask(__name__)
init_app(app)
app.secret_key = 'clave_secreta'

app.register_blueprint(ordenes_bp)
app.register_blueprint(productores_bp)
app.register_blueprint(campos_bp)
app.register_blueprint(lotes_bp)


@app.route('/')
def inicio():
    return render_template('inicio.html')


if __name__ == '__main__':
    app.run(debug=True)


