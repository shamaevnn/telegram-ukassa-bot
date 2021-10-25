import logging
import sys

import telegram
from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, PreCheckoutQueryHandler, CommandHandler, Filters, Dispatcher

from tgbot.handlers.onboarding.handlers import command_start
from tgbot.handlers.payment.handlers import start_without_shipping_callback, precheckout_callback,\
    successful_payment_callback
from tub.celery import app
from tub.settings import DEBUG, TELEGRAM_TOKEN


def setup_dispatcher(dp):
    # simple start function
    dp.add_handler(CommandHandler("start", command_start))

    # Add command handler to start the payment invoice
    dp.add_handler(CommandHandler("test", start_without_shipping_callback))

    # Pre-checkout handler to final check
    dp.add_handler(PreCheckoutQueryHandler(precheckout_callback))

    # Success! Notify your user!
    dp.add_handler(MessageHandler(Filters.successful_payment, successful_payment_callback))

    return dp


def run_pooling():
    """ Run bot in pooling mode """
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = Bot(TELEGRAM_TOKEN).get_me()
    bot_link = f"https://t.me/" + bot_info["username"]

    print(f"Pooling of '{bot_link}' started")
    # it is really useful to send '👋' emoji to developer
    # when you run local test
    # bot.send_message(text='👋', chat_id=<YOUR TELEGRAM ID>)

    updater.start_polling()
    updater.idle()


bot = Bot(TELEGRAM_TOKEN)
try:
    TELEGRAM_BOT_USERNAME = bot.get_me()["username"]
except telegram.error.Unauthorized:
    logging.error(f"Invalid TELEGRAM_TOKEN.")
    sys.exit(1)


@app.task(ignore_result=True)
def process_telegram_event(update_json):
    update = Update.de_json(update_json, bot)
    dispatcher_bot.process_update(update)


dispatcher_bot = setup_dispatcher(Dispatcher(bot, None, workers=0, use_context=True))
