import logging

from telegram import LabeledPrice, ShippingOption, Update
from telegram.ext import (
    CallbackContext,
)

# Enable logging
from config import PROVIDER_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start_callback(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    msg = (
        "Нажми /test, чтобы протестировать покупку."
    )

    update.message.reply_text(msg)


def start_without_shipping_callback(update: Update, context: CallbackContext) -> None:
    """Sends an invoice without shipping-payment."""
    chat_id = update.message.chat_id
    title = "Подписка на FriendZone"
    description = "Подписка на 5 сезонов FriendZone"
    # select a payload just for you to recognize its the donation from your bot
    payload = "Custom-Payload"
    currency = "RUB"
    # price in dollars
    price = 100
    # price * 100 so as to include 2 decimal points
    prices = [LabeledPrice("Подписка 5", price * 100)]

    # optionally pass need_name=True, need_phone_number=True,
    # need_email=True, need_shipping_address=True, is_flexible=True
    context.bot.send_invoice(
        chat_id, title, description, payload, PROVIDER_TOKEN, currency, prices
    )


# after (optional) shipping, it's the pre-checkout
def precheckout_callback(update: Update, context: CallbackContext) -> None:
    """Answers the PreQecheckoutQuery"""
    query = update.pre_checkout_query
    # check the payload, is this from your bot?
    if query.invoice_payload != 'Custom-Payload':
        # answer False pre_checkout_query
        query.answer(ok=False, error_message="Something went wrong...")
    else:
        query.answer(ok=True)


# finally, after contacting the payment provider...
def successful_payment_callback(update: Update, context: CallbackContext) -> None:
    """Confirms the successful payment."""
    # do something after successfully receiving payment?
    update.message.reply_text("Спасибо за покупку!")
