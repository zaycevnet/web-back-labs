from flask import Blueprint, url_for, redirect, render_template
lab2 = Blueprint('lab2', __name__)


@lab2.route("/lab2/a/")
def a():
    return 'слеш'


@lab2.route("/lab2/a")
def a2():
    return 'без слеша'


flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка'] #в () кортеж только для чтения, в [] список


@lab2.route("/lab2/flowers/<int:flower_id>")
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
    

@lab2.route("/lab2/add_flower/<name>") #по умолчанию для него задаётся тип string (строка)
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
# во-вторых, в такие строки можно вставлять значения переменных напрямую, не нужна конкатенация (сцепление строк), 
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


@lab2.route("/lab2/add_flower/")
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

# Обработчик для вывода всех цветов,  список HTML-элементов <li> для каждого цветка из списка flower_list
#Метод join() используется для объединения элементов и создания единой строки. Он берёт список строк и соединяет 
# их, используя указанный разделитель (в данном случае — пустая строка '')
#f - способ вставлять значения переменных или выражений прямо внутрь строки,


@lab2.route("/lab2/flowers")
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


@lab2.route("/lab2/clear_flowers")
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


@lab2.route("/lab2/example")
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


#Flask ищет файл example.html в папке templates
@lab2.route('/lab2/')
def lab():
    return render_template('lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase ="О <b>сколько</b> <u>там</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)


@lab2.route('/lab2/calc/<int:a>/<int:b>')
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


@lab2.route('/lab2/calc/')
def calc_default():
    # Перенаправление на адрес /lab2/calc/1/1
    return redirect('/lab2/calc/1/1')


@lab2.route('/lab2/calc/<int:a>')
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
@lab2.route('/lab2/books')
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
@lab2.route('/lab2/objects')
def show_objects():
    # Генерация путей к изображениям внутри маршрута
    for obj in objects:
        obj['image'] = url_for('static', filename=obj['image'])

    return render_template('objects.html', objects=objects)


#В квадратных скобках [] указывается ключ, по которому нужно получить соответствующее значение
#obj — это переменная, которая ссылается на словарь