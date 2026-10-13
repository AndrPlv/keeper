from flask import Flask, jsonify
import sqlite3

app = Flask()

@app.route('/')
def main():
    return 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=500, debug=True)