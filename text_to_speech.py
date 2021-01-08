# -*- coding: utf-8 -*-
import argparse
from YandexSpeech import *

if __name__ == "__main__":
    conf = read_speech_config('./YandexSpeech/speech.ini')
    conf['iam_token'] = get_iam_token(conf['oauth_token'])
    print("iam_token:", conf['iam_token'])
    person = SpeechPerson(**dict_copy(conf, ['iam_token', 'folder_id', 'lang', 'voice', 'format', 'sampleRateHertz']))

    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=False, help="Text for synthesize")
    parser.add_argument("--output", required=False, help="Output file name")
    args = parser.parse_args()

    if not args.output:
        filename = "speech.ogg"
    if not args.text:
        filetext = "text.txt"

    with open(filetext, "r", encoding='utf-8') as f:
        text = f.read()
    print("{:}: {:}".format(filename, text))
    person.synthesize_to_file(filename, text)
