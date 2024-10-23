from flask import Blueprint, render_template, request,  make_response, redirect
lab3 = Blueprint('lab3', __name__)


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


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect ('/lab3/'))
    resp.set_cookie('name')
    resp.set_cookie('age')
    resp.set_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
#     user = request.args.get('user')
#     age = request.args.get('age')
#     sex = request.args.get('sex')
#     return render_template('lab3/form1.html', user=user, age=age, sex=sex)

    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Введите возвраст!'
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

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