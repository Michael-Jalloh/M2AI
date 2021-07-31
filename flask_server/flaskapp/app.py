from flask import Flask, redirect, url_for, request, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_migrate import Migrate
# from config import config

app = Flask(__name__) # refers to local python file


app.secret_key = 'Dunn0 what 2 put here FOR r3al'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@127.0.0.1/m2ai'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days = 5) #how long we are setting the current session data


db = SQLAlchemy(app)
migrate = Migrate(app, db)
# DASHBOARD



def create_routes():
    from flaskapp.admin import admin
    from flaskapp import auth

    app.register_blueprint(admin.admin)
    app.register_blueprint(auth.auth)

create_routes()
#if __name__ == '__main__':
#    db.create_all()
#    app.run(debug=True)