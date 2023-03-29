import json
import sys
import time
from dotenv import load_dotenv, find_dotenv
import telepot
import random
import os
import sqlite3
from using_flashcards_db import Flashcard
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup

# Telegram bot settings
load_dotenv(find_dotenv())
bot_token = os.environ.get("api_bot")
bot_chatID = os.environ.get("chat_id")
recently_flashcard = []
conn = sqlite3.connect("wordlists.db")
cursor = conn.cursor()


def menu(bot):
    menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Start Test", callback_data="0")],
        [InlineKeyboardButton(text="Add words to flashcards", callback_data="1")],
        [InlineKeyboardButton(text="New list of flashcards", callback_data="2")],
        [InlineKeyboardButton(text="Exit", callback_data="3")]])
    bot.sendMessage(bot_chatID, "Which option do you wanna use?", reply_markup=menu_keyboard)
    while True:
        if os.path.isfile('answer.json'):
            with open("answer.json") as f:
                answer = json.load(f)
            answer = answer["data"]
            break
        else:
            time.sleep(2)
            continue
    os.remove("answer.json")
    return answer


def choose_flashcard(wordlist, bot):
    flashcard = Flashcard()
    flashcards = flashcard.get_all_flashcards(wordlist)
    if len(flashcards) == 0:
        bot.sendMessage(bot_chatID, "Add some words to wordlist.")
        sys.exit()
    while True:
        flashcard = random.choice(flashcards)
        recently_used = check_if_recently_use(flashcard)
        if recently_used:
            continue
        else:
            break
    return flashcard[0]


# Function for sending a flashcard to repeat via Telegram
def repeat_flashcard(bot, chat_id, flashcard):
    message = f"Repeat the translation of the word: {flashcard}"
    bot.sendMessage(chat_id, message)


# Function for checking the correctness of the answer and sending the appropriate message via Telegram
def check_answer(bot, chat_id, word, wordlist):
    flashcard = Flashcard()
    with open("answer.json", encoding="UTF-8") as f:
        answer = json.load(f)
        answer = answer["text"]
        answer = answer.strip().lower()
    if answer == "exit":
        os.remove("answer.json")
        bot.sendMessage(chat_id, "The End")
        sys.exit()
    correctly_answer = flashcard.check_answer(wordlist, word, answer)
    if "str" not in str(type(correctly_answer)):
        os.remove("answer.json")
        bot.sendMessage(chat_id, "Correct answer!")
    else:
        bot.sendMessage(chat_id, f"Incorrect answer. The correct answer is: {correctly_answer}")
        os.remove("answer.json")


def check_if_recently_use(flashcard):
    if len(recently_flashcard) == 10:
        del recently_flashcard[0]
    if flashcard in recently_flashcard:
        return True
    else:
        recently_flashcard.append(flashcard)
        return False


def choose_wordlist(bot, create):
    wordlists = get_wordlists_name()
    buttons = []
    if wordlists == 0 or create:
        create_wordlist(bot)
        bot.sendMessage(bot_chatID, "A new list of flashcards has been created")
        return True
    for len_keys in wordlists.keys():
        buttons.append([InlineKeyboardButton(text=wordlists[len_keys], callback_data=len_keys)])
    keyboard_wordlist = InlineKeyboardMarkup(inline_keyboard=buttons)
    bot.sendMessage(bot_chatID, "Which word list do you wanna use?", reply_markup=keyboard_wordlist)
    while True:
        if os.path.isfile('answer.json'):
            with open("answer.json") as f:
                answer = json.load(f)
            answer = answer["data"]
            break
        else:
            time.sleep(2)
            continue
    os.remove("answer.json")
    return wordlists[answer]


def create_wordlist(bot):
    bot.sendMessage(bot_chatID, "How do you wanna name your flashcards wordlist?")
    while True:
        if os.path.isfile('answer.json'):
            with open("answer.json") as f:
                answer = json.load(f)
            answer = answer["text"]
            break
        else:
            time.sleep(2)
            continue
    os.remove("answer.json")
    flashcard = Flashcard()
    flashcard.create_wordlist(answer)


# Add new flashcard
def add_flashcard(bot, wordlist):
    while True:
        bot.sendMessage(bot_chatID, f"Please enter the words into the {wordlist} flashcard:")
        while True:
            if os.path.isfile('answer.json'):
                with open("answer.json", encoding="UTF-8") as f:
                    choice = json.load(f)
                    choice = choice["text"]
                break
            else:
                time.sleep(2)
                continue
        os.remove("answer.json")
        flashcard = Flashcard()
        flashcard.add_new_flashcard(choice, wordlist)
        keyboard_option = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Add next word", callback_data="0")],
            [InlineKeyboardButton(text="Exit", callback_data="1")]])
        msg = f"The word {choice} has been written to the {wordlist}flashcard \n Do you want to add another word or do you want to finish?"
        bot.sendMessage(bot_chatID, msg, reply_markup=keyboard_option)
        while True:
            if os.path.isfile('answer.json'):
                with open("answer.json", encoding="UTF-8") as f:
                    choice = json.load(f)
                    choice = choice["data"]
                break
            else:
                time.sleep(2)
                continue
        os.remove("answer.json")
        if choice == "0":
            continue
        if choice == "1":
            break



def get_wordlists_name():
    flashcard = Flashcard()
    table_names = {}
    flashcards_tables = flashcard.get_all_tables()
    for tables in flashcards_tables:
        for table in tables:
            table_names[str(flashcards_tables.index(tables))] = table
    return table_names


# Main program loop
def main():
    if os.path.exists("answer.json"):
        os.remove("answer.json")
    # Create a Telepot bot object
    bot = telepot.Bot(bot_token)
    while True:
        choose = menu(bot)
        if choose == "0":
            wordlist = choose_wordlist(bot, False)
            while True:
                # Loop for repeating flashcards
                flashcard = choose_flashcard(wordlist, bot)
                repeat_flashcard(bot, bot_chatID, flashcard)
                # Wait for user answer
                while True:
                    if os.path.isfile('answer.json'):
                        check_answer(bot, bot_chatID, flashcard, wordlist)
                        break
                    else:
                        time.sleep(2)
                        continue
                time.sleep(2)
        elif choose == "1":
            wordlist = choose_wordlist(bot, False)
            add_flashcard(bot, wordlist)
        elif choose == "2":
            choose_wordlist(bot, True)
        elif choose == "3":
            sys.exit()


if __name__ == '__main__':
    main()
