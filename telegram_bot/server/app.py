from fastapi import FastAPI, Request
import requests as r
from secrets import token_hex
import json

from server.telegrambot import TelegramBot

app = FastAPI()
bot = TelegramBot("1847183745:AAHMGwI6d4FwXjP44ZkwXFFFQc2hIa8BlIY")

telegram_url_secret = str(token_hex(10))
bot.set_webhook(f"https://f4eb9ec671d1.ngrok.io/{telegram_url_secret}")
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
    replies = r.post("http://rasa:5005/webhooks/rest/webhook", data=json.dumps({"sender":str(msg.chat_id), "message": msg.message})).json()
    print(replies)
    for reply in replies:
        bot.send_message(reply["text"], msg.chat_id)
    return "ok"