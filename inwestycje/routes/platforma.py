from flask import Blueprint, render_template, request, redirect, url_for, current_app

platforma_bp = Blueprint('platforma', __name__)

@platforma_bp.route('/inwestycje/platforma')
def list():
    cur = current_app.mysql.connection.cursor()
    cur.execute("SELECT * FROM platforma ORDER BY platforma_name ASC")
    rows = cur.fetchall()
    cur.close()
    return render_template('platforma.html', rows=rows)

@platforma_bp.route('/inwestycje/platforma/view/<int:id>')
def view(id):
    cur = current_app.mysql.connection.cursor()
    cur.execute("SELECT * FROM platforma WHERE id_platforma = %s", (id,))
    row = cur.fetchone()
    cur.close()
    return render_template('platforma_view.html', row=row) if row else ("Not Found", 404)

@platforma_bp.route('/inwestycje/platforma/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form.get('platforma_name')
        url = request.form.get('url')
        cur = current_app.mysql.connection.cursor()
        cur.execute("INSERT INTO platforma (platforma_name, url) VALUES (%s, %s)", (name, url))
        current_app.mysql.connection.commit()
        cur.close()
        return redirect(url_for('platforma.list'))
    return render_template('platforma_create.html')

@platforma_bp.route('/inwestycje/platforma/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cur = current_app.mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form.get('platforma_name')
        url = request.form.get('url')
        cur.execute("UPDATE platforma SET platforma_name=%s, url=%s WHERE id_platforma=%s", (name, url, id))
        current_app.mysql.connection.commit()
        cur.close()
        return redirect(url_for('platforma.list'))
    
    cur.execute("SELECT * FROM platforma WHERE id_platforma = %s", (id,))
    row = cur.fetchone()
    cur.close()
    return render_template('platforma_edit.html', row=row) if row else ("Not Found", 404)

@platforma_bp.route('/inwestycje/platforma/delete/<int:id>')
def delete(id):
    cur = current_app.mysql.connection.cursor()
    cur.execute("DELETE FROM platforma WHERE id_platforma = %s", (id,))
    current_app.mysql.connection.commit()
    cur.close()
    return redirect(url_for('platforma.list'))
