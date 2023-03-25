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
word_lists = {"1": "Time Travel"}


def choose_flashcard(wordlist, bot):
    with open(f"{wordlist}.json") as f:
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


# Function for checking the correctness of the answer and sending the appropriate message via Telegram
def check_answer(bot, chat_id, flashcard, wordlist):
    with open(f"{wordlist}.json", encoding="UTF-8") as f:
        flashcards = json.load(f)
    with open("answer.txt", encoding="UTF-8") as f:
        answer = f.read()
    if answer.lower() == "exit":
        os.remove("answer.txt")
        bot.sendMessage(chat_id, "The End")
        sys.exit()
    if flashcards[flashcard] == answer:
        bot.sendMessage(chat_id, "Correct answer!")
    else:
        print(flashcards[flashcard])
        bot.sendMessage(chat_id, f"Incorrect answer. The correct answer is: \n {flashcards[flashcard]}")
    os.remove("answer.txt")


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
                os.remove("answer.txt")
                break
            else:
                time.sleep(2)
                continue
        if word_lists.get(answer) is not None:
            break
        else:
            print("This dictionary not exists! Choose again.")
    return answer


# Main program loop
def main():
    # Create a Telepot bot object
    bot = telepot.Bot(bot_token)
    wordlists_key = choose_wordlist(bot)
    wordlist = word_lists[wordlists_key]
    # Loop for repeating flashcards
    while True:
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
        time.sleep(4)


if __name__ == '__main__':
    main()
