from flaskapp.models import User, Restaurant, Restauranteur, FoodType, Food, User, Order, OrderedFood, db
entries = []


# def seedStatuses():
#     statuses = ['Incoming', 'Accepted', 'On Road', 'Delivered', 'Cancelled', 'Busy', 'Idle']

#     for x in range(1, len(statuses) + 1):
#         if Status.query.get(x) == None:
#             entries.append(Status(x, statuses[x - 1]))

def seedRestaurants():
    if Restaurant.query.get(1) == None:
        entries.append(Restaurant(1, "Heritage","Senegambia"))


def seedFoodTypes():
    foodtypes = ['Starter', 'Breakfast', 'Dinner', 'Lunch', 'Drink']

    for x in range(1, len(foodtypes) + 1):
        if FoodType.query.get(x) == None:
            entries.append(FoodType(x, foodtypes[x - 1]))



def seedRestauranteurs():
    if Restauranteur.query.get(1) == None:
        entries.append(Restauranteur("Fatou", "Ceesay", "test@gmail.com", "password", 1))




def seedUsers():
    entries.append(User('Apollo', 'sunny', 23819, 3982031, 1))
    entries.append(User('Hermes', 'handbag', 232819, 4982031, 1))



def seedFoods():
    entries.append(Food(None, 'Pizza', 90, 'delish', 'dinner.jpg' , 3))
    entries.append(Food(None, 'Shrimps', 80, 'nice', 'breakfast.jpg', 2))

def seedOrders():
    entries.append(Order(1, "Ida"))
    entries.append(Order(2, "Musa"))
    entries.append(Order(3, "John"))

def seedOrderedFoods():
    entries.append(OrderedFood(2, 1, 1))
    entries.append(OrderedFood(3, 2, 2))
    entries.append(OrderedFood(1, 3, 1))



    

def seedEverything():
    print("================")
    print("================")
    print("================")
    print("Seeding....")
    print("================")
    print("================")
    print("================")
    # seedStatuses()
    seedRestaurants()
    seedRestauranteurs()
    seedFoodTypes()
    seedOrders()
    seedUsers()
    seedFoods()
    seedOrderedFoods()

    for entry in entries:
        db.session.add(entry)

    db.session.commit()


def init_app(app):
    for command in [seedEverything]:
        app.cli.add_command(app.cli.command()(command))