# Telegram Flashcards Bot with OpenAI GPT-3

This is a Telegram bot that helps you memorize foreign language vocabulary using flashcards. The bot sends you a randomly selected flashcard (a foreign language word) and asks you to translate it into your native language. You answer the question by sending a message to the bot. The bot then checks your answer using OpenAI GPT-3 and sends you a response indicating whether your answer was correct or not.

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

5. Run the bot by running `python main.py`.

## How it Works

1. The bot randomly selects a flashcard from the list of flashcards you provide in `your_wordlist_name.json`.
2. The bot sends you a message with the foreign word you need to translate.
3. You send a message to the bot with your translation.
4. The bot checks your translation using OpenAI GPT-3 and sends you a response indicating whether your answer was correct or not.
5. The process repeats with a new flashcard.

## Using OpenAI GPT-3

This bot uses OpenAI GPT-3 to check the correctness of your answers. To use OpenAI GPT-3, you need to have an API key and be a member of the OpenAI organization. You can sign up for OpenAI and get an API key [here](https://beta.openai.com/signup/).

To use your OpenAI API key with this bot, add the following lines to your `.env` file:

```
organization=<YOUR_OPENAI_ORGANIZATION_ID>
api_auth=<YOUR_OPENAI_API_KEY>
```
## Requirements
- Python 3.6 or later
- Telepot
- OpenAI API key
- Python-dotenv
- JSON file containing flashcards

## TO-DO
- Remove words from flashcards
- Create a PDF of words for studying
