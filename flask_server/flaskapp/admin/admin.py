from flask import Blueprint, request, session, render_template, url_for, redirect, flash

from flaskapp.models import User, Food, FoodType
from werkzeug.utils import secure_filename
from flaskapp.app import db
import imghdr
import os
import secrets

admin = Blueprint("admin", __name__, static_folder='static', template_folder='templates')


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0) 
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


@admin.route("/")
@admin.route('/dashboard')
def dashboard():
    if 'email' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('auth.login'))


@admin.route('/foods')
@admin.route('/foods/<food_type>')
def foods(food_type=None):
    foodTypes = FoodType.query.all()
    if 'email' in session:
        # get the food types
        pageTitle = 'All'
        if food_type != None:
            foods = Food.query.filter(Food.food_type_id == food_type).filter(Food.is_deleted == 0).all()
            pageTitle = FoodType.query.get_or_404(food_type).food_type
        else:
            foods = Food.query.filter(Food.is_deleted == 0).all()

        return render_template('foods.html', foods=foods, foodTypes=foodTypes, pageTitle = pageTitle)

        
    else:
        return redirect(url_for('auth.login'))



@admin.route('/deleteFood', methods=['GET', 'POST'])
def deleteFood():
    if 'email' in session:
        if request.method == "POST":
            id = request.get_json().get('id')
            food = Food.query.filter_by(id = id).first()
            try:

                food.is_deleted = 1
                db.session.commit()

                return "success"
            except:
                return 'Ops! Something went wong lol!'
            
    
    else:
        return redirect(url_for('auth.login'))


@admin.route('/drivers')
@admin.route('/drivers/<driver_status>')
def drivers(driver_status=None):
    if 'email' in session:
        pageTitle = 'All'

        return render_template('drivers.html', pageTitle = pageTitle)
    
    else:
        return redirect(url_for('auth.login'))



@admin.route('/orders')
def orders():
    if 'email' in session:
        return render_template('orders.html')
    else:
        return redirect(url_for('auth.login'))



@admin.route('/addNewFood', methods=['GET', 'POST'])
def addNewFood():
    foodTypes = FoodType.query.all()


    if request.method == 'POST':

        food_name = request.form['food_name']
        food_type = request.form['category']
        price = request.form['price']
        description = request.form['description']
        picture = request.files['file']

        if len(food_name) == 0 or len(food_type) == 0 or len(price) == 0 or len(description) == 0 or picture.filename == '':
            flash('All fields must be filled', 'error')
            
        else:    
            filename = secure_filename(picture.filename)
            if filename != '':
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in ['.jpg', '.png', '.gif'] or file_ext != validate_image(picture.stream):
                    abort(400)
                new_file_image = f"{secrets.token_hex(10)}{file_ext}"
                picture.save(os.path.join('flaskapp/static/images/foods/', new_file_image))


            # save the image name and description
            flash('Food successfully added!', 'success')
            food = Food(None, food_name, price, description, new_file_image, food_type)
            db.session.add(food)
            db.session.commit()

                
            
        
    return render_template('add_new_food.html', foodTypes = foodTypes)
