import os
import requests
import base64
from telegram.ext import Updater, CommandHandler
import translate_api
from IAM_by_JWT import Token

API_KEY = os.getenv('API_KEY')
# The translation API token is initialized when the main.py starts. It will be renewed, when needed, in the translate_api.py module. 
IAM_TOKEN = Token()
IAM_TOKEN = IAM_TOKEN.get_token()

# Below are three functions based on someone else's tutorial
def get_url(animal):
  if animal == 'dog':
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
  if animal == 'cat':
    contents = requests.get('https://cataas.com/cat?json=true').json()
    url = f"https://cataas.com{contents['url']}"
  return url

def dog(update, context):
  url = get_url('dog')
  chat_id = update.message.chat_id
  context.bot.send_photo(chat_id=chat_id, photo=url)

def cat(update, context):
  url = get_url('cat')
  chat_id = update.message.chat_id
  context.bot.send_photo(chat_id=chat_id, photo=url)


def draw(update, context):
  """Sends the query to Craiyon and fetches the images"""
  # Check that there is a description in the request.
  if context.args == []:
     context.bot.send_message(chat_id=update.message.chat_id,
                              text='Напиши эту команду вручную, потом добавь словесное описание того, что хочешь видеть нарисованным. Например, "/draw Ельцин носит латы".',
                              reply_to_message_id=update.message.message_id)
     return(None)
  # Tell the user to be patient. 
  context.bot.send_message(chat_id=update.message.chat_id,
                           text='Подожди 30 сек.',
                           reply_to_message_id=update.message.message_id)
  promt = ' '.join(context.args)  #The arguments come as a list and we need a single string.
  print (promt)
  # Send into translation API with the promt text and initial IAM Token.
  translated = translate_api.translate(promt, IAM_TOKEN) 
  print(translated)
  # Request and response.
  response = requests.post('https://backend.craiyon.com/generate', #!!! Now it can respond with 'Too much traffic'. Gotta log the response.
                           json={"prompt":translated})
  text = response.json ()
  # Response comes as a dict with a list of b64-encoded images {'images':[]}.
  # Decode and send to the same chat. CrAIyon produces 9 images, we use only 3 for aesthetics.  
  chat_id = update.message.chat_id
  for i in range(3):
    image = base64.b64decode(text['images'][i])
    context.bot.send_photo(chat_id=chat_id, photo=image)




  
def main():  
  updater = Updater(API_KEY)
  dp = updater.dispatcher
  dp.add_handler(CommandHandler('dog',dog))
  dp.add_handler(CommandHandler('cat',cat))
  dp.add_handler(CommandHandler('draw', draw, pass_args=True))
  updater.start_polling()
  updater.idle()


if __name__ == '__main__':
  main()