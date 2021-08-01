from flask import Flask, redirect, url_for, request, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_migrate import Migrate
# from config import config
#from flask_restful import Api

app = Flask(__name__) # refers to local python file
#api = Api(app)

app.secret_key = 'Dunn0 what 2 put here FOR r3al'
app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///app.db" #'mysql+pymysql://root:password@db/m2ai'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days = 5) #how long we are setting the current session data


db = SQLAlchemy(app)
migrate = Migrate(app, db)

# DASHBOARD

def create_routes():
    from flaskapp.admin import admin
    from flaskapp import auth
    from flaskapp.api import api

    app.register_blueprint(admin.admin)
    app.register_blueprint(auth.auth)
    app.register_blueprint(api.api)

    # api

create_routes()
#if __name__ == '__main__':
#    db.create_all()
#    app.run(debug=True)