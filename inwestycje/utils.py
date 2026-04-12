import os
import csv
from datetime import datetime

# Ścieżka do plików ETL
CSV_PATH = '/var/www/html/flask/inwestycje/etl/csv/'

def get_csv_date(filename, row_idx, col_idx, delimiter=','):
    path = os.path.join(CSV_PATH, filename)
    if not os.path.exists(path):
        return "brak"
    try:
        with open(path, mode='r', encoding='utf-8') as f:
            reader = list(csv.reader(f, delimiter=delimiter))
            if len(reader) > row_idx:
                val = reader[row_idx][col_idx].strip()
                return val[:10]  # Zwraca tylko YYYY-MM-DD
    except:
        return "błąd"
    return "brak"

def get_db_status(mysql):
    status = {}
    try:
        cur = mysql.connection.cursor()
        
        # 1. Dane spółek
        cur.execute("SELECT MAX(data) as d FROM dane")
        res = cur.fetchone()
        status['data_dane'] = str(res['d']) if res and res['d'] else "brak"

        # 2. Dane dzienne
        cur.execute("SELECT MAX(data) as d FROM dane_dzienne")
        res = cur.fetchone()
        status['data_dane_dzienne'] = str(res['d']) if res and res['d'] else "brak"
        
        # 3. LICZNIK SPÓŁEK (active_ticker)
        cur.execute("SELECT COUNT(DISTINCT ticker_nm) as cnt FROM obroty WHERE sprzedaz_data IS NULL")
        res_active = cur.fetchone()
        status['active_ticker'] = res_active['cnt'] if res_active else 0

        cur.close()
    except:
        status['data_dane'] = "błąd DB"
        status['data_dane_dzienne'] = "błąd DB"
        status['active_ticker'] = 0

    # Dane z CSV
    status['data_import_gpw'] = get_csv_date('import_gpw.csv', 1, 0)
    status['data_import_gpw_nc'] = get_csv_date('import_gpw_nc.csv', 0, 0)
    status['data_import_zagr'] = get_csv_date('import_zagr.csv', 0, 0)
    status['data_import_stooq'] = get_csv_date('import_stooq.csv', 1, 0)

    path_nowe = os.path.join(CSV_PATH, 'gpw_nowe.csv')
    if os.path.exists(path_nowe) and os.path.getsize(path_nowe) > 0:
        with open(path_nowe, 'r') as f:
            content = f.read().strip()
            status['gpw_nowe'] = content if content else "brak"
    else:
        status['gpw_nowe'] = "brak"

    return status

def format_polish(value):
    if value is None: return "0,00"
    try:
        return f"{float(value):,.2f}".replace(',', ' ').replace('.', ',').replace(' ', ' ')
    except:
        return value

def get_csv_preview_html(filename, limit=10):
    """Odczytuje plik CSV i zwraca jego zawartość jako tabelę HTML."""
    path = os.path.join(CSV_PATH, filename)
    if not os.path.exists(path):
        return '<div class="alert alert-danger">Plik nie istnieje.</div>'
    
    try:
        html = '<table class="table table-sm table-striped table-bordered small">'
        with open(path, mode='r', encoding='utf-8') as f:
            # Próbujemy wykryć separator (średnik lub przecinek)
            content = f.read(2048)
            f.seek(0)
            dialect = csv.Sniffer().sniff(content, delimiters=';,')
            reader = csv.reader(f, dialect)
            
            for i, row in enumerate(reader):
                if i >= limit: break # Ograniczamy podgląd do X wierszy
                
                html += '<tr>'
                for cell in row:
                    # Jeśli to pierwszy wiersz, robimy nagłówki
                    if i == 0:
                        html += f'<th>{cell}</th>'
                    else:
                        html += f'<td>{cell}</td>'
                html += '</tr>'
        
        html += '</table>'
        return html
    except Exception as e:
        return f'<div class="alert alert-danger">Błąd odczytu pliku: {e}</div>'
