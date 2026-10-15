from flask import Flask, request, jsonify
from pandas import to_datetime
import json
import sqlite3

app = Flask(__name__)

with open('secret.json', 'r', encoding='UTF-8') as file:
    passwords = json.load(file)


@app.route('/edit_user_list', methods=['POST'])
def create_user():
    '''
        {'password': '*********',
         'CardID': 'A0V33R4P5D0',
         'NameUser': 'Пылов Андрей Константинович',
         'Group': 'ИЭ82//VIP(для преподователей)'
         'Time': 'y-m-d h:m:s'
         'act': 'add//del'}
    '''
    requests = request.json
    if requests.get('password') == passwords['password_for_add_user']:
        connect = sqlite3.connect('table.db')
        cursore = connect.cursor()

        if not bool(cursore.execute('SELECT name_user FROM card_to_user WHERE id_card = ?', [requests.get('CardID')])) and requests.get('act') == 'del':
            return {'status': 'Not found the user'}, 404
        
        if requests.get('act') == 'del':
            pass
        elif request.get('act') == 'add':
            pass
        else:
            return {'status': "I don't have this action"}, 400

        cursore.close()
        connect.close()
        return {'status': 'good'}, 201
    return {'status': 'access denied'}, 403


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)