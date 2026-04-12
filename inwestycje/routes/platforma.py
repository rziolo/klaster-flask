from flask import Blueprint, render_template

platforma_bp = Blueprint('platforma', __name__)

@platforma_bp.route('/inwestycje/platforma')
def index():
    return render_template('platforma.html', title="Platforma")
