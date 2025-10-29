from flask import Blueprint, render_template,request,redirect
from models.db import mysql

productores_bp = Blueprint('productores', __name__)

@productores_bp.route('/productores')
def listar_productores():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nombre, cuit, localidad FROM productores")
    productores = cursor.fetchall()
    return render_template('listar_productores.html', productores=productores)


@productores_bp.route('/productores/nuevo', methods=['GET', 'POST'])
def nuevo_productor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        localidad = request.form['localidad']
        cuit = request.form['cuit']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO productores (nombre, telefono, localidad, cuit) VALUES (%s, %s, %s, %s)",
                       (nombre, telefono, localidad, cuit))
        mysql.connection.commit()
        return redirect('/productores')
    return render_template('nuevo_productor.html')
