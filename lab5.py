from flask import Blueprint, url_for, redirect, render_template, request, make_response, session
# lab5 = Blueprint('lab5', __name__)
# import psycopg2
# from psycopg2.extras import RealDictCursor
# from werkzeug.security import check_password_hash, generate_password_hash
# @lab5.route('/lab5/')
# def lab():
#     return render_template('lab5/lab5.html', login=session.get('login'))

# def db_connect():
#     conn = psycopg2.connect(
#     host = '127.0.0.1',
#     database = 'ser_knowledge_base',
#     user = 'ser_knowledge_base',
#     password = '123')

#     cur = conn.cursor(cursor_factory=RealDictCursor)
#     return conn, cur

# def db_close(conn,cur):
#     conn.commit()
#     cur.close()
#     conn.close()

# @lab5.route('/lab5/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'GET':
#         return render_template('lab5/register.html')
    
#     conn, cur = db_connect()

#     login = request.form.get('login')
#     password = request.form.get('password')
#     cur.execute(f"SELECT login FROM users WHERE login = '{login}';")
#     if cur.fetchone():
#         return render_template('lab5/register.html',
#                                 error='Такой пользователь уже существует')

#     password_hash = generate_password_hash(password)
#     cur.execute(f"INSERT INTO users (login, password) VALUES ('{login}', '{password_hash}');")

#     return render_template('lab5/success.html', login=login)


# @lab5.route('/lab5/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('lab5/login.html')
    
#     login = request.form.get('login')
#     password = request.form.get('password')

#     conn, cur = db_connect()



#     cur.execute(f"SELECT * FROM users WHERE login='{login}';")
#     user = cur.fetchone()

#     if not user:
#         db_close(conn,cur)
#         return render_template('lab5/login.html', error='Логин и/или пароль неверны')
#     if not check_password_hash(user['password'], password):
#         db_close(conn,cur)
#         return render_template('lab5/login.html', error='Логин и/или пароль неверны')

#     session['login'] = login

#     db_close(conn,cur)
#     return render_template('lab5/succes_login.html', login=login)

from flask import Blueprint, render_template, request, session
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

def db_connect():
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='ser_knowledge_base',
        user='ser_knowledge_base',
        password='123'
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    conn, cur = db_connect()

    try:
        login = request.form.get('login')
        password = request.form.get('password')

        if not login or not password:
            return render_template('lab5/register.html', error='Логин и пароль обязательны')

        # Проверка на существование пользователя
        cur.execute("SELECT login FROM users WHERE login = %s;", (login,))
        if cur.fetchone():
            return render_template('lab5/register.html', error='Такой пользователь уже существует')

        # Хеширование пароля
        password_hash = generate_password_hash(password)

        # Вставка нового пользователя
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))

        return render_template('lab5/success.html', login=login)
    finally:
        db_close(conn, cur)

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/login.html', error='Логин и пароль обязательны')

    conn, cur = db_connect()

    try:
        # Поиск пользователя в базе
        cur.execute("SELECT * FROM users WHERE login = %s;", (login,))
        user = cur.fetchone()

        if not user or not check_password_hash(user['password'], password):
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')

        # Сохранение логина в сессии
        session['login'] = login
        return render_template('lab5/succes_login.html', login=login)
    finally:
        db_close(conn, cur)

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')


    title = request.form.get('title')
    article_text = request.form.get('article_text')

    conn, cur = db_connect()

    cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    login_id = cur.fetchone()["id"]

    cur.execute(f"INSERT INTO articles(user_id, title, article_text) VALUES ({login_id}, '{title}','{article_text}');")
    db_close(conn, cur)
    return redirect('/lab5')