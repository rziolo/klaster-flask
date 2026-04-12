from flask import render_template, request, redirect, url_for
from datetime import datetime
import MySQLdb.cursors

def register_routes(app):
    @app.route('/finanse/wydatki')
    def wydatki_list():
        cur = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM wydatki ORDER BY data DESC")
        rows = cur.fetchall()
        cur.close()
        return render_template('wydatki.html', rows=rows)

    @app.route('/finanse/wydatki/create', methods=['GET', 'POST'])
    def wydatki_create():
        if request.method == 'POST':
            cur = app.mysql.connection.cursor()
            query = """INSERT INTO wydatki (data, zywnosc, niezywnosc, car_cost, car_km, oplaty, inne, medycyna, uwagi) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cur.execute(query, (
                request.form.get('data'), request.form.get('zywnosc'), request.form.get('niezywnosc'),
                request.form.get('car_cost'), request.form.get('car_km'), request.form.get('oplaty'),
                request.form.get('inne'), request.form.get('medycyna'), request.form.get('uwagi')
            ))
            app.mysql.connection.commit()
            cur.close()
            return redirect(url_for('wydatki_list'))
        return render_template('wydatki_create.html', data_dzis=datetime.now().strftime('%Y-%m-%d'), edit_mode=False)

    @app.route('/finanse/wydatki/view/<int:id>')
    def wydatki_view(id):
        cur = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM wydatki WHERE id_wydatki = %s", [id])
        row = cur.fetchone()
        cur.close()
        return render_template('wydatki_create.html', row=row, edit_mode=True, read_only=True)

    @app.route('/finanse/wydatki/edit/<int:id>', methods=['GET', 'POST'])
    def wydatki_edit(id):
        cur = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST':
            query = """UPDATE wydatki SET data=%s, zywnosc=%s, niezywnosc=%s, car_cost=%s, 
                       car_km=%s, oplaty=%s, inne=%s, medycyna=%s, uwagi=%s WHERE id_wydatki=%s"""
            cur.execute(query, (
                request.form.get('data'), request.form.get('zywnosc'), request.form.get('niezywnosc'),
                request.form.get('car_cost'), request.form.get('car_km'), request.form.get('oplaty'),
                request.form.get('inne'), request.form.get('medycyna'), request.form.get('uwagi'), id
            ))
            app.mysql.connection.commit()
            cur.close()
            return redirect(url_for('wydatki_list'))
        
        cur.execute("SELECT * FROM wydatki WHERE id_wydatki = %s", [id])
        row = cur.fetchone()
        cur.close()
        return render_template('wydatki_create.html', row=row, edit_mode=True, read_only=False)

    @app.route('/finanse/wydatki/delete/<int:id>')
    def wydatki_delete(id):
        cur = app.mysql.connection.cursor()
        cur.execute("DELETE FROM wydatki WHERE id_wydatki = %s", [id])
        app.mysql.connection.commit()
        cur.close()
        return redirect(url_for('wydatki_list'))
