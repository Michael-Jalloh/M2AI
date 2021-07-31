from flask import Blueprint, request, session, render_template, redirect, url_for, flash

from flaskapp.models import User, Restauranteur
from flaskapp import admin


auth = Blueprint("auth", __name__, static_folder='static', template_folder='templates')


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        input_email = request.form['email']
        input_password = request.form['password']
        found_user = Restauranteur.query.filter_by(email=input_email).first()
        if found_user and input_password == found_user.password:
            session['email'] = found_user.email
            session['name'] = found_user.first_name + " " + found_user.last_name
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Incorrect Credentials', 'error')
            return render_template('login.html')
    else:
        if 'email' in session:
            return redirect(url_for('admin.dashboard'))
        else:
            return render_template('login.html')


# LOGOUT
@auth.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('name', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.login'))
