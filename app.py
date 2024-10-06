from flask import Flask, url_for, redirect,  render_template #Эта функция как раз и отвечает за рендеринг шаблонов (создание html-текста для браузера):
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

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка'] #в () кортеж только для чтения, в [] список

@app.route("/lab2/flowers/<int:flower_id>")
def flowers(flower_id):
    # return "id=" + str(flower_id)
    if flower_id >= len(flower_list): #длина кортежа в данный момент равна 3, нумерация с 0
        return '''
        <!doctype html>
        <html>    
            <body>
                <h1>Ошибка 404</h1>
                <p>Такого цветка нет</p>
                <a href="/lab2/flowers">Посмотреть все цветы</a>
            </body>
        </html>
        ''', 404
    else:
        flower_name = flower_list[flower_id]
        return f'''
        <!doctype html>
        <html>    
            <body>
                <h1>Информация о цветке</h1>
                <p>Название цветка: {flower_name}</p>
                <a href="/lab2/flowers">Посмотреть все цветы</a>
            </body>
        </html>
        '''
    
@app.route("/lab2/add_flower/<name>") #по умолчанию для него задаётся тип string (строка)
def add_flower(name):
    flower_list.append(name) #добавление имени цветка к общему списку, # сл строка: вывод нового имени в браузер
#     return ''' 
# <!doctype html>
# <html>    
#     <body>
#         <h1>Добавлен новый цветок</h1>
#         <p>Название нового цветка: ''' + name + '''</p>
#         </body>
# </html>
# '''
# во-вторых, в такие строки можно вставлять значения переменных напрямую, не нужна конкатенация, 
# всего лишь надо переменную обрамить фигурными скобками
    return f''' 
    <!doctype html>
    <html>    
        <body>
            <h1>Добавлен новый цветок</h1>
            <p>Название нового цветка: {name}</p>
            <p>Всего цветов: {len(flower_list)}</p>
            <p>Полный список: {flower_list}</p>
            </body>
    </html>
    '''
@app.route("/lab2/add_flower/")
def add_flower_no_name():
    return '''
    <!doctype html>
    <html>    
        <body>
            <h1>Ошибка 400</h1>
            <p>Вы не задали имя цветка</p>
            <a href="/lab2/flowers">Посмотреть все цветы</a>
        </body>
    </html>
    ''', 400

# Обработчик для вывода всех цветов
@app.route("/lab2/flowers")
def show_flowers():
    return f'''
    <!doctype html>
    <html>    
        <body>
            <h1>Список всех цветов</h1>
            <p>Всего цветов: {len(flower_list)}</p>
            <ul>
                {''.join([f'<li>{flower}</li>' for flower in flower_list])}
            </ul>
            <a href="/lab2/add_flower/">Добавить цветок</a>
        </body>
    </html>
    '''
@app.route("/lab2/clear_flowers")
def clear_flowers():
    flower_list.clear()  # Очищаем список полностью
    return '''
    <!doctype html>
    <html>    
        <body>
            <h1>Список цветов очищен</h1>
            <a href="/lab2/flowers">Посмотреть все цветы</a>
        </body>
    </html>
    '''



@app.route("/lab2/example")
def example():
    name  = '010595140' # student — переменная, используемая в коде на питоне, name — переменная в шаблоне. Это две разные сущности.
    kurs = '3'
    nomer_lab = '2'
    fruits = [
        {'name' : 'яблоки', 'price' : 100},
        {'name' : 'груши', 'price' : 120},
        {'name' : 'апельсины', 'price' : 80},
        {'name' : 'мандарины', 'price' : 95},
        {'name' : 'манго', 'price' : 321}
        ]
    return render_template ('example.html', name=name, kurs=kurs, nomer_lab=nomer_lab, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase ="О <b>сколько</b> <u>там</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)


@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
        # Выполняем операции
        addition = a + b
        subtraction = a - b
        multiplication = a * b
        division = a / b if b != 0 else "Деление на ноль невозможно"
        exponentiation = a ** b
        
        # Возвращаем результат в HTML
        return f'''
        <!doctype html>
        <html>    
            <body>
                <h1>Результаты математических операций</h1>
                <p>Суммирование: {a} + {b} = {addition}</p>
                <p>Вычитание: {a} - {b} = {subtraction}</p>
                <p>Умножение: {a} * {b} = {multiplication}</p>
                <p>Деление: {a} / {b} = {division}</p>
                <p>Возведение в степень: {a}  <sup>{b}</sup> = {exponentiation}</p>
            </body>
        </html>
        '''

@app.route('/lab2/calc/')
def calc_default():
    # Перенаправление на адрес /lab2/calc/1/1
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>')
def calc_redirect(a):
    # Перенаправление на адрес /lab2/calc/a/1
    return redirect(f'/lab2/calc/{a}/1')

#Задание 3
# Список книг
books = [
    {'author': 'Фёдор Достоевский', 'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 671},
    {'author': 'Лев Толстой', 'title': 'Война и мир', 'genre': 'Роман', 'pages': 1225},
    {'author': 'Джордж Оруэлл', 'title': '1984', 'genre': 'Антиутопия', 'pages': 328},
    {'author': 'Михаил Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Фантастика', 'pages': 480},
    {'author': 'Александр Пушкин', 'title': 'Евгений Онегин', 'genre': 'Поэма', 'pages': 320},
    {'author': 'Даниэль Дефо', 'title': 'Робинзон Крузо', 'genre': 'Приключения', 'pages': 256},
    {'author': 'Джек Лондон', 'title': 'Мартин Иден', 'genre': 'Роман', 'pages': 431},
    {'author': 'Артур Конан Дойл', 'title': 'Шерлок Холмс', 'genre': 'Детектив', 'pages': 302},
    {'author': 'Рей Брэдбери', 'title': '451 градус по Фаренгейту', 'genre': 'Фантастика', 'pages': 249},
    {'author': 'Габриэль', 'title': 'Сто лет одиночества', 'genre': 'Магический реализм', 'pages': 417}
]

# Маршрут для вывода списка книг
@app.route('/lab2/books')
def show_books():
    return render_template('books.html', books=books)

#Задание 4
# Список объектов
objects = [
    {
        'name': 'Клубника',
        'description': 'Вкусная и сочная летняя ягода.',
        'image': 'strawberry.jpg'
    },
    {
        'name': 'Машина',
        'description': 'Скоростной автомобиль спортивного класса.',
        'image': 'car.jpg'
    },
    {
        'name': 'Котик',
        'description': 'Милый домашний питомец.',
        'image': 'cat.jpg'
    },
    {
        'name': 'Стул',
        'description': 'Удобная мебель для сидения.',
        'image': 'chair.jpg'
    },
    {
        'name': 'Собака',
        'description': 'Преданный друг человека.',
        'image': 'dog.jpg'
    }
]

# Маршрут для отображения объектов
@app.route('/lab2/objects')
def show_objects():
    # Генерация путей к изображениям внутри маршрута
    for obj in objects:
        obj['image'] = url_for('static', filename=obj['image'])

    return render_template('objects.html', objects=objects)
