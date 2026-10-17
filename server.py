from flask import Flask, request, jsonify
from pandas import to_datetime
import json
import sqlite3

app = Flask(__name__)

with open('secret.json', 'r', encoding='UTF-8') as file:
    passwords = json.load(file)


@app.route('/edit_user_list', methods=['POST'])
def edit_user_list():
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

        user = cursore.execute('SELECT name_user FROM card_to_user WHERE id_card = ?;', [requests.get('CardID')]).fetchall()
        if not(bool(user)):
            if requests.get('act') == 'add':
                cursore.execute('INSERT INTO card_to_user(id_card, name_user, time, group_user) VALUES (?,?,?,?)', [requests.get('CardID'), requests.get('NameUser'), requests.get('Time'), requests.get('Group')])
            else:
                return {'status': 'Not found the user in SQL table'}, 404
        else:
            if requests.get('act') == 'del':            
                cursore.execute('DELETE FROM card_to_user WHERE id_card = ?', [requests.get('CardID')])
            else:
                return {'status': "I don't have this action"}, 400
        connect.commit()
        cursore.close()
        connect.close()
        return {'status': 'good'}, 201
    return {'status': 'access denied'}, 403

@app.route('/input_data', methods=['POST'])
def input_data():
    data = request.json

    base = sqlite3.connect


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)