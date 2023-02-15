import requests
from flask import Flask, render_template, request
import psycopg2
import settings

app = Flask(__name__)
conn = psycopg2.connect(database='service_db',
                        user=settings.db_login,
                        password=settings.db_password,
                        host='localhost',
                        port='5432')

cursor = conn.cursor()


@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    if username == "":
        return render_template('login.html', error_msg='Enter username')
    password = request.form.get('password')
    if password == "":
        return render_template('login.html', error_msg='Enter password')
    cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", [str(username), str(password)])
    records = list(cursor.fetchall())
    if len(records) == 0:
        return render_template('login.html', error_msg='Incorrect username or password')
    print(records)
    return render_template('account.html', full_name=records[0][1], username=records[0][2], password=records[0][3])
