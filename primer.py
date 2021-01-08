# -*- coding: utf-8 -*-
from YandexSpeech import *

if __name__ == "__main__":
    conf = read_speech_config('./YandexSpeech/speech.ini')
    conf['iam_token'] = get_iam_token(conf['oauth_token'])
    print("iam_token:", conf['iam_token'])
    person = SpeechPerson(**dict_copy(conf, ['iam_token', 'folder_id', 'lang', 'voice', 'format', 'sampleRateHertz']))
    texts_to_speech = {
        'speech1.ogg': 'Привет мир!',
        'speech2.ogg': 'А мы тут, знаете, все плюшками балуемся',
    }
    for filename, text in texts_to_speech.items():
        print("{:}: {:}".format(filename, text))
        person.synthesize_to_file(filename, text)
