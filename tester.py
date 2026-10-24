import requests
respone = {'CardID': 'A0V33R4P5D0',
         'Time': '2026-10-25 0:38:50'}
respone = requests.get('http://192.168.0.117:5000/open_box', params=respone)
print(respone.text)
print(respone.status_code)