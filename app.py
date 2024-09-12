from flask import Flask, url_for
app = Flask(__name__)
@app.route("/")
@app.route("/web")
def web():
    return """<!doctype html>
        <html>
            <body>
                <h1>web-сервер на flask</h1>
                <p><a href="/author">/author</a></p>
                <p><a href="/labl/oak">Дуууб</a></p>
            </body>
        </html>"""

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
    path = url_for ("static", filename="oak.jpg")
    return '''
<!doctype html>
<html>
    <body>
    <h1>Дуууб</h1>
    <img src="''' + path +'''">
    </body>
</html>
'''