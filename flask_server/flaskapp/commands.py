from flaskapp.models import User, UserType, Status, Restaurant, Restauranteur, FoodType, Food, db
entries = []

def seedUserTypes():
    usertypes = ['Customer', 'Driver']

    for x in range(1, len(usertypes) + 1):
        if UserType.query.get(x) == None:
            entries.append(UserType(x, usertypes[x - 1]))
    

def seedStatuses():
    statuses = ['Pending', 'Accepted', 'Delivered']

    for x in range(1, len(statuses) + 1):
        if Status.query.get(x) == None:
            entries.append(Status(x, statuses[x - 1]))

def seedRestaurants():
    if Restaurant.query.get(1) == None:
        entries.append(Restaurant(1, "Heritage","Senegambia"))


def seedFoodTypes():
    foodtypes = ['Starter', 'Breakfast', 'Dinner', 'Lunch', 'Drink']

    for x in range(1, len(foodtypes) + 1):
        if FoodType.query.get(x) == None:
            entries.append(FoodType(x, foodtypes[x - 1]))

def seedFood():

    entries.append(Food(1, 'Burger', 323, 'nada', 'images/foods/burger.jpg', 1))

    

def seedRestauranteurs():
    if Restauranteur.query.get(1) == None:
        entries.append(Restauranteur("Fatou", "Ceesay", "test@gmail.com", "password", 1))
    

def seedEverything():
    seedUserTypes()
    seedStatuses()
    seedRestaurants()
    seedRestauranteurs()
    seedFoodTypes()
    # seedFood()

    for entry in entries:
        db.session.add(entry)

    db.session.commit()


def init_app(app):
    for command in [seedEverything]:
        app.cli.add_command(app.cli.command()(command))