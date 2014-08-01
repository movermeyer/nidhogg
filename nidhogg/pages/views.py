from flask import Blueprint, render_template

pages_app = Blueprint('pages_app', __name__)


@pages_app.route('/')
def index():
    return render_template('pages/index.html')
