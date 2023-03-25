# Telegram Flashcards Bot

This is a Telegram bot that helps you memorize foreign language vocabulary using flashcards. The bot sends you a randomly selected flashcard (a foreign language word) and asks you to translate it into your native language. You answer the question by sending a message to the bot.

## Getting Started

To use this bot, you need to do the following:

1. Create a Telegram bot by following the instructions [here](https://core.telegram.org/bots#3-how-do-i-create-a-bot).
2. Install the required dependencies.
3. Create a file called `.env` and add your Telegram bot API token and chat ID as follows:

```
api_bot=<YOUR_TELEGRAM_BOT_API_TOKEN>
chat_id=<YOUR_TELEGRAM_CHAT_ID>
```

4. Create a file called `your_wordlist_name.json` and add your flashcards as follows:

```
[
"foreign_word_1",
"foreign_word_2",
...
]
```
5. Change wordlists in line 13 ```word_lists = {"1": "Time Travel"}``` to your own file wordlists.
6. Run the bot by running `python main.py`.

## How it Works

1. The bot randomly selects a flashcard from the list of flashcards you provide in `your_wordlist_name.json`.
2. The bot sends you a message with the foreign word you need to translate.
3. You send a message to the bot with your translation.
4. The bot checks your translation with saved translate and send you message if you be correctly or not
5. The process repeats with a new flashcard.

## Requirements
- Python 3.6 or later
- Telepot
- Python-dotenv
- JSON file containing flashcards

## TO-DO
- Remove words from flashcards
- Create a PDF of words for studying
