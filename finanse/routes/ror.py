from flask import render_template, request, redirect, url_for
from datetime import datetime
import MySQLdb.cursors
from shared.kursy_nbp import get_nbp_rates

def register_routes(app):
    @app.route('/finanse/ror')
    def ror_list():
        cur = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM ror ORDER BY data DESC")
        rows = cur.fetchall()
        cur.close()
        return render_template('ror.html', rows=rows)

    @app.route('/finanse/ror/create', methods=['GET', 'POST'])
    def ror_create():
        if request.method == 'POST':
            cur = app.mysql.connection.cursor()
            query = """INSERT INTO ror (data, PKO, mBank, Millenium, obligacje, fundusze, 
                       lokaty, gotowka, ike_ikze, gielda, EURO, EURO_kurs, USD, USD_kurs, uwagi) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cur.execute(query, (
                request.form.get('data'), request.form.get('PKO'), request.form.get('mBank'),
                request.form.get('Millenium'), request.form.get('obligacje'), request.form.get('fundusze'),
                request.form.get('lokaty'), request.form.get('gotowka'), request.form.get('ike_ikze'),
                request.form.get('gielda'), request.form.get('EURO'), request.form.get('EURO_kurs'),
                request.form.get('USD'), request.form.get('USD_kurs'), request.form.get('uwagi')
            ))
            app.mysql.connection.commit()
            cur.close()
            return redirect(url_for('ror_list'))
        
        kursy = get_nbp_rates()
        return render_template('ror_create.html', kursy=kursy, data_dzis=datetime.now().strftime('%Y-%m-%d'))

    # TRASA PODGLĄDU (TYLKO DO ODCZYTU)
    @app.route('/finanse/ror/view/<int:id>')
    def ror_view(id):
        cur = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM ror WHERE id_ror = %s", [id])
        row = cur.fetchone()
        cur.close()
        return render_template('ror_create.html', row=row, edit_mode=True, read_only=True)

    @app.route('/finanse/ror/edit/<int:id>', methods=['GET', 'POST'])
    def ror_edit(id):
        cur = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST':
            query = """UPDATE ror SET data=%s, PKO=%s, mBank=%s, Millenium=%s, obligacje=%s, 
                       fundusze=%s, lokaty=%s, gotowka=%s, ike_ikze=%s, gielda=%s, 
                       EURO=%s, EURO_kurs=%s, USD=%s, USD_kurs=%s, uwagi=%s WHERE id_ror=%s"""
            cur.execute(query, (
                request.form.get('data'), request.form.get('PKO'), request.form.get('mBank'),
                request.form.get('Millenium'), request.form.get('obligacje'), request.form.get('fundusze'),
                request.form.get('lokaty'), request.form.get('gotowka'), request.form.get('ike_ikze'),
                request.form.get('gielda'), request.form.get('EURO'), request.form.get('EURO_kurs'),
                request.form.get('USD'), request.form.get('USD_kurs'), request.form.get('uwagi'), id
            ))
            app.mysql.connection.commit()
            cur.close()
            return redirect(url_for('ror_list'))
        
        cur.execute("SELECT * FROM ror WHERE id_ror = %s", [id])
        row = cur.fetchone()
        cur.close()
        return render_template('ror_create.html', row=row, edit_mode=True, read_only=False)

    @app.route('/finanse/ror/delete/<int:id>')
    def ror_delete(id):
        cur = app.mysql.connection.cursor()
        cur.execute("DELETE FROM ror WHERE id_ror = %s", [id])
        app.mysql.connection.commit()
        cur.close()
        return redirect(url_for('ror_list'))
