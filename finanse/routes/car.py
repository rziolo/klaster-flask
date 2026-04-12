from flask import render_template
from decimal import Decimal

def register_routes(app):
    @app.route('/finanse/car')
    def car_view():
        try:
            cur = app.mysql.connection.cursor()
            # Pobieramy chronologicznie (ASC), aby móc odjąć licznik poprzedni od obecnego
            query = "SELECT data, car_km, car_cost FROM wydatki WHERE car_km > 0 ORDER BY data ASC"
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()

            def format_pl(value):
                if isinstance(value, (int, float, Decimal)):
                    return f"{value:,.2f}".replace(',', ' ').replace('.', ',')
                return "0,00"

            processed_data = []
            prev_km = None

            for row in rows:
                curr_km = row.get('car_km') or 0
                cost = row.get('car_cost') or 0
                
                # Obliczanie przebiegu (obecny licznik - poprzedni)
                przebieg = (curr_km - prev_km) if prev_km is not None else 0
                
                # Obliczanie kosztu na km (suma kosztów w miesiącu / przebieg w miesiącu)
                koszt_na_km = (cost / przebieg) if przebieg > 0 else 0

                processed_data.append({
                    'miesiac': row.get('data'),
                    'koszt_zl': format_pl(cost),
                    'licznik': f"{curr_km:,}".replace(',', ' '),
                    'poprzedni': f"{prev_km:,}".replace(',', ' ') if prev_km else "---",
                    'przebieg': f"{przebieg:,}".replace(',', ' ') if przebieg > 0 else "---",
                    'koszt_na_km': format_pl(koszt_na_km) if koszt_na_km > 0 else "---"
                })
                prev_km = curr_km

            # Odwracamy listę: najnowsze daty na górę
            processed_data.reverse()

            return render_template('car.html', rows=processed_data)
        except Exception as e:
            return f"Błąd bazy danych (Car): {e}", 500
