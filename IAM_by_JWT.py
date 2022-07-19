import time
import jwt
import json
import requests
#from jose import jwt
#import os
class Token():
  def __init__(self):
    self.IAM_TOKEN = ''
    
  def get_token(self):
    service_account_id = "ajesfftasqmulg457ngm"
    key_id = "aje9l48u7a0m9op6a9c8" # ID ресурса Key, который принадлежит сервисному аккаунту.
    
    with open("newkey.json", 'r') as private:
      private_key = private.read() # Чтение закрытого ключа из файла.
      private_key = json.loads(private_key)['private_key']
      # print(private_key)
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
    # print (encoded_token)
    
    url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
    headers = {'Content-Type': 'application/json'}
    body = {#"serviceAccountId": service_account_id,
            "jwt": encoded_token}
    r = requests.post(url,data=json.dumps(body), headers=headers)
    # print(r)
    self.IAM_TOKEN = r.json()["iamToken"]
    return self.IAM_TOKEN


