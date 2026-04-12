from flask import Blueprint, render_template, current_app
from decimal import Decimal
from datetime import datetime

car_bp = Blueprint('car', __name__)

def format_polish(value):
    if isinstance(value, (int, float, Decimal)):
        s = f"{value:,.2f}"
        return s.replace(',', 'XXX').replace('.', ',').replace('XXX', ' ')
    return value

def format_thousands(n):
    return '{:,}'.format(int(n)).replace(',', ' ') if n is not None else '0'

@car_bp.route('/')
def car_view():
    try:
        cur = car_bp.mysql.connection.cursor()
        cur.execute("SELECT data, car_cost, car_km FROM wydatki WHERE car_km > 0 ORDER BY data ASC")
        rows_raw = cur.fetchall()
        cur.close()

        result = []
        prev_km = None
        for row in rows_raw:
            curr_km = int(row['car_km'])
            cost = Decimal(str(row['car_cost'] or 0))
            przebieg = curr_km - prev_km if prev_km is not None else 0
            cost_per_km = (cost / Decimal(przebieg)) if przebieg > 0 else Decimal('0.00')

            result.append({
                'data': str(row['data'])[:7],
                'car_cost': format_polish(cost),
                'car_km': format_thousands(curr_km),
                'car_km_wczesniej': format_thousands(prev_km),
                'przebieg': format_thousands(przebieg),
                'cost_month': format_polish(cost_per_km)
            })
            prev_km = curr_km

        result.reverse()
        return render_template('car.html', rows=result)
    except Exception as e:
        print("Błąd car:", e)
        return render_template('car.html', rows=[])
