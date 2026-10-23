import requests
respone = {'password': 'XdjL2biYNKxzRd',
         'NameUser': 'Liza Shiman',
         'Group': 'ИЭ9',
         'access': '0'}
respone = requests.post('http://192.168.0.117:5000/edit_accese', json=respone)
print(respone.text)
print(respone.status_code)