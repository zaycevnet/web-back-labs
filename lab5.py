from flask import Blueprint, url_for, redirect, render_template, request, make_response, session, current_app
import sqlite3
from os import path #для работы с файловыми путями. Полезно при работе с локальными файлами базы данных, например, SQLite
lab5 = Blueprint('lab5', __name__)
import psycopg2 #для подключения и взаимодействия с PostgreSQL.

from psycopg2.extras import RealDictCursor #Импорт специального курсора RealDictCursor. 
#Этот курсор возвращает строки базы данных как словари (dict), где ключами являются названия колонок, а значениями — данные

from werkzeug.security import check_password_hash, generate_password_hash
#одна Хэширует пароли перед их сохранением в базе данных для безопасности, другая проверяет

# conn: Подключение к базе данных.
# cur: Курсор, используемый для выполнения запросов.

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login')) #session.get('login'): Проверяет, есть ли сохранённый логин пользователя в сессии.

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres': #Если это postgres, подключается PostgreSQL
        conn = psycopg2.connect(
        host = '127.0.0.1',
        database = 'ser_knowledge_base', ## Имя базы данных
        user = 'ser_knowledge_base',
        password = '123')
        cur = conn.cursor(cursor_factory=RealDictCursor) # Используем курсор RealDictCursor для возврата результатов как словарей
    else: #Если это что-то другое (или по умолчанию), используется SQLite
        dir_path = path.dirname(path.realpath(__file__)) # Получаем текущую директорию файла
        db_path = path.join(dir_path, "database.db") # Путь к файлу базы данных
        conn = sqlite3.connect(db_path) # Подключаемся к SQLite
        conn.row_factory = sqlite3.Row # Возвращаем строки как словари
        cur = conn.cursor() # Создаём курсор для выполнения запросов
    return conn, cur # Возвращаем подключение и курсор

def db_close(conn,cur):
    conn.commit() # Сохраняем все изменения в базе данных
    cur.close() # Закрываем курсор
    conn.close() # Закрываем подключение к базе данных


@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    conn, cur = db_connect() #подключается к базе данных (PostgreSQL или SQLite) и возвращает:conn: Подключение. cur: Курсор для выполнения SQL-запросов.

    login = request.form.get('login') #Данные из отправленной формы (POST) извлекаются с помощью
    password = request.form.get('password')

    if current_app.config['DB_TYPE'] == 'postgres': #для проверки, существует ли пользователь с указанным логином
        cur.execute(f"SELECT login FROM users WHERE login = %s;", (login,)) #В PostgreSQL используется %s как параметр подстановки.
    else: 
        cur.execute(f"SELECT login FROM users WHERE login = ?;", (login,)) #В SQLite используется ?
    if cur.fetchone(): #Если запрос возвращает строку (т.е. пользователь найден)
        db_close(conn,cur) #соединение закрывается
        return render_template('lab5/register.html',
                                error='Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password)

    if current_app.config['DB_TYPE'] == 'postgres': #Добавление нового пользователя
        cur.execute(f"INSERT INTO users (login, password) VALUES (%s, %s);", (login,password_hash))
    else:
        cur.execute(f"INSERT INTO users (login, password) VALUES (?, ?);", (login,password_hash))
    db_close(conn,cur)
    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None) # Удаление логина из сессии
    return redirect('/lab5') # Перенаправление на главную страницу модуля lab5

@lab5.route('/lab5/login', methods=['GET', 'POST'])
# GET: Отображает страницу с формой для ввода логина и пароля.
# POST: Обрабатывает данные, отправленные пользователем, проверяет логин и пароль.

