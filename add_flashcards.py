import telepot
import os
import time
import json
from dotenv import load_dotenv, find_dotenv
from using_flashcards_db import Flashcard
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup
from send_flashcards import choose_wordlist


def add_flashcard(wordlist):
    while True:
        while True:
            try:
                bot = telepot.Bot(bot_token)
                bot.sendMessage(bot_chatID, f"Please enter the words into the {wordlist} flashcard:")
                break
            except:
                time.sleep(1)
                continue
        while True:
            if os.path.isfile(filename):
                with open(filename, encoding="UTF-8") as f:
                    choice = json.load(f)
                    choice = choice["text"]
                break
            else:
                time.sleep(2)
                continue
        os.remove(filename)
        flashcard = Flashcard()
        flashcard.add_new_flashcard(choice, wordlist)
        keyboard_option = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Add next word", callback_data="0")],
            [InlineKeyboardButton(text="Exit", callback_data="1")]])
        msg = f"The word {choice} has been written to the {wordlist}flashcard \n Do you want to add another word or do you want to finish?"
        while True:
            try:
                bot = telepot.Bot(bot_token)
                bot.sendMessage(bot_chatID, msg, reply_markup=keyboard_option)
                break
            except:
                time.sleep(1)
                continue
        while True:
            if os.path.isfile(filename):
                with open(filename, encoding="UTF-8") as f:
                    choice = json.load(f)
                    choice = choice["data"]
                break
            else:
                time.sleep(2)
                continue
        os.remove(filename)
        if choice == "0":
            continue
        if choice == "1":
            break


def main():
    if os.path.exists(filename):
        os.remove(filename)
    add_flashcard(choose_wordlist(False, filename))


load_dotenv(find_dotenv())
bot_token = os.environ.get("api_bot_save_flashcards")
bot_chatID = os.environ.get("chat_id")
filename = "answer_save_flashcards.json"

if __name__ == '__main__':
    main()
