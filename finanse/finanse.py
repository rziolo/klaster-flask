import os
from flask import Flask, render_template
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

# Używamy ścieżki bezwzględnej dla pewności
template_dir = os.path.abspath('../aplikacja/templates')
app = Flask(__name__, template_folder=template_dir)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        ssl_disabled=True
    )

@app.route('/finanse')
def index():
    db_status = False
    try:
        conn = get_db_connection()
        if conn.is_connected():
            db_status = True
        conn.close()
    except Exception as e:
        print(f"Błąd połączenia: {e}")
        db_status = False

    return render_template('index_finanse.html', db_connected=db_status)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
