from flask import Flask, redirect, url_for, session

from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chris'

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('views.home'))

    return wrap

from .views import views
from .auth import auth

app.register_blueprint(views)
app.register_blueprint(auth)




