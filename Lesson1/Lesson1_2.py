
import requests
import json
main_link = 'https://translate.yandex.net'
text = 'Hello world'
appid = ''
link = f'{main_link}/api/v1.5/tr.json/translate?key={appid}&text={text}&lang=en-ru&format=html'
req = requests.get(link)

if req.ok:
    data = json.loads(req.text)
    print(f"Фраза на английском '{text}' переводится как '{data['text'][0]}'")
