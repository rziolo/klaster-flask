import os
import requests
from flask import render_template, request, redirect, url_for
from datetime import datetime
from pytz import timezone

def register_routes(app):
    @app.route('/zdrowie')
    def zdrowie_index():
        return render_template('index.html', tytul_aplikacji='Moje Zdrowie')

    @app.route('/zdrowie/pressure_list')
    def pressure_list():
        try:
            cur = app.mysql.connection.cursor()
            cur.execute("SELECT * FROM ha_vita_pressure ORDER BY Date DESC")
            rows = cur.fetchall()
            cur.close()
            for row in rows:
                if row.get('Date'):
                    row['tylko_data'] = row['Date'].strftime('%Y-%m-%d')
                    row['tylko_godzina'] = row['Date'].strftime('%H:%M')
                row['sys'] = row.get('P_skurczowe')
                row['dia'] = row.get('P_rozkurczowe')
                row['puls_val'] = row.get('Puls')
                waga_val = row.get('waga')
                try:
                    row['waga_pl'] = f"{float(waga_val):.1f}".replace('.', ',') if waga_val else ""
                except:
                    row['waga_pl'] = waga_val
            return render_template('ha_vita_pressure.html', rows=rows)
        except Exception as e:
            return f"Błąd bazy danych (List): {e}", 500

    @app.route('/zdrowie/pressure/read/<int:id>')
    def pressure_read(id):
        try:
            cur = app.mysql.connection.cursor()
            cur.execute("SELECT * FROM ha_vita_pressure WHERE id_ha_fit = %s", [id])
            row = cur.fetchone()
            cur.close()
            return render_template('pressure_read.html', row=row)
        except Exception as e:
            return f"Błąd bazy danych (Read): {e}", 500

    @app.route('/zdrowie/pressure/create', methods=['GET', 'POST'])
    def pressure_create():
        HA_TOKEN = os.getenv("HA_TOKEN", "")
        OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
        locality = "Police"
        weather = {"pressure": 1013, "temp": 20, "humidity": 50}
        
        if request.method == 'POST':
            cur = app.mysql.connection.cursor()
            query = "INSERT INTO ha_vita_pressure (Date, `atmosf.`, P_skurczowe, P_rozkurczowe, Puls, temperatura, wilgotnosc, waga, miasto, uwagi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(query, (request.form.get('Date'), request.form.get('atmosf'), request.form.get('P_skurczowe'), 
                                request.form.get('P_rozkurczowe'), request.form.get('Puls'), request.form.get('temperatura'), 
                                request.form.get('wilgotnosc'), request.form.get('waga').replace(',', '.'), 
                                request.form.get('miasto'), request.form.get('uwagi')))
            app.mysql.connection.commit()
            cur.close()
            return redirect(url_for('pressure_list'))

        warsaw_tz = timezone('Europe/Warsaw')
        current_time = datetime.now(warsaw_tz).strftime('%Y-%m-%dT%H:%M')
        return render_template('pressure_create.html', locality=locality, weather=weather, current_time=current_time)

    @app.route('/zdrowie/pressure/update/<int:id>', methods=['GET', 'POST'])
    def pressure_update(id):
        cur = app.mysql.connection.cursor()
        if request.method == 'POST':
            query = "UPDATE ha_vita_pressure SET Date=%s, `atmosf.`=%s, P_skurczowe=%s, P_rozkurczowe=%s, Puls=%s, temperatura=%s, wilgotnosc=%s, waga=%s, miasto=%s, uwagi=%s WHERE id_ha_fit=%s"
            cur.execute(query, (request.form.get('Date'), request.form.get('atmosf'), request.form.get('P_skurczowe'), 
                                request.form.get('P_rozkurczowe'), request.form.get('Puls'), request.form.get('temperatura'), 
                                request.form.get('wilgotnosc'), request.form.get('waga').replace(',', '.'), 
                                request.form.get('miasto'), request.form.get('uwagi'), id))
            app.mysql.connection.commit()
            cur.close()
            return redirect(url_for('pressure_list'))
        
        cur.execute("SELECT * FROM ha_vita_pressure WHERE id_ha_fit = %s", [id])
        row = cur.fetchone()
        cur.close()
        if row and row['Date']: row['Date_iso'] = row['Date'].strftime('%Y-%m-%dT%H:%M')
        return render_template('pressure_update.html', row=row)

    @app.route('/zdrowie/pressure/delete/<int:id>')
    def pressure_delete(id):
        cur = app.mysql.connection.cursor()
        cur.execute("DELETE FROM ha_vita_pressure WHERE id_ha_fit = %s", [id])
        app.mysql.connection.commit()
        cur.close()
        return redirect(url_for('pressure_list'))

    @app.route('/zdrowie/pressure/print')
    def pressure_print():
        cur = app.mysql.connection.cursor()
        cur.execute("SELECT * FROM ha_vita_pressure ORDER BY Date DESC")
        rows = cur.fetchall()
        cur.close()
        for row in rows:
            if row.get('Date'):
                row['f_date'] = row['Date'].strftime('%Y-%m-%d')
                row['f_time'] = row['Date'].strftime('%H:%M')
            waga_val = row.get('waga')
            try:
                row['waga_pl'] = f"{float(waga_val):.1f}".replace('.', ',') if waga_val else "---"
            except:
                row['waga_pl'] = "---"
        return render_template('pressure_print.html', rows=rows, now=datetime.now())
