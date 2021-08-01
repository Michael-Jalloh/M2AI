# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset, Restarted, SlotSet
import requests as r

food_list = r.get("http://127.0.0.1:5000/api/get_all_foods").json()# ["Ham burger", "chicken and chips", "coke", "sprite", "fanta", "beef stew"]
food_types = {"starter": 1, "breakfast":2, "dinner": 3, "lunch": 4, "drink": 5}
server_url = "http://127.0.0.1:5000/api/"

class ActionGetMenu(Action):

    def name(self) -> Text:
        return "action_get_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food_type = tracker.get_slot("food_type")
        print(food_type)
        if food_type:
            try:
                data = r.get(server_url+f"get_foods/{food_types[food_type.lower()]}").json()
                print(data)
                foods = []
                if data != None and data != []:
                    for food in data:
                        foods.append(food["name"])
                dispatcher.utter_message("These are the foods u ask for\n" + "\n".join(foods)+"\n Please pick one")
            except Exception as e:
                print(str(e))
        else:
            try:
                data = r.get(server_url+f"get_food_types").json()
                #print(data)
                menus = []
                if data != None and data != []:
                    for menu in data:
                        menus.append(
                            {"text": f"i want {menu['food_type']}", "data":f"sweet"}
                        )
                    dispatcher.utter_button_message("Please pick a menu", menus)
                else:
                    dispatcher.utter_message("Our menu is unavaible at the moment")
            except Exception as e:
                print(e)
                dispatcher.utter_message(text=f"server unavaible")
            #dispatcher.utter_message(text="We got starters, main dish and lunch")
        return [SlotSet("food_type","")]

class ActionAddForm(Action):
    
    def name(self) -> Text:
        return "action_add_food"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message#.get("intent")
        text = intent["text"]
        foods = tracker.get_slot("foods")
        food_list = r.get("http://127.0.0.1:5000/api/get_all_foods").json()
        if foods == None:
            foods = []
        for food in food_list:
            if food.lower() in text.lower():
                foods.append(food.lower())
        print(foods)
        dispatcher.utter_message(response="utter_and_what_else")
        if foods != None or foods != []:
            return [SlotSet("foods", foods)]
        
        return []

class ActionProcessOrder(Action):

    def name(self) -> Text:
        return "action_process_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        foods = tracker.get_slot("foods")
        text = ", ".join(foods)
        payload = [{
                    "text":"My Location",
                    "request_location": True 
                }]
        dispatcher.utter_message(text)        
        dispatcher.utter_button_message("Please share your location", [{
                    "text":"My Location",
                    "request_location": True 
                }])
        return [SlotSet("foods",[])]

class ActionCancelOrder(Action):

    def name(self) -> Text:
        return "action_cancel_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # foods = tracker.get_slots("foods")
        # text = "/n".join(foods)
        # dispatcher.utter_message(text)        
        dispatcher.utter_message(response="utter_cancel_order")
        return [SlotSet("foods",[])]