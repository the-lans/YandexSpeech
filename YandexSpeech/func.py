# -*- coding: utf-8 -*-
import configparser
import requests
import json

def read_speech_config(filename):
    """
    Чтение конфигурации.
    @param filename: Имя файла.
    @return: (dict) - Конфигурация.
    """
    cfg = configparser.ConfigParser(allow_no_value=True)
    cfg.read(filename, encoding='utf-8')
    print(cfg.defaults())
    conf = {'oauth_token': cfg.get('DEFAULT', 'oauth_token'),
            'folder_id': cfg.get('DEFAULT', 'folder_id'),
            'lang': cfg.get('DEFAULT', 'lang'),
            'voice': cfg.get('DEFAULT', 'voice'),
            'format': cfg.get('DEFAULT', 'format'),
            'sampleRateHertz': cfg.getint('DEFAULT', 'sampleRateHertz')}
    return conf

def get_iam_token(oauth_token):
    """
    Получение IAM-токена.
    @param oauth_token: OAuth-токен в сервисе Яндекс.OAuth
    @return: (str) - IAM-токен.
    """
    url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
    data = {'yandexPassportOauthToken': oauth_token}
    with requests.post(url, data=json.dumps(data)) as resp:
        if resp.status_code != 200:
            raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))
        else:
            resp_dict = resp.json()
            return resp_dict['iamToken']

def dict_copy(dictv, key_lst):
    """
    Отбор некоторых значений из словаря.
    @param dictv: Исходный словарь.
    @param key_lst: Список ключей.
    @return: Итоговый словарь.
    """
    return dict([(key, value) for key, value in dictv.items() if key in key_lst])
