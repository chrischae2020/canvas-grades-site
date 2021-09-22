from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from passlib.hash import pbkdf2_sha256
from .extensions import db

auth = Blueprint('auth', __name__)

@auth.route('/login/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        return User().login()

    return render_template('login.html')

@auth.route('/register/', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        return User().register()

    return render_template('register.html')

@auth.route('/signout/')
def signout():
    session.clear()
    return redirect(url_for('views.home'))