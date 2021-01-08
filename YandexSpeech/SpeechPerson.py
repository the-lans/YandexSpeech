# -*- coding: utf-8 -*-
import requests
import json
#from .func import *

class SpeechPerson:
    def __init__(self, iam_token, folder_id, lang='ru-RU', voice='oksana', format='oggopus', sampleRateHertz=48000):
        self.iam_token = iam_token
        self.folder_id = folder_id
        self.lang = lang
        self.voice = voice
        self.format = format
        self.sampleRateHertz = sampleRateHertz

    def update_iam_token(self, oauth_token):
        """
        Обновление IAM-токена (раз в 1-12 часов).
        @param oauth_token: OAuth-токен в сервисе Яндекс.OAuth
        """
        url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
        data = {'yandexPassportOauthToken': oauth_token}
        with requests.post(url, data=json.dumps(data)) as resp:
            if resp.status_code != 200:
                raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))
            else:
                resp_dict = resp.json()
                self.iam_token = resp_dict['iamToken']

    def synthesize(self, text, emotion='neutral', speed=1.0):
        """
        Синтезирование голоса.
        @param text: Текст, который нужно озвучить, в кодировке UTF-8.
        @param emotion: Эмоциональная окраска голоса. Поддерживается только при выборе русского языка (ru-RU)
            и голосов jane или omazh.
        @param speed: Скорость (темп) синтезированной речи.
        @return: (iterator) - Данные для озвучки (потоковая передача).
        """
        url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
        headers = {'Authorization': 'Bearer ' + self.iam_token}
        data = {
            'text': text,
            'lang': self.lang,
            'voice': self.voice,
            'emotion': emotion,
            'speed': str(speed),
            'format': self.format,
            'folderId': self.folder_id,
        }
        if self.format == 'lpcm':
            data.update({'sampleRateHertz': self.sampleRateHertz})

        with requests.post(url, headers=headers, data=data, stream=True) as resp:
            if resp.status_code != 200:
                raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))
            for chunk in resp.iter_content(chunk_size=None):
                yield chunk

    def synthesize_to_file(self, filename, text, emotion='neutral', speed=1.0):
        """
        Синтезирование голоса и запись в файл.
        @param text: Текст, который нужно озвучить, в кодировке UTF-8.
        @param emotion: Эмоциональная окраска голоса. Поддерживается только при выборе русского языка (ru-RU)
            и голосов jane или omazh.
        @param speed: Скорость (темп) синтезированной речи.
        @return: (iterator) - Данные для озвучки (потоковая передача).
        """
        with open(filename, "wb") as f:
            for audio_content in self.synthesize(text, emotion, speed):
                f.write(audio_content)
