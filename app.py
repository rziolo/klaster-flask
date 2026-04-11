import os
import sys
from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv

def create_app(template_folder='templates'):
    # Inicjalizacja apki
    app = Flask(__name__, 
                template_folder=template_folder,
                static_folder='../static')

    # Ładowanie .env z BIEŻĄCEGO katalogu roboczego (tam gdzie jest moduł)
    load_dotenv(os.path.join(os.getcwd(), '.env'))

    # Konfiguracja MySQL - uniwersalne mapowanie dla Twoich plików .env
    app.config['MYSQL_HOST'] = os.getenv('DB_HOST') or os.getenv('MYSQL_HOST')
    app.config['MYSQL_USER'] = os.getenv('DB_USER') or os.getenv('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD') or os.getenv('MYSQL_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv('DB_NAME') or os.getenv('MYSQL_DB')
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    mysql = MySQL(app)
    app.mysql = mysql

    return app
