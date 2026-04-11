import os
import sys
import requests
from datetime import datetime
from pytz import timezone
from flask import Flask, render_template, request, redirect, url_for

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FLASK_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))
sys.path.insert(0, FLASK_ROOT)

from app import create_app
app = create_app()

from jinja2 import ChoiceLoader, FileSystemLoader
app.jinja_loader = ChoiceLoader([
    FileSystemLoader(os.path.join(BASE_DIR, 'templates')),
    FileSystemLoader(os.path.join(FLASK_ROOT, 'shared', 'templates')),
])

@app.route('/')
@app.route('/zdrowie')
def index():
    return render_template('index.html', tytul_aplikacji='Moje Zdrowie')

@app.route('/zdrowie/pressure_list')
def pressure_list():
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

@app.route('/zdrowie/pressure/create', methods=['GET', 'POST'])
def pressure_create():
    HOME_ASSISTANT_URL = "https://rziolo.duckdns.org:8123/api/states/sensor.s23_geocoded_location"
    HA_TOKEN = os.getenv("HA_TOKEN")
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    locality = "Police"
    weather = {"pressure": 1013, "temp": 20, "humidity": 50}
    try:
        ha_response = requests.get(HOME_ASSISTANT_URL, headers={"Authorization": f"Bearer {HA_TOKEN}"}, verify=False, timeout=5)
        if ha_response.status_code == 200:
            attr = ha_response.json().get('attributes', {})
            locality = attr.get('locality') or attr.get('city') or "Police"
    except: pass
    try:
        w_res = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={locality}&appid={OPENWEATHER_API_KEY}&units=metric", timeout=5)
        if w_res.status_code == 200:
            wd = w_res.json()
            weather = {"pressure": wd['main']['pressure'], "temp": round(wd['main']['temp']), "humidity": wd['main']['humidity']}
    except: pass
    warsaw_tz = timezone('Europe/Warsaw')
    current_time = datetime.now(warsaw_tz).strftime('%Y-%m-%dT%H:%M')

    if request.method == 'POST':
        try:
            cur = app.mysql.connection.cursor()
            query = """INSERT INTO ha_vita_pressure 
                       (Date, `atmosf.`, P_skurczowe, P_rozkurczowe, Puls, temperatura, wilgotnosc, waga, miasto, uwagi) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cur.execute(query, (request.form.get('Date'), request.form.get('atmosf'), request.form.get('P_skurczowe'), 
                                request.form.get('P_rozkurczowe'), request.form.get('Puls'), request.form.get('temperatura'), 
                                request.form.get('wilgotnosc'), request.form.get('waga').replace(',', '.'), 
                                request.form.get('miasto'), request.form.get('uwagi')))
            app.mysql.connection.commit()
            cur.close()
            return redirect(url_for('pressure_list'))
        except Exception as e: return f"Błąd: {e}", 500
    return render_template('pressure_create.html', locality=locality, weather=weather, current_time=current_time)

@app.route('/zdrowie/pressure/update/<int:id>', methods=['GET', 'POST'])
def pressure_update(id):
    cur = app.mysql.connection.cursor()
    if request.method == 'POST':
        query = """UPDATE ha_vita_pressure SET Date=%s, `atmosf.`=%s, P_skurczowe=%s, P_rozkurczowe=%s, Puls=%s, 
                   temperatura=%s, wilgotnosc=%s, waga=%s, miasto=%s, uwagi=%s WHERE id_ha_fit=%s"""
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

@app.route('/zdrowie/pressure/read/<int:id>')
def pressure_read(id):
    cur = app.mysql.connection.cursor()
    cur.execute("SELECT * FROM ha_vita_pressure WHERE id_ha_fit = %s", [id])
    row = cur.fetchone()
    cur.close()
    return render_template('pressure_read.html', row=row)

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
    # Pobieramy dane do druku
    cur.execute("SELECT * FROM ha_vita_pressure ORDER BY Date DESC")
    rows = cur.fetchall()
    cur.close()

    for row in rows:
        # Formatowanie daty i wagi pod wydruk
        if row.get('Date'):
            row['f_date'] = row['Date'].strftime('%Y-%m-%d')
            row['f_time'] = row['Date'].strftime('%H:%M')
        
        waga_val = row.get('waga')
        try:
            row['waga_pl'] = f"{float(waga_val):.1f}".replace('.', ',') if waga_val else "---"
        except:
            row['waga_pl'] = "---"

    return render_template('pressure_print.html', rows=rows, now=datetime.now())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
