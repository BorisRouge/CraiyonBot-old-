import time
import jwt
import json
import requests
#from jose import jwt
import os
class Token():
  def __init__(self):
    self.IAM_TOKEN = ''
    
  def get_token(self):
    service_account_id = os.getenv('service_account_id')
    key_id = os.getenv('key_id') # ID ресурса Key, который принадлежит сервисному аккаунту.
    with open("newkey.json", 'r') as private:
      private_key = private.read() # Чтение закрытого ключа из файла.
      private_key = json.loads(private_key)['private_key']      
    now = int(time.time())
    payload = {
            'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
            'iss': service_account_id,
            'iat': now,
            'exp': now + 360}
    
    # Формирование JWT.
    encoded_token = jwt.encode(
        payload,
        private_key,
        algorithm='PS256',
        headers={'kid': key_id})
        
    url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
    headers = {'Content-Type': 'application/json'}
    body = {#"serviceAccountId": service_account_id,
            "jwt": encoded_token}
    r = requests.post(url,data=json.dumps(body), headers=headers)    
    self.IAM_TOKEN = r.json()["iamToken"]
    return self.IAM_TOKEN


