from flask import Blueprint, render_template, request, redirect
from models.db import mysql

lotes_bp = Blueprint('lotes', __name__)

@lotes_bp.route('/lotes', methods=['GET', 'POST'])
def gestionar_lotes():
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        campo_id = request.form['campo_id']
        nombre = request.form['nombre']
        superficie = request.form['superficie']
        cursor.execute("INSERT INTO lotes (campo_id, nombre, superficie) VALUES (%s, %s, %s)",
                       (campo_id, nombre, superficie))
        mysql.connection.commit()

    # Cargar campos con nombre y productor
    cursor.execute("""
        SELECT c.id, c.nombre, p.nombre
        FROM campos c JOIN productores p ON c.productor_id = p.id
    """)
    campos = cursor.fetchall()

    # Cargar lotes existentes
    cursor.execute("""
        SELECT l.nombre, l.superficie, c.nombre, p.nombre
        FROM lotes l
        JOIN campos c ON l.campo_id = c.id
        JOIN productores p ON c.productor_id = p.id
    """)
    lotes = cursor.fetchall()

    return render_template('lotes.html', campos=campos, lotes=lotes)


@lotes_bp.route('/lotes/nuevo', methods=['GET', 'POST'])
def nuevo_lote():
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        campo_id = request.form['campo_id']
        nombre = request.form['nombre']
        superficie = request.form['superficie']
        cursor.execute("INSERT INTO lotes (campo_id, nombre, superficie) VALUES (%s, %s, %s)",
                       (campo_id, nombre, superficie))
        mysql.connection.commit()
        return redirect('/lotes/nuevo')

    # Cargar campos existentes
    cursor.execute("""
        SELECT c.id, c.nombre, p.nombre
        FROM campos c JOIN productores p ON c.productor_id = p.id
    """)
    campos = cursor.fetchall()

    return render_template('nuevo_lote.html', campos=campos)

