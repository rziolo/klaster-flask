import os
import sys
from flask import Flask, render_template
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from jinja2 import ChoiceLoader, FileSystemLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def create_app(module_folder='inwestycje'):
    module_path = os.path.join(BASE_DIR, module_folder)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

    app = Flask(__name__,
                template_folder=os.path.join(module_path, 'templates'),
                static_folder=os.path.join(BASE_DIR, 'static'))

    load_dotenv(os.path.join(module_path, '.env'))

    app.config['MYSQL_HOST'] = os.getenv('DB_HOST')
    app.config['MYSQL_USER'] = os.getenv('DB_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv('DB_NAME')
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    app.jinja_loader = ChoiceLoader([
        FileSystemLoader(os.path.join(module_path, 'templates')),
        FileSystemLoader(os.path.join(BASE_DIR, 'shared/templates'))
    ])

    mysql = MySQL(app)
    app.mysql = mysql

    # REJESTRACJA TRAS
    try:
        if module_folder == 'finanse':
            from routes.ror import register_routes as reg_ror
            from routes.bilans import register_routes as reg_bilans
            from routes.przychody import register_routes as reg_przychody
            from routes.wydatki import register_routes as reg_wydatki
            from routes.car import register_routes as reg_car

            reg_ror(app)
            reg_bilans(app)
            reg_przychody(app)
            reg_wydatki(app)
            reg_car(app)

        elif module_folder == 'inwestycje':
            # Importujemy inwestycje.py z folderu inwestycje
            import inwestycje
            if hasattr(inwestycje, 'register_routes'):
                inwestycje.register_routes(app)

        elif module_folder == 'zdrowie':
            # Importujemy zdrowie.py z folderu zdrowie
            import zdrowie
            if hasattr(zdrowie, 'register_routes'):
                zdrowie.register_routes(app)

    except Exception as e:
        print(f"DEBUG BŁĄD ({module_folder}): {e}")

    # Główna trasa modułu jest teraz definiowana wewnątrz plików inwestycje.py / zdrowie.py
    return app
