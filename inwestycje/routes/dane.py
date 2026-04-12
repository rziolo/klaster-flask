from flask import Blueprint, render_template, current_app, request, redirect, url_for
import traceback

dane_bp = Blueprint('dane', __name__)

# --- READ ---
@dane_bp.route('/dane')
def dane_index():
    try:
        mysql = current_app.mysql
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT id_dane, data, ticker, ISIN, waluta, open, max, min, close, 
                   zmiana, volume, number_transactions, turnover 
            FROM dane 
            ORDER BY data DESC, ticker ASC 
            LIMIT 100
        """)
        rows = cur.fetchall()
        cur.close()
        return render_template('dane.html', rows=rows)
    except Exception as e:
        return f"Błąd (Dane Index): {e}"

# --- VIEW (OKO) ---
@dane_bp.route('/dane/view/<int:id>')
def view(id):
    mysql = current_app.mysql
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM dane WHERE id_dane = %s", (id,))
    row = cur.fetchone()
    cur.close()
    return render_template('dane_view.html', row=row)

# --- CREATE ---
@dane_bp.route('/dane/create', methods=['GET', 'POST'])
def create():
    mysql = current_app.mysql
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        d = request.form
        cur.execute("""
            INSERT INTO dane (data, ticker, ISIN, waluta, open, max, min, close, zmiana, volume, number_transactions, turnover)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            d.get('data'), d.get('ticker'), d.get('isin'), d.get('waluta'),
            d.get('open').replace(',', '.'), d.get('max').replace(',', '.'),
            d.get('min').replace(',', '.'), d.get('close').replace(',', '.'),
            d.get('zmiana').replace(',', '.'), d.get('volume'),
            d.get('number_transactions'), d.get('turnover').replace(',', '.')
        ))
        mysql.connection.commit()
        cur.close()
        return redirect('/inwestycje/dane')
    cur.execute("SELECT ticker_name FROM ticker ORDER BY ticker_name ASC")
    tickers = cur.fetchall()
    cur.close()
    return render_template('dane_create.html', tickers=tickers)

# --- EDIT (OŁÓWEK) ---
@dane_bp.route('/dane/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    mysql = current_app.mysql
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        d = request.form
        cur.execute("""
            UPDATE dane 
            SET data=%s, ticker=%s, ISIN=%s, waluta=%s, open=%s, max=%s, min=%s, 
                close=%s, zmiana=%s, volume=%s, number_transactions=%s, turnover=%s
            WHERE id_dane=%s
        """, (
            d.get('data'), d.get('ticker'), d.get('isin'), d.get('waluta'),
            d.get('open').replace(',', '.'), d.get('max').replace(',', '.'),
            d.get('min').replace(',', '.'), d.get('close').replace(',', '.'),
            d.get('zmiana').replace(',', '.'), d.get('volume'),
            d.get('number_transactions'), d.get('turnover').replace(',', '.'), id
        ))
        mysql.connection.commit()
        cur.close()
        return redirect('/inwestycje/dane')
    cur.execute("SELECT * FROM dane WHERE id_dane = %s", (id,))
    row = cur.fetchone()
    cur.execute("SELECT ticker_name FROM ticker ORDER BY ticker_name ASC")
    tickers = cur.fetchall()
    cur.close()
    return render_template('dane_edit.html', row=row, tickers=tickers)

# --- DELETE ---
@dane_bp.route('/dane/delete/<int:id>')
def delete(id):
    mysql = current_app.mysql
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM dane WHERE id_dane = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/inwestycje/dane')