def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    conn, cur = db_connect() #Подключается к базе данных

    if current_app.config['DB_TYPE'] == 'postgres': #SQL-запрос ищет пользователя с указанным логином в таблице users
        cur.execute(f"SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute(f"SELECT * FROM users WHERE login=?;", (login,))
    user = cur.fetchone() #Возвращает первую найденную строку, если пользователь существует. Возвращает None, если пользователь с таким логином не найден.

    if not user: #Если пользователь с таким логином не найден, база данных закрывается
        db_close(conn,cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')
    
    if not check_password_hash(user['password'], password): #Если пароли не совпадают
        db_close(conn,cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')
    
    session['login'] = login #В сессии сохраняется логин пользователя
    db_close(conn,cur) #Подключение к базе данных закрывается.
    return render_template('lab5/succes_login.html', login=login)


@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login') #Проверяет, авторизован ли пользователь (логин сохранён в сессии)
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title') #Данные заголовка из формы извлекаются
    article_text = request.form.get('article_text') #Данные статьи из формы извлекаются

    conn, cur = db_connect() #Создаётся подключение к базе данных

    if current_app.config['DB_TYPE'] == 'postgres': #Выполняется запрос для получения информации о пользователе по его логину.
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    login_id = cur.fetchone()["id"] #Возвращает первую найденную строку

    if current_app.config['DB_TYPE'] == 'postgres': #Вставляет данные о статье в таблицу articles
        cur.execute(f"INSERT INTO articles(user_id, title, article_text) VALUES (%s, %s, %s);", (login_id, title, article_text))
    else:
        cur.execute(f"INSERT INTO articles(login_id, title, article_text) VALUES (?, ?, ?);", (login_id, title, article_text))
    db_close(conn, cur) #Сохраняет изменения и закрывает подключение к базе данных
    return redirect('/lab5')

@lab5.route('/lab5/list')
def list():
    login = session.get('login') #Проверяет, авторизован ли пользователь (логин сохранён в сессии)
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect() #Подключается к базе данных

    if current_app.config['DB_TYPE'] == 'postgres': #Выполняется SQL-запрос для получения ID текущего пользователя
        cur.execute(f"SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute(f"SELECT id FROM users WHERE login=?;", (login,))
    login_id = cur.fetchone()['id']

    if current_app.config['DB_TYPE'] == 'postgres': #Выполняется SQL-запрос для получения всех статей, связанных с текущим пользователем
        cur.execute(f"SELECT * FROM articles WHERE user_id=%s;", (login_id,))
    else:
        cur.execute(f"SELECT * FROM articles WHERE login_id=?;", (login_id,))
    articles = cur.fetchall()

    db_close(conn, cur) #Закрывается подключение и курсор
    return render_template('lab5/list.html', articles=articles)


@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login') #Проверяет, авторизован ли пользователь.
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    
    # Получаем id пользователя для проверки, что он является владельцем статьи
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user_id = cur.fetchone()['id']

    # Получаем статью для редактирования
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
    else:
        cur.execute("SELECT * FROM articles WHERE id=? AND login_id=?;", (article_id, user_id))
    article = cur.fetchone()

    # Если статья не найдена или не принадлежит пользователю
    if article is None:
        return redirect('/lab5/list')

    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('article_text')

        # Валидация данных
        if not title or not article_text:
            return render_template('lab5/edit_article.html', article=article, error='Заполните все поля')

        # Обновление статьи
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE articles SET title=%s, article_text=%s WHERE id=%s;", (title, article_text, article_id))
        else:
            cur.execute("UPDATE articles SET title=?, article_text=? WHERE id=?;", (title, article_text, article_id))
        
        db_close(conn, cur)

        return redirect('/lab5/list')

    db_close(conn, cur)
    return render_template('lab5/edit_article.html', article=article)

@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    login = session.get('login') #Проверяет, авторизован ли пользователь (логин сохранён в сессии).
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres': #Выполняется SQL-запрос для получения ID текущего пользователя на основе его логина.
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user_id = cur.fetchone()['id']

    if current_app.config['DB_TYPE'] == 'postgres': #SQL-запрос удаляет статью из таблицы articles: Удаляет только ту статью, которая принадлежит текущему пользователю (user_id
        cur.execute("DELETE FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
    else:
        cur.execute("DELETE FROM articles WHERE id=? AND login_id=?;", (article_id, user_id))
    
    db_close(conn, cur) #Сохраняет изменения и закрывает подключение к базе данных.
    return redirect('/lab5/list')