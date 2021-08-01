import requests
import json
import urllib


class Msg(object):
    def __init__(self, message, chat_id, user, location):
        self.message = message
        self.chat_id = chat_id
        self.user = user
        self.location = location

class TelegramBot(object):
    def __init__(self, token):
        self.BOT_URL = f"https://api.telegram.org/bot{token}/"
        self.last_id = None
    
    def delete_webhook(self):
        try:
            return requests.get(f"{self.BOT_URL}deleteWebhook")
        except requests.exceptions.ConnectionError:
            return self.no_network()
    
    def set_webhook(self, webhook):
        try:
            return requests.post(f"{self.BOT_URL}setWebhook", json={"url":webhook}).json()
        except requests.exceptions.ConnectionError:
            return self.no_network()
    
    def get_webhook(self):
        try:
            return requests.post(f"{self.BOT_URL}getWebhookInfo").json()
        except requests.exceptions.ConnectionError:
            return self.no_network()

    def get_me(self):
        try:
            return requests.get(f"{self.BOT_URL}getMe").json()
        except requests.exceptions.ConnectionError:
            return self.no_network()

    def get_last_update_id(self, updates):
        last_update = len(updates["result"]) - 1
        if last_update >= 0:
            self.last_id = int(updates["result"][last_update]["update_id"]) + 1

    def get_update(self):
        url = f"{self.BOT_URL}getUpdates?timeout=100"
        if self.last_id:
            url += f"&offset={self.last_id}"
        try:
            res = requests.get(url, timeout=10).json()
            print(res)
            return self.get_messages(res)
        except requests.exceptions.ReadTimeout:
            print("[*] Timeout")
            return 
        except requests.exceptions.ConnectionError:
            return self.no_network()

    def get_messages(self, res):
        messages = []
        #print(res)
        for data in res["result"]:
            msg = self.get_message(data)
            messages.append(msg)
        self.get_last_update_id(res)
        return messages

    def get_message(self, data):
        message = Msg(data["message"].get("text",None), data["message"]["chat"]["id"], data["message"]["chat"]["first_name"], data["message"].get("location",None))
        return message

    def send_message(self, message, chat_id, reply_markup = None):
        message = urllib.parse.quote_plus(message)
        url = self.BOT_URL + f"sendMessage?text={message}&chat_id={chat_id}"
        if reply_markup:
            url = self.BOT_URL + f"sendMessage?text={message}&chat_id={chat_id}&reply_markup={json.dumps(reply_markup)}"
        try:
            #return requests.get(self.BOT_URL +"sendMessage", data = data).json()
            return requests.get(url)
        except requests.exceptions.ConnectionError:
            return self.no_network()

    def get_location(self, message, chat_id):
        payload = {
                "one_time_keyboard": True,
                "keyboard": [[{
                    "text":"My Location",
                    "request_location": True 
                }],
                ["Cancel"]]
            }
        print(payload)
        self.send_message(message, chat_id, payload)
    
    def get_contact(self, message, chat_id):
        payload = {
                "one_time_keyboard": True,
                "keyboard": [[{
                    "text":"My Contact",
                    "request_contact": True 
                }],
                ["Cancel"]]
            }
        
        self.send_message(message, chat_id, payload)

    def send_location(self,chat_id, longitude, latitude):
        print(longitude, latitude)
        url = self.BOT_URL + f"sendlocation?chat_id={chat_id}&longitude={longitude}&latitude={latitude}"
        try:
            print(url)
            r = requests.get(url)
            print(r.status_code)
            print(r.json())
            return r
        except requests.exceptions.ConnectionError:
            return self.no_network()

    def no_network(self):
        print("[*] No Network")
        return

    def build_keyboard(self, items, row=1, one_time=True):
        keyboard = []
        key_row = []
        for item in items:
            key_row.append(item)
            if len(key_row) == row:
                keyboard.append(key_row.copy())
                key_row = []
        if len(key_row) > 0: keyboard.append(key_row)
        keyboard = {"keyboard": keyboard, "one_time_keyboard": one_time}
        return keyboard

    def chatbot(self, msg: Msg):
        try:
            data = json.dumps({"sender": "t-" + str(msg.chat_id), "message": msg.message})
            headers = {"Content-type":"application/json", "Accept":"text/plain"}
            replies = requests.post(self.rasa_url, data= data, headers= headers).json()
            print(replies)
            
            for i,reply in enumerate(replies):
                if reply.get("buttons"):
                    buttons = self.build_keyboard(replies["buttons"])
                    self.send_message(reply["text"].replace("[name]", msg.user), msg.chat_id, buttons)
                else:
                    self.send_message(reply["text"].replace("[name]", msg.user), msg.chat_id) 
        except requests.exceptions.ConnectionError:
            print("[*] No Network")
            return


        
