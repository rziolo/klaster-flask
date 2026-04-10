import os
from flask import Flask, render_template
from dotenv import load_dotenv
import mysql.connector

# Wczytujemy zmienne z pliku .env w folderze finanse
load_dotenv()

app = Flask(__name__, template_folder='../aplikacje/templates')

def get_data():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            ssl_disabled=True
        )
        cursor = conn.cursor(dictionary=True)
        # Tutaj wpisz swoje zapytanie SQL, np.:
        # cursor.execute("SELECT * FROM transakcje ORDER BY data DESC LIMIT 10")
        # data = cursor.fetchall()
        cursor.execute("SELECT 'Baza Finanse Połączona' as status")
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data['status']
    except Exception as e:
        return f"Błąd bazy: {str(e)}"

@app.route('/finanse')
def index():
    status_db = get_data()
    return f"Status Finansów: {status_db}"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
