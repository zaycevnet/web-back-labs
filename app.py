from flask import Flask, url_for, session, redirect,  render_template #Эта функция как раз и отвечает за рендеринг шаблонов (создание html-текста для браузера):
import os
from flask_sqlalchemy import SQLAlchemy
from db.models import users
from flask_login import LoginManager
from db import db
from os import path
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from lab9 import lab9
from zaycev_rgz import zaycev_rgz
app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(lab9)
app.register_blueprint(zaycev_rgz)
# app.secret_key = 'пароль'

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет') #Устанавливает секретный ключ приложения, используемый для безопасности
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres') #Определяет используемую базу данных

# Пытается получить переменную окружения SECRET_KEY с помощью метода os.environ.get.
# Если SECRET_KEY не установлена в окружении, по умолчанию будет использовано значение 'секретно-секретный секрет'.

#генерирует URL-адреса для маршрутов, для перенаправления 

if app.config['DB_TYPE'] == 'postgres':
    db_name = 'ser_orm'
    db_user = 'ser_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432
    options="-c client_encoding=UTF8"

    # Формирование строки подключения для PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__)) # Получаем текущую директорию файла
    db_path = path.join(dir_path, "ser.db")  # Формируем путь к файлу SQLite базы данных
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}' # Формирование строки подключения для SQLite

db.init_app(app) # Инициализация базы данных с текущим приложением Flask

@app.errorhandler(404)
def not_found(err):
    css_path = url_for("static", filename="lab1.css")
    img_path = url_for("static", filename="404_image.png")  # Путь к изображению в папке static
    return '''
<!doctype html>
<html>
    <head>
        <title>Ошибка 404 - Страница не найдена</title>
        <meta charset="UTF-8">
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body class="error-page">
        <h1>Ошибка 404 - Страница не найдена</h1>
        <p>Ой!</p>
        <img src="''' + img_path + '''" alt="404 ошибка">
        <p><a href="/">Вернуться на главную страницу</a></p>
    </body>
</html>
''', 404

 # rel="stylesheet" этот файл — таблица стилей, Flask сгенерирует полный URL для файла lab1.css из каталога static


@app.route("/")


@app.route("/index")
def index():
    css_path = url_for("static", filename="lab1.css")
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        <nav>
                <li><a href="/lab1/web">Первая лабораторная</a></li>
                <li><a href="/lab2/">Вторая лабораторная</a></li>
                <li><a href="/lab3/">Третья лабораторная</a></li>
                <li><a href="/lab4/">Четвёртая лабораторная</a></li>
                <li><a href="/lab5/">Пятая лабораторная</a></li>
                <li><a href="/lab6/">Шестая лабораторная</a></li>
                <li><a href="/lab7/">Седьмая лабораторная</a></li>
                <li><a href="/lab8/">Восьмая лабораторная</a></li>
                <li><a href="/lab9/">Девятая лабораторная</a></li>
        </nav>
        <footer>
            <p>ФИО: 010595140</p>
            <p>Группа: ФБИ-21</p>
            <p>Курс: 3</p>
            <p>Год: 2024</p>
        </footer>
    </body>
</html>
'''


@app.errorhandler(500)
def internal_server_error(err):
    css_path = url_for("static", filename="lab1.css")
    return '''
<!doctype html>
<html>
    <head>
        <title>Ошибка 500 - Внутренняя ошибка сервера</title>
        <meta charset="UTF-8">
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body class="error-page">
        <h1>Ошибка 500 - Внутренняя ошибка сервера</h1>
        <p>Ой.</p>
        <p><a href="/">Вернуться на главную страницу</a></p>
    </body>
</html>
''', 500

# from flask_migrate import Migrate

login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_users(login_id):
    return users.query.get(int(login_id))