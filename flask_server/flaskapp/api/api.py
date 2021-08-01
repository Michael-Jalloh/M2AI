from flask import Blueprint, request, session, render_template, url_for, redirect, flash

from flaskapp.models import User, Food, FoodType
from werkzeug.utils import secure_filename
from flaskapp.app import db
import json
import imghdr
import os
import secrets

api = Blueprint("api", __name__, static_folder='static', template_folder='templates')


@api.route("/api/get_foods/<food_type>")
def get_foods(food_type):
    foods = Food.query.filter(Food.food_type_id == food_type).filter(Food.is_deleted == 0).all()
    foods = [food.tojson() for food in foods]
    return json.dumps(foods)    

@api.route("/api/get_food_types")
def get_food_types():
    foods = [food_type.tojson() for food_type in FoodType.query.all()]
    return json.dumps(foods)
