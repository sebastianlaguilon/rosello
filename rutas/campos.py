from flask import Blueprint, render_template, request, redirect
from models.db import mysql

campos_bp = Blueprint('campos', __name__)

@campos_bp.route('/campos', methods=['GET', 'POST'])
def gestionar_campos():
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        productor_id = request.form['productor_id']
        campo = request.form['campo']
        localidad = request.form['localidad']
        cursor.execute("INSERT INTO campos (productor_id, nombre, localidad) VALUES (%s, %s, %s)",
                       (productor_id, campo, localidad))
        mysql.connection.commit()

    cursor.execute("SELECT id, nombre FROM productores")
    productores = cursor.fetchall()

    cursor.execute("""
        SELECT c.id, c.nombre, c.localidad, p.nombre
        FROM campos c JOIN productores p ON c.productor_id = p.id
    """)
    campos = cursor.fetchall()

    return render_template('campos.html', productores=productores, campos=campos)
