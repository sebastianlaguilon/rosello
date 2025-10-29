from flask import Blueprint, render_template, request, redirect
from models.db import mysql

ordenes_bp = Blueprint('ordenes', __name__)

@ordenes_bp.route('/nueva_orden', methods=['GET', 'POST'])
def nueva_orden():
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        productor_id = request.form['productor_id']
        lote_id = request.form['lote_id']
        fecha = request.form['fecha']
        hectareas = request.form['hectareas']

        cursor.execute("""
            INSERT INTO ordenes (productor_id, lote_id, fecha, hectareas_estimadas)
            VALUES (%s, %s, %s, %s)
        """, (productor_id, lote_id, fecha, hectareas))
        orden_id = cursor.lastrowid

        # Cargar productos aplicados
        productos = request.form.getlist('producto[]')
        unidades = request.form.getlist('unidad[]')
        dosis = request.form.getlist('cantidad[]')

        for i in range(len(productos)):
            cursor.execute("""
                INSERT INTO aplicaciones (orden_id, producto, unidad, cantidad_por_hectarea)
                VALUES (%s, %s, %s, %s)
            """, (orden_id, productos[i], unidades[i], dosis[i]))

        mysql.connection.commit()
        return redirect('/ordenes')

    # Cargar productores
    cursor.execute("SELECT id, nombre FROM productores")
    productores = cursor.fetchall()

    # Cargar campos y lotes
    cursor.execute("""
    SELECT l.id, l.nombre, c.nombre AS campo, p.id AS productor_id
    FROM lotes l
    JOIN campos c ON l.campo_id = c.id
    JOIN productores p ON c.productor_id = p.id
    """)
    lotes = cursor.fetchall()

    return render_template('nueva_orden.html', productores=productores, lotes=lotes)
