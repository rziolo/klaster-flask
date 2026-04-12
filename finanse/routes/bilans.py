from flask import render_template
from decimal import Decimal
from datetime import datetime

def register_routes(app):
    @app.route('/finanse/bilans')
    def bilans_view():
        try:
            # Używamy app.mysql zarejestrowanego w głównej aplikacji
            cur = app.mysql.connection.cursor()

            cur.execute("SELECT data, ZUS_Iwona, ZUS_Robert, gielda, odsetki, urzad, inne FROM przychody")
            przychody_rows = cur.fetchall()

            cur.execute("SELECT data, zywnosc, niezywnosc, car_cost, oplaty, medycyna, inne FROM wydatki")
            wydatki_rows = cur.fetchall()

            cur.execute("SELECT data, PKO, mBank, Millenium, obligacje, fundusze, lokaty, gotowka, ike_ikze, gielda, EURO, EURO_kurs, USD, USD_kurs FROM ror")
            rory_rows = cur.fetchall()
            cur.close()

            bilans_data = {}

            def format_polish(value):
                if isinstance(value, (int, float, Decimal)):
                    s = f"{value:,.2f}"
                    return s.replace(',', 'XXX').replace('.', ',').replace('XXX', ' ')
                return value

            for row in przychody_rows:
                ym = str(row['data'])[:7]
                suma = sum(Decimal(str(row[k] or 0)) for k in ['ZUS_Iwona', 'ZUS_Robert', 'gielda', 'odsetki', 'urzad', 'inne'])
                bilans_data.setdefault(ym, {})['przychody'] = bilans_data.get(ym, {}).get('przychody', Decimal('0.00')) + suma

            for row in wydatki_rows:
                ym = str(row['data'])[:7]
                suma = sum(Decimal(str(row[k] or 0)) for k in ['zywnosc', 'niezywnosc', 'car_cost', 'oplaty', 'medycyna', 'inne'])
                bilans_data.setdefault(ym, {})['wydatki'] = bilans_data.get(ym, {}).get('wydatki', Decimal('0.00')) + suma

            for row in rory_rows:
                ym = str(row['data'])[:7]
                suma = sum(Decimal(str(row[k] or 0)) for k in ['PKO', 'mBank', 'Millenium', 'obligacje', 'fundusze', 'lokaty', 'gotowka', 'ike_ikze', 'gielda'])
                suma += Decimal(str(row['EURO'] or 0)) * Decimal(str(row['EURO_kurs'] or 0))
                suma += Decimal(str(row['USD'] or 0)) * Decimal(str(row['USD_kurs'] or 0))
                bilans_data.setdefault(ym, {})['ror'] = suma 

            result = []
            for ym in sorted(bilans_data.keys(), reverse=True):
                p = bilans_data[ym].get('przychody', Decimal('0.00'))
                w = bilans_data[ym].get('wydatki', Decimal('0.00'))
                r = bilans_data[ym].get('ror', Decimal('0.00'))
                bilans_mies = p - w
                result.append({
                    'ym': ym,
                    'przychody': format_polish(p),
                    'wydatki': format_polish(w),
                    'bilans': format_polish(bilans_mies),
                    'bilans_color': 'text-success' if bilans_mies >= 0 else 'text-danger',
                    'ror': format_polish(r)
                })
            return render_template('bilans.html', bilans_data=result)
        except Exception as e:
            print("Błąd bilansu:", e)
            return render_template('bilans.html', bilans_data=[])
