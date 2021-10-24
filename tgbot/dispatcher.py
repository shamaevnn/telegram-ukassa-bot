from telegram import Bot
from telegram.ext import Updater, MessageHandler, PreCheckoutQueryHandler, CommandHandler, Filters

from config import TELEGRAM_TOKEN
from .handlers import start_callback, start_without_shipping_callback, \
    precheckout_callback, successful_payment_callback


def setup_dispatcher(dispatcher):
    # simple start function
    dispatcher.add_handler(CommandHandler("start", start_callback))

    # Add command handler to start the payment invoice
    dispatcher.add_handler(CommandHandler("test", start_without_shipping_callback))

    # Pre-checkout handler to final check
    dispatcher.add_handler(PreCheckoutQueryHandler(precheckout_callback))

    # Success! Notify your user!
    dispatcher.add_handler(MessageHandler(Filters.successful_payment, successful_payment_callback))


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
