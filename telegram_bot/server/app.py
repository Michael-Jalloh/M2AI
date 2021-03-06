from fastapi import FastAPI, Request
import requests as r
from secrets import token_hex
import json

from server.telegrambot import TelegramBot

app = FastAPI()
bot = TelegramBot("")

telegram_url_secret = str(token_hex(10))
bot.set_webhook(f"https://9e8516d84850.ngrok.io/{telegram_url_secret}")
print(telegram_url_secret)
@app.get("/")
def index():
    return {"Hello": "World"}

@app.post(f"/{telegram_url_secret}")
async def telegram(request: Request):
    payload = await request.json()
    #print(payload)
    msg = bot.get_message(payload)
    print(msg)
    if msg.location:
        bot.send_message("You ordered has been added", msg.chat_id)
        return "ok"
    replies = r.post("http://127.0.0.1:5005/webhooks/rest/webhook", data=json.dumps({"sender":str(msg.chat_id), "message": msg.message})).json()
    print(replies)
    # for reply in replies:
    #     bot.send_message(reply["text"], msg.chat_id)
    print(replies)
    for i,reply in enumerate(replies):
        if reply.get("buttons"):
            print()
            buttons = bot.build_keyboard(reply["buttons"])
            print(buttons)
            #bot.get_location("hello", msg.chat_id)
            bot.send_message(reply["text"].replace("[name]", msg.user), msg.chat_id, buttons)
        else:
            bot.send_message(reply["text"].replace("[name]", msg.user), msg.chat_id)
    return "ok"
