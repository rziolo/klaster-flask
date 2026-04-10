import os
from flask import Flask
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

app = Flask(__name__)

@app.route('/inwestycje')
def index():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            ssl_disabled=True
        )
        return "Serwis Inwestycje: Baza Inwestycje Połączona"
    except Exception as e:
        return f"Serwis Inwestycje: Błąd bazy ({str(e)})"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002)
