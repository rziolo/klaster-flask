from flask import Flask, render_template
app = Flask(__name__, template_folder='../aplikacje/templates')

@app.route('/zdrowie')
def index():
    return "Serwis Zdrowie: Działa (tryb offline)"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5003)
