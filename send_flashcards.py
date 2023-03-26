#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import time
from dotenv import load_dotenv, find_dotenv
import telepot
import random
import os

# Telegram bot settings
load_dotenv(find_dotenv())
bot_token = os.environ.get("api_bot")
bot_chatID = os.environ.get("chat_id")
word_lists = {"1": "Time_Travel"}


def choose_flashcard(wordlist, bot):
    with open(f"{wordlist}.json", encoding="UTF-8") as f:
        flashcards = json.load(f)
    if len(flashcards) == 0:
        bot.sendMessage(bot_chatID, "Add some words to wordlist.")
        sys.exit()
    flashcard = random.choice(list(flashcards.keys()))
    return flashcard


# Function for sending a flashcard to repeat via Telegram
def repeat_flashcard(bot, chat_id, flashcard):
    message = f"Repeat the translation of the word: {flashcard}"
    bot.sendMessage(chat_id, message)


# Function for delete learned flashcards
def delete_learned_flashcards(wordlist, word):
    with open(f"{wordlist}.json", encoding="UTF-8") as f:
        flashcards = json.load(f)
    del flashcards[word]
    with open(f"{wordlist}.json", "w", encoding="UTF-8") as f:
        json.dump(flashcards, f, indent=4, ensure_ascii=False)
    with open(f"{wordlist}_answered_correctly.json", encoding="UTF-8") as f:
        answered_flashcards = json.load(f)
    del answered_flashcards[word]
    with open(f"{wordlist}_answered_correctly.json", "w", encoding="UTF-8") as f:
        f.write(json.dumps(answered_flashcards, indent=4, ensure_ascii=False))
    return answered_flashcards


# Function for add how many times you answer correctly.
def answer_correctly(wordlist, flashcard):
    with open(f"{wordlist}_answered_correctly.json", encoding="UTF-8") as f:
        answered_correctly = json.load(f)
    if flashcard in answered_correctly:
        if answered_correctly[flashcard] == 10:
            answered_correctly = delete_learned_flashcards(wordlist, flashcard)
        else:
            answered_correctly[flashcard] += 1
    else:
        answered_correctly[flashcard] = 1

    with open(f"{wordlist}_answered_correctly.json", "w", encoding="UTF-8") as f:
        json.dump(answered_correctly, f, indent=4, ensure_ascii=False)


# Function for checking the correctness of the answer and sending the appropriate message via Telegram
def check_answer(bot, chat_id, flashcard, wordlist):
    with open(f"{wordlist}.json", encoding="UTF-8") as f:
        flashcards = json.load(f)
    with open("answer.txt", encoding="UTF-8") as f:
        answer = f.read().strip().lower()
    if answer.lower() == "exit":
        os.remove("answer.txt")
        bot.sendMessage(chat_id, "The End")
        sys.exit()
    if flashcards[flashcard].strip().lower() == answer:
        answer_correctly(wordlist, flashcard)
        os.remove("answer.txt")
        bot.sendMessage(chat_id, "Correct answer!")
    else:
        bot.sendMessage(chat_id, f"Incorrect answer. The correct answer is: \n {flashcards[flashcard]}")


def choose_wordlist(bot):
    while True:
        bot.sendMessage(bot_chatID, "Which word list do you wanna use?")
        msg = ""
        for option, wordlist in word_lists.items():
            msg += f"{option}: {wordlist}\n"
        bot.sendMessage(bot_chatID, msg)
        while True:
            if os.path.isfile('answer.txt'):
                with open("answer.txt") as f:
                    answer = f.read()

                break
            else:
                time.sleep(2)
                continue
        if word_lists.get(answer) is not None:
            break
        else:
            print("This dictionary not exists! Choose again.")
            os.remove("answer.txt")
            time.sleep(1)
    os.remove("answer.txt")
    return answer


# Main program loop
def main():
    # Create a Telepot bot object
    bot = telepot.Bot(bot_token)
    wordlists_key = choose_wordlist(bot)
    wordlist = word_lists[wordlists_key]
    while True:
        # Loop for repeating flashcards
        flashcard = choose_flashcard(wordlist, bot)
        repeat_flashcard(bot, bot_chatID, flashcard)
        # Wait for user answer
        while True:
            if os.path.isfile('answer.txt'):
                check_answer(bot, bot_chatID, flashcard, wordlist)
                break
            else:
                time.sleep(2)
                continue
        time.sleep(2)


if __name__ == '__main__':
    main()
