import requests
import re
res = requests.get('http://myip.ru/index_small.php').text
ip = re.findall('\d+\.\d+\.\d+\.\d+', res)[0]
print(ip)
