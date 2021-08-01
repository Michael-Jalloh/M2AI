from flask import Blueprint, request, session, render_template, url_for, redirect, flash, abort

from flaskapp.models import User, Food, FoodType, Order
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
@admin.route('/orders/<order_status>')
def orders(order_status=None):
    if 'email' in session:
        pageTitle = 'Incoming'
        if order_status != None:
            orders = Order.query.filter(Order.status == order_status).all()
            pageTitle = order_status.capitalize()
        else:
            orders =  Order.query.filter(Order.status == pageTitle).all()
        
        return render_template('orders.html', orders=orders, pageTitle=pageTitle)
    else:
        return redirect(url_for('auth.login'))


@admin.route('/assignOrder', methods=['GET', 'POST'])
def assignOrder():
    if 'email' in session:
        if request.method == "POST":
            driver_id = request.form['driver_id']
            order_id = request.form['order_id']
            order = Order.query.filter_by(id = order_id).first()
           
            try:

                order.driver_id = driver_id
                order.status = 'Outgoing'
                db.session.commit()
                flash('Driver Successfully Assigned the Order', 'success')
                return redirect(url_for('admin.orders'))
            except:
                return 'Ops! Something went wong lol!'
            
    
    else:
        return redirect(url_for('auth.login'))


@admin.route('/acceptOrder/<int:id>')
def acceptOrder(id):
    if 'email' in session:
      
        order = Order.query.filter_by(id = id).first()
        
        try:
            
            order.status = 'Waiting'
            db.session.commit()
            flash('Order Accepted', 'success')

            return redirect(url_for('admin.orders'))
        except Exception as e:
            print(e)
            
    
    else:
        return redirect(url_for('auth.login'))



@admin.route('/rejectOrder/<int:id>')
def rejectOrder(id):
    if 'email' in session:
      
        order = Order.query.filter_by(id = id).first()
        
        try:

            order.status = 'Cancelled'
            db.session.commit()
            flash('Order Rejected', 'success')

            return redirect(url_for('admin.orders'))
        except:
            return 'Ops! Something went wrong!'
            
    
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




@admin.route('/viewOrder/<int:id>')
def viewOrder(id):
    if 'email' in session:
        #get the order details
        order = Order.query.filter(Order.id == id).first()
        
        return render_template('view_order.html', order=order)
    else:
        return redirect(url_for('auth.login'))

