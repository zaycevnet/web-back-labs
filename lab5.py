from flask import Blueprint, render_template, request
import psycopg2
lab5 = Blueprint('lab5', __name__)

# app = Flask(__name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', username="anonymous")

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

# @lab5.route('/list')
# def list_articles():
#     return render_template('list.html')

# @lab5.route('/create')
# def create_article():
#     return render_template('create.html')

