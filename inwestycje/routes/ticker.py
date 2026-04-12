from flask import Blueprint, render_template, current_app, request, redirect, url_for

ticker_bp = Blueprint('ticker', __name__)

# --- READ ---
@ticker_bp.route('/ticker')
def ticker_index():
    try:
        mysql = current_app.mysql
        cur = mysql.connection.cursor()
        cur.execute("SELECT id_ticker, ticker_name, market, rating, altman FROM ticker ORDER BY ticker_name ASC")
        rows = cur.fetchall()
        cur.close()
        return render_template('ticker.html', rows=rows)
    except Exception as e:
        return f"Błąd (Ticker Index): {e}"

# --- CREATE ---
@ticker_bp.route('/ticker/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form.get('ticker_name')
        market = request.form.get('market')
        rating = request.form.get('rating')
        altman = request.form.get('altman').replace(',', '.') if request.form.get('altman') else None
        
        mysql = current_app.mysql
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO ticker (ticker_name, market, rating, altman) 
            VALUES (%s, %s, %s, %s)
        """, (name, market, rating, altman))
        mysql.connection.commit()
        cur.close()
        return redirect('/inwestycje/ticker')
    return render_template('ticker_create.html')

# --- EDIT ---
@ticker_bp.route('/ticker/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    mysql = current_app.mysql
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form.get('ticker_name')
        market = request.form.get('market')
        rating = request.form.get('rating')
        altman = request.form.get('altman').replace(',', '.') if request.form.get('altman') else None
        
        cur.execute("""
            UPDATE ticker SET ticker_name=%s, market=%s, rating=%s, altman=%s 
            WHERE id_ticker=%s
        """, (name, market, rating, altman, id))
        mysql.connection.commit()
        cur.close()
        return redirect('/inwestycje/ticker')
    
    cur.execute("SELECT * FROM ticker WHERE id_ticker = %s", (id,))
    row = cur.fetchone()
    cur.close()
    return render_template('ticker_edit.html', row=row)

# --- DELETE ---
@ticker_bp.route('/ticker/delete/<int:id>')
def delete(id):
    mysql = current_app.mysql
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM ticker WHERE id_ticker = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/inwestycje/ticker')
