from flask import Blueprint, render_template, current_app, request, redirect, url_for, flash
import traceback

obroty_bp = Blueprint('obroty', __name__)

# --- READ (Wszystkie - Historia) ---
@obroty_bp.route('/obroty')
def obroty_index():
    try:
        mysql = current_app.mysql
        cur = mysql.connection.cursor()
        query = "SELECT id_obroty, ticker_nm, zakup_data, zakup_cena, zakup_ilosc, sprzedaz_data, sprzedaz_cena, platforma, uwagi FROM obroty ORDER BY zakup_data DESC LIMIT 100"
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return render_template('obroty.html', obroty=data, widok='historia')
    except Exception as e:
        return f"Błąd (Index): {e}"

# --- READ (Tylko otwarte - Bieżące) ---
@obroty_bp.route('/obroty/biezace')
def biezace():
    try:
        mysql = current_app.mysql
        cur = mysql.connection.cursor()
        # Filtr: Data sprzedaży is NULL, Sort: Ticker ASC
        query = "SELECT id_obroty, ticker_nm, zakup_data, zakup_cena, zakup_ilosc, sprzedaz_data, sprzedaz_cena, platforma, uwagi FROM obroty WHERE sprzedaz_data IS NULL ORDER BY ticker_nm ASC"
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return render_template('obroty.html', obroty=data, widok='biezace')
    except Exception as e:
        return f"Błąd (Bieżące): {e}"

# --- CREATE ---
@obroty_bp.route('/obroty/create', methods=['GET', 'POST'])
def create():
    mysql = current_app.mysql
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        ticker = request.form.get('ticker_nm')
        zakup_data = request.form.get('zakup_data')
        zakup_cena = request.form.get('zakup_cena').replace(',', '.')
        zakup_ilosc = request.form.get('zakup_ilosc')
        platforma = request.form.get('platforma')
        uwagi = request.form.get('uwagi')
        cur.execute("INSERT INTO obroty (ticker_nm, zakup_data, zakup_cena, zakup_ilosc, platforma, uwagi) VALUES (%s, %s, %s, %s, %s, %s)", (ticker, zakup_data, zakup_cena, zakup_ilosc, platforma, uwagi))
        mysql.connection.commit()
        cur.close()
        return redirect('/inwestycje/obroty')
    cur.execute("SELECT ticker_name FROM ticker ORDER BY ticker_name ASC")
    tickers = cur.fetchall()
    cur.close()
    return render_template('obroty_create.html', tickers=tickers)

# --- VIEW ---
@obroty_bp.route('/obroty/view/<int:id>')
def view(id):
    mysql = current_app.mysql
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM obroty WHERE id_obroty = %s", (id,))
    row = cur.fetchone()
    cur.close()
    return render_template('obroty_view.html', row=row)

# --- EDIT ---
@obroty_bp.route('/obroty/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    mysql = current_app.mysql
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        ticker = request.form.get('ticker_nm')
        zakup_data = request.form.get('zakup_data')
        zakup_cena = request.form.get('zakup_cena').replace(',', '.')
        zakup_ilosc = request.form.get('zakup_ilosc')
        sprzedaz_data = request.form.get('sprzedaz_data') or None
        sprzedaz_cena = request.form.get('sprzedaz_cena').replace(',', '.') if request.form.get('sprzedaz_cena') else None
        platforma = request.form.get('platforma')
        uwagi = request.form.get('uwagi')
        cur.execute("UPDATE obroty SET ticker_nm=%s, zakup_data=%s, zakup_cena=%s, zakup_ilosc=%s, sprzedaz_data=%s, sprzedaz_cena=%s, platforma=%s, uwagi=%s WHERE id_obroty=%s", (ticker, zakup_data, zakup_cena, zakup_ilosc, sprzedaz_data, sprzedaz_cena, platforma, uwagi, id))
        mysql.connection.commit()
        cur.close()
        return redirect('/inwestycje/obroty')
    cur.execute("SELECT * FROM obroty WHERE id_obroty = %s", (id,))
    row = cur.fetchone()
    cur.execute("SELECT ticker_name FROM ticker ORDER BY ticker_name ASC")
    tickers = cur.fetchall()
    cur.close()
    return render_template('obroty_edit.html', row=row, tickers=tickers)

# --- DELETE ---
@obroty_bp.route('/obroty/delete/<int:id>')
def delete(id):
    mysql = current_app.mysql
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM obroty WHERE id_obroty = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/inwestycje/obroty')
