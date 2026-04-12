from flask import Blueprint, render_template, current_app, request, redirect, url_for
import traceback

dane_dzienne_bp = Blueprint('dane_dzienne', __name__)

@dane_dzienne_bp.route('/dane_dzienne')
def dane_dzienne_index():
    try:
        mysql = current_app.mysql
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM dane_dzienne ORDER BY data DESC LIMIT 100")
        rows = cur.fetchall()
        cur.close()
        return render_template('dane_dzienne.html', rows=rows)
    except Exception as e:
        return f"Błąd Index: {e}"

@dane_dzienne_bp.route('/dane_dzienne/view/<int:id>')
def view(id):
    mysql = current_app.mysql
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM dane_dzienne WHERE id_dane_dzienne = %s", (id,))
    row = cur.fetchone()
    cur.close()
    return render_template('dane_dzienne_view.html', row=row)

@dane_dzienne_bp.route('/dane_dzienne/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        d = request.form
        mysql = current_app.mysql
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO dane_dzienne (data, wartosc, wklad, H_ilosc, H_vol, L_ilosc, L_vol, turnover, HL, NL)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (d.get('data'), d.get('wartosc').replace(',', '.'), d.get('wklad').replace(',', '.'),
              d.get('h_ilosc'), d.get('h_vol'), d.get('l_ilosc'), d.get('l_vol'),
              d.get('turnover'), d.get('hl'), d.get('nl')))
        mysql.connection.commit()
        cur.close()
        return redirect('/inwestycje/dane_dzienne')
    return render_template('dane_dzienne_create.html')

@dane_dzienne_bp.route('/dane_dzienne/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    mysql = current_app.mysql
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        d = request.form
        cur.execute("""
            UPDATE dane_dzienne 
            SET data=%s, wartosc=%s, wklad=%s, H_ilosc=%s, H_vol=%s, L_ilosc=%s, L_vol=%s, turnover=%s, HL=%s, NL=%s
            WHERE id_dane_dzienne=%s
        """, (d.get('data'), d.get('wartosc').replace(',', '.'), d.get('wklad').replace(',', '.'),
              d.get('h_ilosc'), d.get('h_vol'), d.get('l_ilosc'), d.get('l_vol'),
              d.get('turnover'), d.get('hl'), d.get('nl'), id))
        mysql.connection.commit()
        cur.close()
        return redirect('/inwestycje/dane_dzienne')
    
    cur.execute("SELECT * FROM dane_dzienne WHERE id_dane_dzienne = %s", (id,))
    row = cur.fetchone()
    cur.close()
    if not row: return "Nie znaleziono wpisu", 404
    return render_template('dane_dzienne_edit.html', row=row)

@dane_dzienne_bp.route('/dane_dzienne/delete/<int:id>')
def delete(id):
    mysql = current_app.mysql
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM dane_dzienne WHERE id_dane_dzienne = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/inwestycje/dane_dzienne')
