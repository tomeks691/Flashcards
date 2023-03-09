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


def check_if_enough_practice(wordlist):
    with open(f"{wordlist} Count Correct Answers.json") as f:
        flashcards = json.load(f)
    with open(f"{wordlist}.json") as f:
        flashcards_main = json.load(f)
    key_to_delete = []
    been_deleted = False
    for key in flashcards:
        if flashcards[key] == 10:
            been_deleted = True
            key_to_delete.append(key)
    for key in key_to_delete:
        del flashcards[key]
        del flashcards_main[key]
    with open(f"{wordlist} Count Correct Answers.json", "w") as f:
        json.dump(flashcards, f, indent=4)
    with open(f"{wordlist}.json", "w") as f:
        json.dump(flashcards_main, f, indent=4)
    return been_deleted


# Function for randomly selecting a flashcard to repeat
def check_if_learned(wordlist):
    with open(f"{wordlist}.json") as f:
        flashcards = json.load(f)
    if 0 in flashcards.values(): return False
    with open(f"{wordlist} Count Correct Answers.json") as f:
        flashcards_from_file_count = json.load(f)
    for flashcard_in_count_file in flashcards_from_file_count:
        for flashcard_in_main_file in flashcards:
            if flashcard_in_count_file == flashcard_in_main_file:
                flashcards_from_file_count[flashcard_in_count_file] += flashcards[flashcard_in_main_file]
    if 0 not in flashcards.values():
        for key in flashcards:
            flashcards[key] = 0
    with open(f"{wordlist}.json", "w") as f:
        json.dump(flashcards, f, indent=4)


def choose_flashcard(wordlist, bot):
    check_if_learned(wordlist)
    with open(f"{wordlist}.json") as f:
        flashcards = json.load(f)
    if len(flashcards) == 0:
        bot.sendMessage(bot_chatID, "Add some words to wordlist.")
        sys.exit()
    while True:
        flashcard = random.choice(list(flashcards.keys()))
        if flashcards[flashcard] == 0:
            return flashcard
        else:
            continue


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
def check_answer(bot, chat_id, flashcard, wordlist):
    with open(f"{wordlist}.json") as f:
        flashcards = json.load(f)
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
        flashcards[flashcard] += 1
        with open(f"{wordlist}.json", "w") as f:
            json.dump(flashcards, f, indent=4)
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
    wordlist = word_lists[wordlists_key]
    check_if_enough_practice(wordlist)
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
