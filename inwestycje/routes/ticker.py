from flask import Blueprint, render_template, request, redirect, url_for, current_app

ticker_bp = Blueprint('ticker', __name__)

def clean_altman(val):
    if val is None:
        return None
    val = str(val).strip().replace(',', '.')
    # Jeśli wartość jest pusta lub jest dosłownym napisem "None" (z HTML)
    if val == '' or val.lower() == 'none':
        return None
    try:
        return float(val)
    except ValueError:
        return None

@ticker_bp.route('/inwestycje/ticker')
def list():
    cur = current_app.mysql.connection.cursor()
    cur.execute("SELECT * FROM ticker ORDER BY ticker_name ASC")
    rows = cur.fetchall()
    cur.close()
    return render_template('ticker.html', rows=rows)

@ticker_bp.route('/inwestycje/ticker/view/<int:id>')
def view(id):
    cur = current_app.mysql.connection.cursor()
    cur.execute("SELECT * FROM ticker WHERE id_ticker = %s", (id,))
    row = cur.fetchone()
    cur.close()
    return render_template('ticker_view.html', row=row) if row else ("Not Found", 404)

@ticker_bp.route('/inwestycje/ticker/create', methods=['GET', 'POST'])
def create():
    cur = current_app.mysql.connection.cursor()
    if request.method == 'POST':
        altman = clean_altman(request.form.get('altman'))
        cur.execute("INSERT INTO ticker (ticker_name, market, rating, altman) VALUES (%s, %s, %s, %s)",
                   (request.form.get('ticker_name'), request.form.get('market'), request.form.get('rating'), altman))
        current_app.mysql.connection.commit()
        cur.close()
        return redirect(url_for('ticker.list'))
    
    cur.execute("SELECT platforma_name FROM platforma ORDER BY platforma_name ASC")
    platforms = cur.fetchall()
    cur.close()
    return render_template('ticker_create.html', platforms=platforms)

@ticker_bp.route('/inwestycje/ticker/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cur = current_app.mysql.connection.cursor()
    if request.method == 'POST':
        altman = clean_altman(request.form.get('altman'))
        cur.execute("""
            UPDATE ticker 
            SET ticker_name=%s, market=%s, rating=%s, altman=%s 
            WHERE id_ticker=%s
        """, (request.form.get('ticker_name'), request.form.get('market'), 
              request.form.get('rating'), altman, id))
        current_app.mysql.connection.commit()
        cur.close()
        return redirect(url_for('ticker.list'))

    cur.execute("SELECT * FROM ticker WHERE id_ticker = %s", (id,))
    row = cur.fetchone()
    cur.execute("SELECT platforma_name FROM platforma ORDER BY platforma_name ASC")
    platforms = cur.fetchall()
    cur.close()
    return render_template('ticker_edit.html', row=row, platforms=platforms) if row else ("Not Found", 404)

@ticker_bp.route('/inwestycje/ticker/delete/<int:id>')
def delete(id):
    cur = current_app.mysql.connection.cursor()
    cur.execute("DELETE FROM ticker WHERE id_ticker = %s", (id,))
    current_app.mysql.connection.commit()
    cur.close()
    return redirect(url_for('ticker.list'))
