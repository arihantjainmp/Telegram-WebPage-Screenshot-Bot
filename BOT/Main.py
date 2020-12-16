import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

import validators
import requests
import re

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello !\nUse the command /screenshot followed by the url of the website to get a screenshot of the webage.\n Make sure you include the entire url (Including http/https)\n \nExample : /screenshot https://www.google.com\n \nThis bot is developed and maintained by Arihant Jain')


def screenshot(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    try:
        # args[0] will contain url of the website
        url = str(context.args[0])
        #validate the url
        valid = validators.url(url)
        if(valid is True) :
            msg = update.message.reply_text('Getting a screenshot.Please wait...')
            apiurl = 'https://screenshotapi.net/api/v1/screenshot?url=' + url
            contents = requests.get(apiurl).json()
            screenshot_url = contents['screenshot']
            context.bot.send_photo(chat_id=chat_id, photo=screenshot_url)
            msg.edit_text("Done ! Here's the screenshot for the webpage you requested")
        else :
            update.message.reply_text('Enter a Valid URL ! (Including http/https)')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /screenshot <url>')

def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Instructions\nUse /screenshot <url> to get the screenshot of a webpage.\nMake sure you enter the full URL (including http/https)\nExample : https://www.google.com\n\nThis bot is developed and maintained by Arihant Jain')


def main():
    """Run bot"""
    # Create the Updater and pass it your bot's token.
    updater = Updater("BOT_TOKEN", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("screenshot", screenshot))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time. This will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
