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

food_list = ["Ham burger", "chicken and chips", "coke", "sprite", "fanta", "beef stew"]

class ActionGetMenu(Action):

    def name(self) -> Text:
        return "action_get_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food_type = tracker.get_slot("food_type")
        if food_type == "main":
            dispatcher.utter_message(text=f"The {food_type} menu is .......")
        elif food_type == "lunch":
            dispatcher.utter_message(text=f"The {food_type} menu is .......")
        elif food_type == "starter":
            dispatcher.utter_message(text=f"The {food_type} menu is .......")
        elif food_type == "drink":
            dispatcher.utter_message(text=f"The {food_type} menu is .......")
        elif food_type == "breakfast":
            dispatcher.utter_message(text=f"The {food_type} menu is .......")
        else:
            dispatcher.utter_message(text="We got starters, main dish and lunch")
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
        dispatcher.utter_message(text)        
        dispatcher.utter_message(response="utter_process")
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