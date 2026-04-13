from flask import render_template, request, redirect, url_for
from datetime import datetime
import utils

def clean_float(val):
    if val is None or str(val).strip() in ['', 'None']:
        return 0.0
    try:
        return float(str(val).replace(',', '.'))
    except:
        return 0.0

def clean_int(val):
    if val is None or str(val).strip() in ['', 'None']:
        return 0
    try:
        return int(float(str(val).replace(' ', '')))
    except:
        return 0

def register_routes(app):
    @app.route('/inwestycje')
    def inwestycje_index():
        try:
            stats = utils.get_db_status(app.mysql)
            return render_template('index.html', s=stats, today=str(datetime.now().date()), tytul_aplikacji='Portfel Inwestycyjny')
        except Exception as e:
            return f"Błąd: {e}", 500

    # --- SEKCOJA: OBROTY ---
    @app.route('/inwestycje/obroty')
    @app.route('/inwestycje/obroty/<widok>')
    def obroty_list(widok='historia'):
        cur = app.mysql.connection.cursor()
        if widok == 'biezace':
            cur.execute("SELECT * FROM obroty WHERE sprzedaz_data IS NULL OR sprzedaz_data = '' ORDER BY ticker_nm ASC")
        else:
            cur.execute("SELECT * FROM obroty ORDER BY zakup_data DESC")
        
        rows = cur.fetchall()
        cur.close()
        # Przekazujemy 'obroty=rows', bo tak masz w obroty.html
        return render_template('obroty.html', obroty=rows, widok=widok)

    @app.route('/inwestycje/obroty/create', methods=['GET', 'POST'])
    def obroty_create():
        cur = app.mysql.connection.cursor()
        if request.method == 'POST':
            query = """INSERT INTO obroty (ticker_nm, zakup_data, zakup_cena, zakup_ilosc, platforma, uwagi) 
                       VALUES (%s, %s, %s, %s, %s, %s)"""
            cur.execute(query, (
                request.form.get('ticker_nm'), request.form.get('zakup_data'),
                clean_float(request.form.get('zakup_cena')), clean_int(request.form.get('zakup_ilosc')),
                request.form.get('platforma'), request.form.get('uwagi')
            ))
            app.mysql.connection.commit()
            cur.close()
            return redirect(url_for('obroty_list'))
        
        cur.execute("SELECT ticker_name FROM ticker ORDER BY ticker_name ASC")
        tickers = cur.fetchall()
        cur.execute("SELECT platforma_name FROM platforma ORDER BY platforma_name ASC")
        platforms = cur.fetchall()
        cur.close()
        return render_template('obroty_create.html', tickers=tickers, platforms=platforms)

    @app.route('/inwestycje/obroty/view/<int:id>')
    def obroty_view(id):
        cur = app.mysql.connection.cursor()
        cur.execute("SELECT * FROM obroty WHERE id_obroty = %s", (id,))
        row = cur.fetchone()
        cur.close()
        return render_template('obroty_view.html', row=row)

    @app.route('/inwestycje/obroty/edit/<int:id>', methods=['GET', 'POST'])
    def obroty_edit(id):
        cur = app.mysql.connection.cursor()
        if request.method == 'POST':
            s_data = request.form.get('sprzedaz_data')
            query = """UPDATE obroty SET ticker_nm=%s, zakup_data=%s, zakup_cena=%s, zakup_ilosc=%s, 
                       platforma=%s, uwagi=%s, sprzedaz_data=%s, sprzedaz_cena=%s WHERE id_obroty=%s"""
            cur.execute(query, (
                request.form.get('ticker_nm'), request.form.get('zakup_data'),
                clean_float(request.form.get('zakup_cena')), clean_int(request.form.get('zakup_ilosc')),
                request.form.get('platforma'), request.form.get('uwagi'),
                s_data if s_data else None,
                clean_float(request.form.get('sprzedaz_cena')), id
            ))
            app.mysql.connection.commit()
            cur.close()
            return redirect(url_for('obroty_list'))
        
        cur.execute("SELECT * FROM obroty WHERE id_obroty = %s", (id,))
        row = cur.fetchone()
        cur.execute("SELECT ticker_name FROM ticker ORDER BY ticker_name ASC")
        tickers = cur.fetchall()
        cur.execute("SELECT platforma_name FROM platforma ORDER BY platforma_name ASC")
        platforms = cur.fetchall()
        cur.close()
        return render_template('obroty_edit.html', row=row, tickers=tickers, platforms=platforms)

    @app.route('/inwestycje/obroty/delete/<int:id>')
    def obroty_delete(id):
        cur = app.mysql.connection.cursor()
        cur.execute("DELETE FROM obroty WHERE id_obroty = %s", (id,))
        app.mysql.connection.commit()
        cur.close()
        return redirect(url_for('obroty_list'))

    # --- POZOSTAŁE SEKCE (Ticker, Platforma, Dane) ---
    @app.route('/inwestycje/ticker')
    def ticker_list():
        cur = app.mysql.connection.cursor()
        cur.execute("SELECT * FROM ticker ORDER BY ticker_name ASC")
        rows = cur.fetchall()
        cur.close()
        return render_template('ticker.html', rows=rows)

    @app.route('/inwestycje/ticker/create', methods=['GET', 'POST'])
    def ticker_create():
        cur = app.mysql.connection.cursor()
        if request.method == 'POST':
            cur.execute("INSERT INTO ticker (ticker_name, market, rating, altman) VALUES (%s, %s, %s, %s)", 
                       (request.form.get('ticker_name'), request.form.get('market'), request.form.get('rating'), clean_float(request.form.get('altman'))))
            app.mysql.connection.commit()
            cur.close()
            return redirect(url_for('ticker_list'))
        cur.execute("SELECT platforma_name FROM platforma ORDER BY platforma_name ASC")
        platforms = cur.fetchall()
        cur.close()
        return render_template('ticker_create.html', platforms=platforms)

    @app.route('/inwestycje/platforma')
    def platforma_list():
        cur = app.mysql.connection.cursor()
        cur.execute("SELECT * FROM platforma ORDER BY platforma_name ASC")
        rows = cur.fetchall()
        cur.close()
        return render_template('platforma.html', rows=rows)

    @app.route('/inwestycje/dane_dzienne')
    def dane_dzienne_list():
        cur = app.mysql.connection.cursor()
        cur.execute("SELECT * FROM dane_dzienne ORDER BY data DESC LIMIT 100")
        rows = cur.fetchall()
        cur.close()
        return render_template('dane_dzienne.html', rows=rows)

    @app.route('/inwestycje/dane')
    def dane_list():
        cur = app.mysql.connection.cursor()
        cur.execute("SELECT * FROM dane ORDER BY data DESC LIMIT 100")
        rows = cur.fetchall()
        cur.close()
        return render_template('dane.html', rows=rows)

    @app.route('/inwestycje/get_csv_preview/<filename>')
    def get_csv_preview(filename):
        return utils.get_csv_preview_html(filename, limit=15)
