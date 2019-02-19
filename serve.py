#!/usr/bin/env python3

from flask import Flask
from flask import make_response, render_template, request, abort
import sqlite3


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index_page():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('SELECT `id`, `MAC_Addr`, `Computer_Name`, `Current_User_Name` from fields')
    computers = cur.fetchall()

    return render_template('index.html', computers=computers)


@app.route('/details', methods=['GET'])
def details_page():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    id = request.args.get('id')

    if id is None:
        abort(404)

    cur.execute('SELECT * from `fields` where `id`=?', (id,))
    details = cur.fetchone()

    if details is None:
        abort(404)

    details = details[1:]

    with open('NEEDED FIELDS.txt') as f:
        data = f.read().strip().split('\n')
        fields = [field for field in data if not field.startswith('[')]

    return render_template('details.html', details=zip(fields, details))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
