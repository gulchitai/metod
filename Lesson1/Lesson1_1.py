import requests
import json
link = 'http://api.github.com/users/gulchitai/repos'
req = requests.get(link)

if req.ok:
    data = json.loads(req.text)
    for i in range(len(data)):
        print(data[i]['full_name'])
