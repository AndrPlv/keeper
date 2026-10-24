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

@app.route('/edit_accese', methods=['POST'])
def edit_accese():
    '''
        {'password': '*********',
         'NameUser': 'Пылов Андрей Константинович',
         'Group': 'ИЭ82//VIP(для преподователей)'
         'access': '0//1'}
    '''    
    requests = request.json
    if requests.get('password') == passwords['password_for_add_user']:
        level_access = requests['access']
        
        connect = sqlite3.connect('table.db')
        cursore = connect.cursor()

        if cursore.execute('SELECT id FROM card_to_user WHERE name_user = ? AND group_user = ?', [requests['NameUser'], requests['Group']]).fetchone():
            cursore.execute('UPDATE card_to_user SET access = (?) WHERE name_user = ? AND group_user = ?', [requests['access'], requests['NameUser'], requests['Group']])
            connect.commit()
            return {'status': 'good'}, 201
        else:
            return {'status': 'Not found the users'}     
        cursore.close()
        connect.close()                                                                                                                                                     
    return {'status': 'access denied'}, 403    

@app.route('/open_box', methods=['GET'])
def open_box():
    '''
        {'CardID': 'A0V33R4P5D0',
         'Time': 'y-m-d H:M:S'}
    '''

    data = request.args
    base = sqlite3.connect()
    cursore = base.cursor()

    
    if cursore.execute('SELECT id FROM card_to_user WHERE id_card = (?)', [data['CardID']]).fetchone():
        level = cursore.execute('SELECT access FROM card_to_user WHERE id_card = (?)', [data['CardID']])

    else:
        return {'status': 'Not found the user'}, 404
    
    name_user = ursore.execute('SELECT name_user FROM card_to_user WHERE id_card = (?)', [data['CardID']]).fetchone()
    name_user = ursore.execute('SELECT group_user FROM card_to_user WHERE id_card = (?)', [data['CardID']]).fetchone()   
    cursore.execute('INSERT INTO box_history(name_user, act, time, group_user) VALUES (?,?,?,?)', [name_user, 'get_access', request['Time']])
    base.commit()
    
    cursore.close()
    base.close()
    return {'open': level}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)