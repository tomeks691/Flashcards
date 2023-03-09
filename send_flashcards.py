import json
import sys
import time
import openai
from dotenv import load_dotenv, find_dotenv
import telepot
import random
import os

# Telegram bot settings
load_dotenv(find_dotenv())
bot_token = os.environ.get("api_bot")
bot_chatID = os.environ.get("chat_id")
word_lists = {"1": "Time Travel"}


# Function for randomly selecting a flashcard to repeat
def choose_flashcard(wordlist):
    with open(f"{wordlist}.json") as f:
        flashcards = json.load(f)
    return random.choice(flashcards)


# Function for sending a flashcard to repeat via Telegram
def repeat_flashcard(bot, chat_id, flashcard):
    message = f"Repeat the translation of the word: {flashcard}"
    bot.sendMessage(chat_id, message)


def prompt_to_chat_gpt(answer="", word="", choose_chat_gpt=0):
    load_dotenv(find_dotenv())
    openai.organization = os.environ.get("organization")
    openai.api_key = os.environ.get("api_auth")
    choose = [
        f"Zwróć odpowiedz jako wartość bool dla tekstu: \n Czy {word} po polsku to {answer}. Odpowiedź zwróc tylko jako True lub False",
        f"Przetłumacz słowo {word} na język polski:"]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": choose[choose_chat_gpt]},
        ],
    )
    result = ''
    for choice in response["choices"]:
        result += choice["message"]["content"]
    return result


# Function for checking the correctness of the answer and sending the appropriate message via Telegram
def check_answer(bot, chat_id, flashcard):
    with open("answer.txt") as f:
        answer = f.read()
    if answer.lower() == "exit":
        os.remove("answer.txt")
        bot.sendMessage(chat_id, "The End")
        sys.exit()
    result = prompt_to_chat_gpt(answer=answer, word=flashcard, choose_chat_gpt=0).strip()
    if "." in result:
        result = result.replace(".", "")
    with open("log.txt", "a") as f:
        f.write(f"{result}\n")
    if result == "True":
        bot.sendMessage(chat_id, "Correct answer!")
    elif result == "False":
        correct_answer = prompt_to_chat_gpt(word=flashcard, choose_chat_gpt=1).strip()
        bot.sendMessage(chat_id, f"Incorrect answer. The correct answer is: \n {correct_answer}")
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
    # Loop for repeating flashcards
    while True:
        flashcard = choose_flashcard(word_lists[wordlists_key])
        repeat_flashcard(bot, bot_chatID, flashcard)
        # Wait for user answer
        while True:
            if os.path.isfile('answer.txt'):
                check_answer(bot, bot_chatID, flashcard)
                break
            else:
                time.sleep(2)
                continue
        time.sleep(4)


if __name__ == '__main__':
    main()
