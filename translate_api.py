import os
import requests
from IAM_by_JWT import Token

def translate (texts,IAM_TOKEN): # IAM Token should be also called from main.py when initialized.
   # Coucou.
  # print(IAM_TOKEN)
  folder_id = os.getenv('folder_id')
  target_language = 'en'  
  
  body = {
      "targetLanguageCode": target_language,
      "texts": texts,
      "folderId": folder_id,
  }
  
  headers = {
      "Content-Type": "application/json",
      "Authorization": "Bearer {0}".format(IAM_TOKEN)
  }
  
  response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
      json = body,
      headers = headers
  )
  print(response.status_code)
  if response.status_code == 401:
    print ('Unauthorized. Getting a new token.')
    IAM_TOKEN = Token()
    IAM_TOKEN = IAM_TOKEN.get_token()
    return translate (texts,IAM_TOKEN)
  return(response.json()['translations'][0]['text'])
  

