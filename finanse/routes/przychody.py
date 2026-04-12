from flask import render_template, request, redirect, url_for
from datetime import datetime
import MySQLdb.cursors

def register_routes(app):
    @app.route('/finanse/przychody')
    def przychody_list():
        cur = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM przychody ORDER BY data DESC")
        rows = cur.fetchall()
        cur.close()
        return render_template('przychody.html', rows=rows)

    @app.route('/finanse/przychody/create', methods=['GET', 'POST'])
    def przychody_create():
        if request.method == 'POST':
            cur = app.mysql.connection.cursor()
            query = """INSERT INTO przychody (data, ZUS_Iwona, ZUS_Robert, gielda, odsetki, urzad, inne, uwagi) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cur.execute(query, (
                request.form.get('data'), request.form.get('ZUS_Iwona'), request.form.get('ZUS_Robert'),
                request.form.get('gielda'), request.form.get('odsetki'), request.form.get('urzad'),
                request.form.get('inne'), request.form.get('uwagi')
            ))
            app.mysql.connection.commit()
            cur.close()
            return redirect(url_for('przychody_list'))
        return render_template('przychody_create.html', data_dzis=datetime.now().strftime('%Y-%m-%d'), edit_mode=False)

    @app.route('/finanse/przychody/view/<int:id>')
    def przychody_view(id):
        cur = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM przychody WHERE id_przychody = %s", [id])
        row = cur.fetchone()
        cur.close()
        return render_template('przychody_create.html', row=row, edit_mode=True, read_only=True)

    @app.route('/finanse/przychody/edit/<int:id>', methods=['GET', 'POST'])
    def przychody_edit(id):
        cur = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST':
            query = """UPDATE przychody SET data=%s, ZUS_Iwona=%s, ZUS_Robert=%s, gielda=%s, 
                       odsetki=%s, urzad=%s, inne=%s, uwagi=%s WHERE id_przychody=%s"""
            cur.execute(query, (
                request.form.get('data'), request.form.get('ZUS_Iwona'), request.form.get('ZUS_Robert'),
                request.form.get('gielda'), request.form.get('odsetki'), request.form.get('urzad'),
                request.form.get('inne'), request.form.get('uwagi'), id
            ))
            app.mysql.connection.commit()
            cur.close()
            return redirect(url_for('przychody_list'))
        
        cur.execute("SELECT * FROM przychody WHERE id_przychody = %s", [id])
        row = cur.fetchone()
        cur.close()
        return render_template('przychody_create.html', row=row, edit_mode=True, read_only=False)

    @app.route('/finanse/przychody/delete/<int:id>')
    def przychody_delete(id):
        cur = app.mysql.connection.cursor()
        cur.execute("DELETE FROM przychody WHERE id_przychody = %s", [id])
        app.mysql.connection.commit()
        cur.close()
        return redirect(url_for('przychody_list'))
