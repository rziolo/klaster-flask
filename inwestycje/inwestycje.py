from flask import render_template, request, redirect, url_for
from datetime import datetime
import utils  # Importujemy zaktualizowany utils.py

def register_routes(app):
    @app.route('/inwestycje')
    def inwestycje_index():
        try:
            stats = utils.get_db_status(app.mysql)
            return render_template('index.html', 
                                 s=stats, 
                                 today=str(datetime.now().date()),
                                 tytul_aplikacji='Portfel Inwestycyjny')
        except Exception as e:
            return f"Błąd modułu inwestycji: {e}", 500

    @app.route('/inwestycje/obroty')
    def obroty_list():
        cur = app.mysql.connection.cursor()
        cur.execute("SELECT * FROM obroty ORDER BY zakup_data DESC")
        rows = cur.fetchall()
        cur.close()
        return render_template('obroty.html', rows=rows)

    @app.route('/inwestycje/ticker')
    def ticker_list():
        cur = app.mysql.connection.cursor()
        cur.execute("SELECT * FROM ticker ORDER BY ticker_name ASC")
        rows = cur.fetchall()
        cur.close()
        return render_template('ticker.html', rows=rows)

    @app.route('/inwestycje/dane')
    def dane_list():
        cur = app.mysql.connection.cursor()
        cur.execute("SELECT * FROM dane ORDER BY data DESC LIMIT 100")
        rows = cur.fetchall()
        cur.close()
        return render_template('dane.html', rows=rows)

    @app.route('/inwestycje/dane_dzienne')
    def dane_dzienne_list():
        cur = app.mysql.connection.cursor()
        cur.execute("SELECT * FROM dane_dzienne ORDER BY data DESC LIMIT 100")
        rows = cur.fetchall()
        cur.close()
        return render_template('dane_dzienne.html', rows=rows)

    @app.route('/inwestycje/platforma')
    def platforma_list():
        cur = app.mysql.connection.cursor()
        cur.execute("SELECT * FROM platforma")
        rows = cur.fetchall()
        cur.close()
        return render_template('platforma.html', rows=rows)

    @app.route('/inwestycje/get_csv_preview/<filename>')
    def get_csv_preview(filename):
        # Wywołujemy faktyczną funkcję podglądu z utils.py
        # Ograniczamy podgląd do pierwszych 15 wierszy
        return utils.get_csv_preview_html(filename, limit=15)
