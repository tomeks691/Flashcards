import json
import time
from dotenv import load_dotenv, find_dotenv
import telepot
import random
import os
from using_flashcards_db import Flashcard
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup

# Telegram bot settings
load_dotenv(find_dotenv())
bot_token = os.environ.get("api_bot")
bot_chatID = os.environ.get("chat_id")
recently_flashcard = []
filename = "answer.json"


def menu(filename):
    menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Start Test", callback_data="0")],
        [InlineKeyboardButton(text="New list of flashcards", callback_data="1")],
        [InlineKeyboardButton(text="Learn FLashcards", callback_data="2")]])
    while True:
        try:
            bot = telepot.Bot(bot_token)
            bot.sendMessage(bot_chatID, "Which option do you wanna use?", reply_markup=menu_keyboard)
            break
        except:
            time.sleep(1)
            continue

    while True:
        if os.path.isfile(filename):
            with open(filename) as f:
                answer = json.load(f)
            answer = answer["data"]
            break
        else:
            time.sleep(2)
            continue
    os.remove(filename)
    return answer


def learn_flashcard(wordlist):
    while True:
        flashcard = choose_flashcard(wordlist)
        while True:
            try:
                bot = telepot.Bot(bot_token)
                bot.sendMessage(bot_chatID, f"{flashcard[0]}: {flashcard[1]}")
                break
            except:
                time.sleep(1)
                continue
        learn_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Next", callback_data="0")],
            [InlineKeyboardButton(text="Menu", callback_data="1")]])
        bot.sendMessage(bot_chatID, "Next Flashcard or back to the menu:", reply_markup=learn_keyboard)
        while True:
            if os.path.isfile(filename):
                with open(filename) as f:
                    answer = json.load(f)
                answer = answer["data"]
                break
            else:
                time.sleep(2)
                continue
        os.remove(filename)
        if answer == "0":
            continue
        elif answer == "1":
            break


def choose_flashcard(wordlist):
    flashcard = Flashcard()
    flashcards = flashcard.get_all_flashcards(wordlist)
    if len(flashcards) == 0:
        while True:
            try:
                bot = telepot.Bot(bot_token)
                bot.sendMessage(bot_chatID, "Add some words to wordlist.")
                break
            except:
                time.sleep(1)
                continue
        return False
    while True:
        flashcard = random.choice(flashcards)
        recently_used = check_if_recently_use(flashcard)
        if recently_used:
            continue
        else:
            break
    return flashcard


# Function for sending a flashcard to repeat via Telegram
def repeat_flashcard(chat_id, flashcard):
    message = f"Repeat the translation of the word: {flashcard}"
    while True:
        try:
            bot = telepot.Bot(bot_token)
            bot.sendMessage(chat_id, message)
            break
        except:
            time.sleep(1)
            continue


# Function for checking the correctness of the answer and sending the appropriate message via Telegram
def check_answer(chat_id, word, wordlist, filename):
    flashcard = Flashcard()
    with open(filename) as f:
        answer = json.load(f)
        answer = answer["text"]
        answer = answer.strip().lower()
    if answer == "back":
        os.remove(filename)
        return False
    correctly_answer = flashcard.check_answer(wordlist, word, answer)
    if "str" not in str(type(correctly_answer)):
        os.remove(filename)
        while True:
            try:
                bot = telepot.Bot(bot_token)
                bot.sendMessage(chat_id, "Correct answer!")
                break
            except:
                time.sleep(1)
                continue

    else:
        while True:
            try:
                bot = telepot.Bot(bot_token)
                bot.sendMessage(chat_id, f"Incorrect answer. The correct answer is: {correctly_answer}")
                break
            except:
                time.sleep(1)
                continue
        os.remove(filename)


def check_if_recently_use(flashcard):
    if len(recently_flashcard) == 10:
        del recently_flashcard[0]
    if flashcard in recently_flashcard:
        return True
    else:
        recently_flashcard.append(flashcard)
        return False


def choose_wordlist(create, filename):
    wordlists = get_wordlists_name()
    buttons = []
    if wordlists == 0 or create:
        create_wordlist(filename)
        while True:
            try:
                bot = telepot.Bot(bot_token)
                bot.sendMessage(bot_chatID, "A new list of flashcards has been created")
                break
            except:
                time.sleep(1)
                continue
        return True
    for len_keys in wordlists.keys():
        buttons.append([InlineKeyboardButton(text=wordlists[len_keys], callback_data=len_keys)])
    keyboard_wordlist = InlineKeyboardMarkup(inline_keyboard=buttons)
    while True:
        try:
            bot = telepot.Bot(bot_token)
            bot.sendMessage(bot_chatID, "Which word list do you wanna use?", reply_markup=keyboard_wordlist)
            break
        except:
            time.sleep(1)
            continue
    while True:
        if os.path.isfile(filename):
            with open(filename) as f:
                answer = json.load(f)
            answer = answer["data"]
            break
        else:
            time.sleep(2)
            continue
    os.remove(filename)
    return wordlists[answer]


def create_wordlist(filename):
    while True:
        try:
            bot = telepot.Bot(bot_token)
            bot.sendMessage(bot_chatID, "How do you wanna name your flashcards wordlist?")
            break
        except:
            time.sleep(1)
            continue

    while True:
        if os.path.isfile(filename):
            with open(filename) as f:
                answer = json.load(f)
            answer = answer["text"]
            break
        else:
            time.sleep(2)
            continue
    os.remove(filename)
    flashcard = Flashcard()
    flashcard.create_wordlist(answer)


# Add new flashcard


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
    if os.path.exists(filename):
        os.remove(filename)
    i = 0
    while True:
        choose = menu(filename)
        if choose == "0":
            wordlist = choose_wordlist(False, filename)
            while True:
                # Loop for repeating flashcards
                flashcard = choose_flashcard(wordlist)[0]
                if flashcard == False:
                    break
                repeat_flashcard(bot_chatID, flashcard)
                # Wait for user answer
                while True:
                    if os.path.isfile(filename):
                        back = check_answer(bot_chatID, flashcard, wordlist, filename)
                        break
                    else:
                        time.sleep(2)
                        continue
                if back == False:
                    break
                time.sleep(2)
        elif choose == "1":
            choose_wordlist(True, filename)
        elif choose == "2":
            wordlist = choose_wordlist(False, filename)
            learn_flashcard(wordlist)
        time.sleep(1)


if __name__ == '__main__':
    main()
