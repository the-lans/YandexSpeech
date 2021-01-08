# YandexSpeech
Yandex SpeechKit technology



Использование технологии озвучивания текста на базе Yandex SpeechKit.

Полная документация по Yandex SpeechKit доступна по адресу: https://cloud.yandex.ru/docs/speechkit/ 

Для того, чтобы у вас всё заработало необходимо:

1. Пройдите регистрацию в сервисе Yandex.Cloud. На странице [биллинга](https://console.cloud.yandex.ru/billing) убедитесь, что [платёжный аккаунт](https://cloud.yandex.ru/docs/billing/concepts/billing-account) находится в статусе ACTIVE или TRIAL_ACTIVE. Если платёжного аккаунта нет, [создайте его](https://cloud.yandex.ru/docs/billing/quickstart/#create_billing_account).

2. [Получите идентификатор](https://cloud.yandex.ru/docs/resource-manager/operations/folder/get-id) любого каталога, на который у вашего аккаунта есть роль editor или выше.

3. Получите OAuth-токен в сервисе Яндекс.OAuth. Как это сделать описано здесь: https://cloud.yandex.ru/docs/iam/concepts/authorization/oauth-token.

4. Необходимую информацию занесите в файл настроек speech.ini.

      

Для работы с озвучиванием текста используйте класс SpeechPerson. Данный класс - это как бы персона, которая обладает набором характеристик и от лица которой ведётся повествование на определённом языке и с определённым голосом.

Функции для работы:

- read_speech_config(filename) - Чтение файла конфигурации ini (см. ниже).
- get_iam_token(oauth_token) - Получение [IAM-токена](https://cloud.yandex.ru/docs/iam/concepts/authorization/iam-token) с помощью [OAuth-токена](https://cloud.yandex.ru/docs/iam/concepts/authorization/oauth-token). IAM-токен действует не больше 12 часов, но рекомендуется запрашивать новый токен чаще, например каждый час. 
- SpeechPerson.update_iam_token(oauth_token) - Обновление IAM-токена. См. функцию get_iam_token.
- SpeechPerson.synthesize(text, emotion='neutral', speed=1.0) - Синтезирование голоса. 
  - text - Текст, который нужно озвучить, в кодировке UTF-8.
  - emotion - Эмоциональная окраска голоса. Поддерживается только при выборе русского языка (ru-RU) и голосов jane или omazh. Допустимые значения: 
    - good — доброжелательный
    - evil — злой
    - neutral (по умолчанию) — нейтральный.
  - speed - Скорость (темп) синтезированной речи. Скорость речи задается дробным числом в диапазоне от 0.1 до 3.0.
- SpeechPerson.synthesize_to_file(filename, text, emotion='neutral', speed=1.0) - Синтезирование голоса и запись в файл с именем filename. Описание остальных полей см. в SpeechPerson.synthesize.

   

Чтобы озвучивание текста заработало, необходимо в конфигурационном файле поменять следующие параметры:

- oauth_token - OAuth-токен в сервисе Яндекс.OAuth. 

- folder_id - Идентификатор каталога, к которому у вас есть доступ.

- lang - Язык. Допустимые значения:

  - ru-RU (по умолчанию) — русский язык
  - en-US — английский язык
  - tr-TR — турецкий язык.

- voice - Желаемый голос для синтеза речи из [списка](https://cloud.yandex.ru/docs/speechkit/tts/voices). Значение параметра по умолчанию: oksana.

- format - Формат синтезируемого аудио. Допустимые значения:

  - oggopus (по умолчанию) — данные в аудиофайле кодируются с помощью аудиокодека OPUS и упаковываются в контейнер OGG (OggOpus).
  - lpcm — аудиофайл синтезируется в формате LPCM без WAV-заголовка. 

- sampleRateHertz - Частота дискретизации синтезируемого аудио. Применяется, если значение format равно lpcm. Допустимые значения:

  - 48000 (по умолчанию) — частота дискретизации 48 кГц
  - 16000 — частота дискретизации 16 кГц
  - 8000 — частота дискретизации 8 кГц.

     

Для интеграции в ваш проект, просто скопируйте папку YandexSpeech в свою директорию.

Пример кода:

```
from YandexSpeech import *
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
```

   

Для работы данного проекта дополнительно нужно установить следующие пакеты:

- Configparser

