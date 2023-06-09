import json
import os
import telepot
from dotenv import load_dotenv, find_dotenv
from telepot.loop import MessageLoop
from time import sleep


def handle(msg):
    with open("answer.json", "w", encoding='utf-8') as f:
        json.dump(msg, f, indent=4)


load_dotenv(find_dotenv())
api_bot = os.environ.get("api_bot")
bot = telepot.Bot(api_bot)
MessageLoop(bot, handle).run_as_thread()

while True:
    sleep(3)