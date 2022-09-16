import os
import sys
import requests
import logging

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler(stream=sys.stdout))


def translate(texts, token):  # IAM Token should be also called from bot.py when initialized.
    folder_id = os.getenv('folder_id')
    target_language = 'en'
    body = {
        "targetLanguageCode": target_language,
        "texts": texts,
        "folderId": folder_id,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(token)
    }
    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                             json=body,
                             headers=headers
                             )
    log.info(f'Yandex responds with: {response.status_code}')
    if response.status_code == 401:
        log.info('Unauthorized. Getting a new token.')
        return PermissionError
        # token = Token()
        # token = token.get_token()
        # return translate(texts, token)
    return response.json()['translations'][0]['text']
