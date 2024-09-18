from flask import Flask, url_for, redirect
app = Flask(__name__)

@app.errorhandler(404)
def not_found (err):
    return "Нет такой страницы =/", 404

@app.route("/")
@app.route("/web")
def web():
    return """<!doctype html>
        <html>
            <body>
                <h1>web-сервер на flask</h1>
                <p><a href="/author">/author</a></p>
                <p><a href="/labl/oak">Дуууб</a></p>
                <p><a href="/lab1/counter">Счетчик</a></p>
            </body>
        </html>""", 200, {
            "X-Server": "sample",
            'Content-Type': 'text/plain; charset=utf-8'
            }

@app.route("/author")
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
    </body>
</html>
'''
@app.route("/info")
def info():
    return redirect ("/author")

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