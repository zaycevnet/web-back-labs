from flask import Blueprint, render_template, request,  make_response, redirect
lab3 = Blueprint('lab3', __name__)

# Каждый Blueprint имеет свои собственные маршруты (URLs), представления (views) и шаблоны. 
# После регистрации в основном приложении эти маршруты становятся частью вашего основного приложения Flask.

@lab3.route('/lab3/')
def lab():
    # name = request.cookies.get('name')
    # name_color = request.cookies.get ('name_color')
    # return render_template('lab3/lab3.html', name=name, name_color=name_color)
    name = request.cookies.get('name')
    if not name:  # Если куки "name" отсутствует
        name = 'аноним'

    name_color = request.cookies.get('name_color', '#000000')  # значение по умолчанию черное
    
    age = request.cookies.get('age')
    if not age:  # Если куки "age" отсутствует
        age = 'не указан'

    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    # return 'установка cookie', 200, {'Set-Cookie': 'name=Alex'}
    resp = make_response(redirect ('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

# В Flask объект Response представляет собой HTTP-ответ, который сервер отправляет клиенту (браузеру). Этот объект 
# содержит всю информацию об ответе: тело ответа 
# (данные), заголовки, статусный код и прочие параметры, которые определяют, как сервер взаимодействует с клиентом

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect ('/lab3/')) #Перенаправление говорит браузеру, что нужно перейти на страницу /lab3/ после установки куки
    resp.set_cookie('name')
    resp.set_cookie('age')
    resp.set_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1(): #Эта функция обрабатывает GET-запрос и проверяет наличие параметров
#     user = request.args.get('user')
#     age = request.args.get('age')
#     sex = request.args.get('sex')
#     return render_template('lab3/form1.html', user=user, age=age, sex=sex)

    errors = {}
    user = request.args.get('user') #пытается получить параметр user из строки запроса (например, ?user=Alex). Если параметр не передан, будет возвращено значение None
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Введите возвраст!'
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

# рендер для рендеринга (отображения) HTML-шаблонов и передачи в них данных.

# request.args в Flask предназначен для доступа к параметрам строки запроса, которые передаются в URL после знака ?. 
# Например, при запросе /lab3/form1?user=Alex&age=20 параметры user и age



@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    price = 0

    drink = request.args.get('drink')
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10    

    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    return render_template('lab3/success.html')

@lab3.route('/lab3/settings')
def settings():
    # Получаем параметры из запроса
    color = request.args.get('color')
    background_color = request.args.get('background_color')
    font_size = request.args.get('font_size')
    reset = request.args.get('reset')

    # Если параметр сброса передан, очищаем cookies
    if reset:
        resp = make_response(redirect('/lab3/settings'))
        resp.delete_cookie('color')
        resp.delete_cookie('background_color')
        resp.delete_cookie('font_size')
        return resp

    # Если переданы параметры, устанавливаем их в cookies и делаем редирект
    if color or background_color or font_size:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if background_color:
            resp.set_cookie('background_color', background_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        return resp

    # Если параметры не переданы, загружаем их из cookies
    color = request.cookies.get('color')
    background_color = request.cookies.get('background_color')
    font_size = request.cookies.get('font_size')

    # Рендерим шаблон с текущими значениями
    resp = make_response(render_template('lab3/settings.html', color=color, background_color=background_color, font_size=font_size))
    return resp

@lab3.route('/lab3/trail_ticket')
def trail_ticket():
    return render_template('lab3/trail_ticket.html')

@lab3.route('/lab3/ticket')
def ticket():
    passenger_name = request.args.get('passenger_name')
    passenger_type = request.args.get('passenger_type')
    berth_type = request.args.get('berth_type')
    luggage = request.args.get('luggage')
    insurance = request.args.get('insurance') 
    passenger_age_str = request.args.get('passenger_age')  
    departure_point = request.args.get('departure_point')
    destination = request.args.get('destination')
    travel_date = request.args.get('travel_date')

    # Проверяем, что возраст не пуст и является числом. isdigit() — это встроенный метод строк в Python, который проверяет, состоит ли строка полностью из цифр.
    if not passenger_age_str or not passenger_age_str.isdigit():
        return "Ошибка: Возраст должен быть числом", 400

    # Преобразуем возраст в целое число
    passenger_age = int(passenger_age_str)

    # Валидация возраста
    if not (1 <= passenger_age <= 120):
        return "Ошибка: Возраст должен быть от 1 до 120 лет", 400

    # Расчет стоимости
    if passenger_type == 'child' or passenger_age < 18:
        ticket_price = 700  # Детский билет
    else:
        ticket_price = 1000  # Взрослый билет

    # Доплата за нижнюю или нижнюю боковую полку
    if berth_type in ['lower', 'lower_side']:
        ticket_price += 100

    # Доплата за багаж
    if luggage == 'on':
        ticket_price += 250

    # Доплата за страховку
    if insurance == 'on':
        ticket_price += 150

    # Отображение страницы с билетом
    return render_template('lab3/ticket.html',
                           passenger_name=passenger_name,
                           passenger_type=passenger_type,
                           berth_type=berth_type,
                           luggage=luggage,
                           insurance=insurance,
                           passenger_age=passenger_age,
                           departure_point=departure_point,
                           destination=destination,
                           travel_date=travel_date,
                           ticket_price=ticket_price)