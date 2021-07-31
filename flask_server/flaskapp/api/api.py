from flask import Blueprint, request, session, render_template, url_for, redirect, flash

from flaskapp.models import User, Food, FoodType
from werkzeug.utils import secure_filename
from flaskapp.app import db
import imghdr
import os
import secrets

api = Blueprint("api", __name__, static_folder='static', template_folder='templates')




@api.route('/getImage/<image>')
def get(image):
    pass
