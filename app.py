from flask import Flask, url_for, redirect
app = Flask(__name__)

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

@app.route("/")
@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
            <body>
                <h1>web-сервер на flask</h1>
                <li><a href="/lab1/web">Первая лабораторная (web)</a></li>
                <li><a href="/lab1/author">Информация об авторе</a></li>
                <li><a href="/labl/oak">Изображение дуба</a></li>
                <li><a href="/lab1/counter">Счётчик</a></li>
                <li><a href="/lab1/reset">Очистить счётчик</a></li>
                <li><a href="/lab1">Описание Flask (Лабораторная 1)</a></li>
            </body>
        # </html>""" 
        # , 200, {
        #     "X-Server": "sample",
        #     'Content-Type': 'text/plain; charset=utf-8'
        #     }

@app.route("/lab1/author")
def author():
    name = "010595140"
    group = "ФБИ-21"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <p><a href="/web">web</a></p>
                <p><a href="/labl/oak">Дуууб</a></p>
            </body>
        </html>"""

@app.route('/labl/oak')
def oak():
    path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css")
    return '''
<!doctype html>
<html>
    <body>
    <h1>Дуууб</h1>
    <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    <img src="''' + path + '''">
    </body>
</html>
'''

def new_func():
    css_path = url_for("static", filename="lab1.css")

count = 0  # Инициализируем счетчик вне функции тк ошибка 500

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    return '''
<!doctype html>
<html>
    <body>
    Сколько раз вы сюда заходили: ''' + str(count) + '''
    <p><a href="/lab1/reset">Очистить счетчик</a></p>
    </body>
</html>
'''

@app.route("/lab1/info")
def info():
    return redirect ("/lab1/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
    <h1>Создано успешно</h1>
    <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201


@app.route('/lab1/reset')
def reset_counter():
    global count
    count = 0
    return '''
<!doctype html>
<html>
    <body>
    <h1>Счетчик был очищен</h1>
    <p><a href="/lab1/counter">Назад к счетчику</a></p>
    </body>
</html>
'''

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

@app.route("/lab1")
def lab1():
    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
        <link rel="stylesheet" type="text/css" href="''' + url_for("static", filename="lab1.css") + '''">
    </head>
    <body>
        <h1>Лабораторная 1</h1>
        <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
        <p><a href="/">Вернуться на главную</a></p>
    </body>
</html>
'''

@app.route("/error/400")
def error_400():
    return "400 Bad Request: Некорректный запрос", 400

@app.route("/error/401")
def error_401():
    return "401 Unauthorized: Неавторизован", 401

@app.route("/error/402")
def error_402():
    return "402 Payment Required: Требуется оплата", 402

@app.route("/error/403")
def error_403():
    return "403 Forbidden: Доступ запрещён", 403

@app.route("/error/405")
def error_405():
    return "405 Method Not Allowed: Метод не разрешён", 405

@app.route("/error/418")
def error_418():
    return "418", 418
