from flaskapp.app import db
# database .. will seperate later

class Restaurant(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(255), unique=True)
    address = db.Column('address', db.String(255))

    def __init__(self, id, name, address):
        self.id = id
        self.name = name
        self.address =  address


class Status(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    state = db.Column('state', db.String(55), unique=True)
    orders = db.relationship('Order', backref='status', lazy=True)

    def __init__(self, id, state):
        self.id = id
        self.state = state


class FoodType(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    food_type = db.Column('food_type', db.String(55), unique=True)
    foods = db.relationship('Food', backref='category', lazy=True)

    def __init__(self, id, food_type):
        self.id = id
        self.food_type = food_type
    
    def tojson(self):
        return {
            "id": self.id,
            "food_type": self.food_type
        }



class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    first_name = db.Column('first_name', db.String(100),  nullable=True)
    last_name = db.Column('last_name', db.String(100),  nullable=True)
    username = db.Column('username', db.String(100), unique=True)
    chat_id = db.Column('chat_id', db.String(255), unique=True)
    phone_number = db.Column('phone_number', db.String(7), unique=True)

    is_customer = db.Column('is_customer', db.Boolean, default=1)
    is_deactivated = db.Column('is_deactivated', db.Boolean, default=0)


    def __init__(self, first_name, username, chat_id, phone_number, is_customer):
        self.first_name = first_name
        self.username = username
        self.chat_id = chat_id
        self.phone_number =  phone_number
        self.is_customer = is_customer


class Restauranteur(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    first_name = db.Column('first_name', db.String(100),  nullable=True)
    last_name = db.Column('last_name', db.String(100),  nullable=True)
    email = db.Column('email', db.String(100), unique=True, nullable=True)
    password = db.Column('password', db.String(255), nullable=False)
    restaurant_id = db.Column('restaurant_id', db.Integer, nullable=True)

    def __init__(self, first_name, last_name, email, password, restaurant_id):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.restaurant_id = restaurant_id


class Food(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(255), unique=True)
    price = db.Column('price', db.Float)
    description = db.Column('description', db.Text, nullable=True)
    image = db.Column('image_path', db.String(255), nullable=True)
    is_deleted = db.Column('is_deleted', db.Boolean, default=0)
    food_type_id = db.Column(db.Integer, db.ForeignKey('food_type.id'), nullable=False)

    foods = db.relationship('OrderedFood', backref='food', lazy=True)

    def __init__(self, id, name, price, description, image, food_type_id):
        self.id = id
        self.name = name
        self.price =  price
        self.description = description
        self.image = image
        self.food_type_id = food_type_id
 
    def tojson(self):
        return {
        "id":self.id,
        "name": self.name,
        "price":self.price,
        "description": self.description,
        "image": self.image,
        "food_type_id": self.food_type_id
        }

class Order(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    customer_id = db.Column('customer_id', db.Integer)
    food_id = db.Column('food_id', db.Integer)
    food_name = db.Column('food_name', db.String(255))
    price = db.Column('price', db.Float)
    status_id = db.Column('status_id', db.Integer)
    driver_id = db.Column('driver_id', db.Integer)
    is_order_ready = db.Column('is_order_ready', db.Boolean)
    is_order_delivery = db.Column('is_order_delivery', db.Boolean)

    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)

    
    ordered_foods = db.relationship('OrderedFood', backref='order', lazy=True)



class OrderedFood(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    quantiy = db.Column('quantity', db.Integer)

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)

    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    



