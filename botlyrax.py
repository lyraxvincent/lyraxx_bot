import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer


# Auth token
TOKEN = str(os.environ['TOKEN_KEY'])

chatbot = ChatBot(
    'lyrax',
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch"
        },

        {
            'import_path': 'chatterbot.logic.TimeLogicAdapter'
        },

        {
            'import_path': 'chatterbot.logic.MathematicalEvaluation'
        }

    ]
)

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot based on the english corpus
#trainer.train("chatterbot.corpus.english")

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# A function to process a specific type of update:
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I'm a bot, my name is lyrax, my creator is "
                                                                    "Vincent and you can reach him through: "
                                                                    "(https://t.me/lyraxvincent)\nTalk to me!")

# A function called every time the Bot receives a Telegram message that contains the /start command
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Adding another handler that listens for regular messages
def echo(update, context):

    if str(chatbot.get_response(update.message.text)) != "":
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(chatbot.get_response(update.message.text)))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Rephrase that please?")

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)


# For commands that the bot doesn't understand:
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

# starting the bot
updater.start_polling()
