import os
import sys
from jinja2 import ChoiceLoader, FileSystemLoader

# Ścieżki
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SHARED_TEMPLATES = os.path.abspath(os.path.join(BASE_DIR, '..', 'shared', 'templates'))
LOCAL_TEMPLATES = os.path.join(BASE_DIR, 'templates')

# Dodanie ścieżki nadrzędnej dla importu create_app
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, '..')))
from app import create_app

# Inicjalizacja aplikacji
app = create_app(template_folder=LOCAL_TEMPLATES)

# Konfiguracja Jinja2, aby szukała w obu folderach (lokalnym i shared)
app.jinja_loader = ChoiceLoader([
    FileSystemLoader(LOCAL_TEMPLATES),
    FileSystemLoader(SHARED_TEMPLATES)
])

# 1. Rejestracja standardowych modułów
from routes import ror, wydatki, przychody
ror.register_routes(app)
wydatki.register_routes(app)
przychody.register_routes(app)

# 2. Rejestracja nowych Blueprintów
from routes.bilans import bilans_bp
from routes.car import car_bp

bilans_bp.mysql = app.mysql
car_bp.mysql = app.mysql

app.register_blueprint(bilans_bp, url_prefix='/finanse/bilans')
app.register_blueprint(car_bp, url_prefix='/finanse/car')

# 3. Trasa główna
from flask import render_template
@app.route('/finanse')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
