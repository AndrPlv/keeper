from flask import Flask, request, jsonify
from pandas import to_datetime
import json
import sqlite3

app = Flask(__name__)

with open('secret.json', 'r', encoding='UTF-8') as file:
    passwords = json.load(file)

@app.route('/create_user', methods=['POST'])
def get():
    requests = request.args.to_dict()
    if requests['password'] == passwords['GENERAL_PASSWRD']:
        base = sqlite3.connect("table.db")
        cursore = base.cursor()

        message = 'INSERT INTO card_to_user(id_card, name_user, time) VALUES (?,?,?)'

        cursore.execute(message, (requests['CardID'], requests['NameUser'], requests['Time']))
        base.commit()
        cursore.close()
        base.close()        
        return 'Good!', 201
    return 'INVALID password', 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=500, debug=True)