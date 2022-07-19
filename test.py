import requests
import time
import logging
import base64
import io
from PIL import Image
from bs4 import BeautifulSoup

logging.basicConfig(filename="logfilename.log", level=logging.INFO)

def draw():
  """Sends the string to Craiyon and fetches the image's URL"""
  response = requests.post(
                        'https://backend.craiyon.com/generate',
                        json={"prompt":"Pizza from spare parts"})
  text = response.json ()
  print (response)
  #print(text)
  image_string = text['images'][0]
  image = Image.open(io.BytesIO(base64.decodebytes(bytes(image_string, "utf-8"))))
  image.save('my-image.jpeg')
  #print(type(image))
  print(text.keys())
  #print(text['version'])
  #parsed = BeautifulSoup(text, 'html.parser')
  #logging.info(text)
  #for item in parsed.find_all('version'):
    #print ('and here')
    #print(item)

draw ()