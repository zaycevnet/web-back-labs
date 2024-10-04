from flask import Flask, url_for, redirect 
app = Flask(__name__)
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
@app.route("/lab1/web")
def web():
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
        
        <h2>Список роутов</h2>
        <ul>
            <li><a href="/">Главная страница</a></li>
            <li><a href="/lab1">Описание Flask (Лабораторная 1)</a></li>
            <li><a href="/lab1/web">Первая лабораторная (web)</a></li>
            <li><a href="/lab1/author">Информация об авторе</a></li>
            <li><a href="/labl/oak">Изображение дуба</a></li>
            <li><a href="/lab1/counter">Счётчик</a></li>
            <li><a href="/lab1/reset">Очистить счётчик</a></li>
            <li><a href="/lab1/info">Перенаправление на автора</a></li>
            <li><a href="/lab1/created">Создано успешно</a></li>
            <li><a href="/lab1/story">Фрагмент из романа "Мы"</a></li>
        </ul>
        
        <p><a href="/">Вернуться на главную</a></p>
    </body>
</html>
'''

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
def oak(): #файлы из папки static
    path = url_for("static", filename="oak.jpg") #URL для изображения
    css_path = url_for("static", filename="lab1.css") #URL для подключения CSS-файла
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
    global count #тк используется между различными HTTP-запросами
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

@app.route("/error/500")
def error_500():
    # Намеренная ошибка
    return 1 / 0

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

@app.route("/lab1/story")
def story():
    css_path = url_for("static", filename="lab1.css")
    img_path = url_for("static", filename="story_image.jpg") 
    return '''
<!doctype html>
<html>
    <head>
        <title>Фрагмент из романа Замятина "Мы"</title>
        <meta charset="UTF-8">
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Фрагмент из романа "Мы"</h1>
        <p>"Да, конечно, это я, я! Вчера это было так же ясно, как теперь ясно, что передо мной — этот лист бумаги. Тогда почему я сказал — «он»? И вообще, о чем я вчера говорил? Или — говорил?</p>
        <p>Сквозь головокружение, как в тумане, тускло светилось: она ведь говорила о любви. А я... Или не говорил? Нет, это не так. Я ясно помню: говорил, но не помню, о чем."</p>
        <p>Новый абзац</p>
        <img src="''' + img_path + '''" alt="Фрагмент из романа Мы">
    </body>
</html>
''', 200, {
        'Content-Language': 'ru',  # Язык страницы, стандартный заголовок
        'X-Developer': 'Student 010595140',  # Нестандартный заголовок
        'X-Course': 'Web Programming, Part 2'  # Нестандартный заголовок
    }


@app.route("/lab2/a/")
def a():
    return 'слеш'

@app.route("/lab2/a")
def a2():
    return 'без слеша'

flower_list = ('роза', 'тюльпан', 'незабудка', 'ромашка')

@app.route("/lab2/flowers/<int:flower_id>")
def flowers(flower_id):
    # return "id=" + str(flower_id)
    if flower_id >= len(flower_list): #длина кортежа в данный момент равна 3, нумерация с 0
        return "такого цветка нет", 404
    else:
        return "цветок: " + flower_list[flower_id]