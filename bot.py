import os
import sys

import requests
import base64

from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from telegram import InputMediaPhoto
from translator.token import Token
from translator import translate_api
import logging


logging.basicConfig(filename='logs/log.info', level='INFO')
log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler(stream=sys.stdout))

API_KEY = os.getenv('API_KEY')
# The translation API token is initialized when the bot.py starts.
# It will be renewed, when needed, in the translate_api.py module.
IAM_TOKEN = Token()
IAM_TOKEN = IAM_TOKEN.get_token()


def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Напиши словесное описание того, что хочешь видеть '
        'нарисованным. Например, "Ельцин носит латы".')


def draw(update, context, token=IAM_TOKEN):
    """Sends the query to Craiyon and fetches the images"""
    # Tell the user to be patient.
    context.bot.send_message(chat_id=update.message.chat_id,
                             text='Подожди 1-2 минуты.',
                             reply_to_message_id=update.message.message_id)
    prompt = update.message.text  # The arguments come as a list, and we need a single string.
    log.info(f'The requested prompt is: {prompt}')
    # Send into translation API with the prompt text and initial IAM Token.
    try:
        translated = translate_api.translate(prompt, token)
    except PermissionError:
        token = Token()
        token = token.get_token()
        translated = translate_api.translate(prompt, token)
    log.info(f'It has been translated as: {translated}')
    # Request and response.
    response = requests.post('https://backend.craiyon.com/generate',
                             # !!! Now it can respond with 'Too much traffic'. Gotta log the response.
                             json={"prompt": translated})
    log.info(f"Craiyon's response: {response}")
    text = response.json()
    # Response comes as a dict with a list of b64-encoded images {'images':[]}.
    # Decode and send to the same chat. CrAIyon produces 9 images, we use only 3 for aesthetics.
    chat_id = update.message.chat_id
    media_group = []
    for i in range(9):
        image = base64.b64decode(text['images'][i])
        media_unit = InputMediaPhoto(image)
        media_group.append(media_unit)
    context.bot.send_media_group(chat_id=chat_id, media=media_group)


def main():
    updater = Updater(API_KEY)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, callback=draw))
    updater.start_polling()
    log.info("Bot started")
    updater.idle()
    log.info("Bot stopped")


if __name__ == '__main__':
    main()
