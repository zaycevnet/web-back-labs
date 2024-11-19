from flask import Blueprint, render_template, request, session
import psycopg2
from psycopg2.extras import RealDictCursor
lab5 = Blueprint('lab5', __name__)

# app = Flask(__name__)

@lab5.route('/lab5/')
def lab():
        return render_template('lab5/lab5.html', login=session.get('login'))

# @lab5.route('/login')
# def login():
#     return render_template('login.html')

@lab5.route('/lab5/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template ('lab5/register.html', error = 'Заполни пж все поля')

    conn = psycopg2.connect(
    host='127.0.0.1',
    database='ser_knowledge_base',
    user='ser_knowledge_base',
    password='123'
    )
    cur = conn.cursor()
    cur.execute(f"SELECT login FROM users WHERE login='{login}';")
    if cur.fetchone():
        cur.close()
        conn.close()
        return render_template('lab5/register.html', error ='Такой пользователь уже существует')
    cur.execute(f"INSERT INTO users (login, password) VALUES ('{login}', '{password}');")
    conn.commit()
    cur.close()
    conn.close()
    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template ('lab5/login.html', error = 'Заполни пж все поля')
    conn = psycopg2.connect(
    host='127.0.0.1',
    database='ser_knowledge_base',
    user='ser_knowledge_base',
    password='123'
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(f"SELECT * FROM users WHERE login='{login}';")
    user = cur.fetchone()
    if not user:
        cur.close()
        conn.close()
        return render_template('lab5/login.html', error='логин и/или пароль неверны')

    if user['password'] != password:
        cur.close()
        conn.close()
        return render_template('lab5/login.html',  error='логин и/или пароль неверны')
    session['login'] = login
    cur.close()
    conn.close()
    return render_template('lab5/succes_login.html' , login=login)

