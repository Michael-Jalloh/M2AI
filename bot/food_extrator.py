from rasa.nlu.components import Component
from rasa.nlu.extractors.extractor import EntityExtractor
from rasa.nlu import utils
from rasa.nlu.model import Metadata

import os

import typing
from typing import Any, Optional, Text, Dict


foods = ["Ham burger", "chicken and chips", "coke", "sprite", "fanta", "beef stew"]

class FoodExtrator(EntityExtractor, Component):

    name = "food_extrator"
    language_list = ["en"]
    print('initialised the class')

    def __init__(self, component_config = None):
        super(FoodExtrator, self).__init__(component_config)

    def process(self, message, **kwargs):
        """Retrieve the tokens of the new message, pass it to the classifier
            and append prediction results to the message class."""
        # data = message.data
        # print("==========================")
        # print("==========================")
        # print("==========================")
        # if data:
        #     text = data.get("text", "")
        #     intent = data.get("intent")["name"]
        #     print(text)
        #     print(intent)
        
        # print("==========================")
        # print("==========================")
        # print("==========================")
        pass