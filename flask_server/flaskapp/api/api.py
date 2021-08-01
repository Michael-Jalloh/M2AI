from flask import Blueprint, request, session, render_template, url_for, redirect, flash, send_from_directory
from flaskapp.models import Order, OrderedFood, User, Food, FoodType
from werkzeug.utils import secure_filename
from flaskapp.app import db
import json
import imghdr
import os
import secrets

api = Blueprint("api", __name__, static_folder='static', template_folder='templates')


@api.route("/api/get_all_foods")
def get_all_foods():
    foods = [food.name for food in Food.query.all()]
    return json.dumps(foods)
     
@api.route("/api/get_foods/<food_type>")
def get_foods(food_type):
    foods = Food.query.filter(Food.food_type_id == food_type).filter(Food.is_deleted == 0).all()
    foods = [food.tojson() for food in foods]
    return json.dumps(foods)    

@api.route("/api/get_food_types")
def get_food_types():
    foods = [food_type.tojson() for food_type in FoodType.query.all()]
    return json.dumps(foods)

@api.route("/api/get_image/<image>")
def get_image(image):
    print(image)
    file_path = os.path.join("flaskapp/static/images/foods/",image)
    if os.path.isfile(file_path):
        return send_from_directory("static/images/foods/", image)
    return "None"


# @api.route("/api/add_order", methods=["GET", "POST"])
# def add_order():
#     data = request.get_json()
#     foods = data["foods"]
#     for food in foods:
#         f = Food.query.filter_by(Food.name.lower() == food.lower).first()
#         if f:
#             o = Order(1,"Michael")
#             db.session.add(o)
#             db.session.commit()

#             orderfood = OrderedFood(2, o.id, f.id)
#             db.session.add(orderfood)
#             db.session.commit()
#     return "ok"