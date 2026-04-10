# /var/www/html/flask/aplikacja.py
from flask import Flask, render_template
import os

app = Flask(__name__, 
            template_folder='templates',
            static_folder='../static')

@app.route('/')
@app.route('/aplikacje')
def index():
    # Renderujemy interfejs bez pobierania danych z MySQL
    return render_template('index.html', title="Moje Aplikacje - HUB")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
