import requests
respone = {'password': 'XdjL2biYNKxzRd',
            'CardID': 'S0N4ED2F1D9',
            'NameUser': 'Ярослав Всевлодович',
            'Group': 'ИЭ82//VIP(для преподователей)',
            'Time': '2026-10-14 22:43:50',
            'act': 'add'}
respone = requests.post('http://192.168.0.117:5000/edit_user_list', json=respone)
print(respone.text)
print(respone.status_code)