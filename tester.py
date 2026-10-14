import requests
respone = {'password': 'UNIkUm_adm-2023',
            'CardID': 'A0V33R4P5D0',
            'NameUser': 'Yaroslav Vselodovich',
            'Time': '2026-10-14 22:43:50'}
respone = requests.post('http://192.168.0.117:500/create_user', data=respone)
print(respone.text)
print(respone.status_code)