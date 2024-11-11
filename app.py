from flask import Flask, url_for, session, redirect,  render_template #Эта функция как раз и отвечает за рендеринг шаблонов (создание html-текста для браузера):
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.secret_key = 'пароль'
#генерирует URL-адреса для маршрутов, для перенаправления 


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

