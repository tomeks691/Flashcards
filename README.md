# Telegram Flashcards Bot

This is a Telegram bot that helps you memorize foreign language vocabulary with flashcards. The bot sends a randomly selected flashcard (a word in a foreign language) and asks you to translate it into your native language. You answer the question by sending a message to the bot.
It contains a menu in which we can choose whether we want to test from flashcards or create a new list of flashcards. Thanks to the script add_flashcards.py we can add words via telegram.
## Getting Started

To use this bot, you need to do the following:

1. Create a Telegram bot by following the instructions [here](https://core.telegram.org/bots#3-how-do-i-create-a-bot).
2. Install the required dependencies.
3. Create a file called `.env` and add your Telegram bot API token and chat ID as follows:

```
api_bot=<YOUR_TELEGRAM_BOT_API_TOKEN>
chat_id=<YOUR_TELEGRAM_CHAT_ID>
api_bot_save_flashcards=<YOUR_TELEGRAM_BOT_API_TOKEN_TO_SAVE_NEW_FLASHCARDS>
```
4. Run the bot by running `python receive.py` and next `python send_flashcards.py`.

## How it Works
1. The bot sends you a message with menu buttons
2. If you choose test:
   - The bot randomly selects flashcards from the list of flashcards in the `wordlists.db` database.
   - The bot sends you a message with the foreign word you need to translate.
   - You send a message to the bot with your translation.
   - The bot checks your translation with saved translate and send you message if you be correctly or not
   - The process repeats with a new card, unless you typed `back` it will return to the menu.
3. If you choose `New list of flashcards`:
   - You will be asked what you want to name the new list of cards
   - It will return to the menu

## Requirements
- Python 3.6 or later
- Telepot
- Mtranslate
- Python-dotenv
- SQLITE3

## TO-DO
- Create a PDF of words for studying
