from flask import Blueprint, render_template, redirect, request, session
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form/')
def div_form():
    return render_template('lab4/div-form.html')

#---------------------------------
@lab4.route('/lab4/add_form')
def add_form():
    return render_template('lab4/add_form.html')

@lab4.route('/lab4/sub_form')
def sub_form():
    return render_template('lab4/sub_form.html')

@lab4.route('/lab4/mul_form')
def mul_form():
    return render_template('lab4/mul_form.html')

@lab4.route('/lab4/pow_form')
def pow_form():
    return render_template('lab4/pow_form.html')

#-------------------------------------------

@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    # Проверяем, заполнены ли оба поля
    if x1 == "" or x2 == "":
        return render_template('lab4/div.html', x1=x1, x2=x2, result=None, error='Оба поля должны быть заполнены')

    try:
        # Преобразуем ввод в целые числа
        x1 = int(x1)
        x2 = int(x2)
        
        # Выполняем деление
        result = x1 / x2
    
    except ZeroDivisionError:
        # Обработка деления на ноль
        return render_template('lab4/div.html', x1=x1, x2=x2, result=None, error='Деление на ноль невозможно')

    # Возвращаем результат, если всё прошло успешно
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result, error=None)

# ---------------------------------------
@lab4.route('/lab4/add', methods=['POST'])
def add():
    x1 = request.form.get('x1') or '0'  # Пустое поле трактуется как 0
    x2 = request.form.get('x2') or '0'

    try:
        result = int(x1) + int(x2)
    except ValueError:
        return render_template('lab4/add.html', x1=x1, x2=x2, result=None, error='Ввод должен быть целыми числами')

    return render_template('lab4/add.html', x1=x1, x2=x2, result=result, error=None)


# --- Вычитание ---
@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == "" or x2 == "":
        return render_template('lab4/sub.html', x1=x1, x2=x2, result=None, error='Оба поля должны быть заполнены')

    result = int(x1) - int(x2)
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result, error=None)


# --- Умножение ---
@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1') or '1'  # Пустое поле трактуется как 1
    x2 = request.form.get('x2') or '1'
    result = int(x1) * int(x2)
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result, error=None)


# --- Возведение в степень ---
@lab4.route('/lab4/pow', methods=['POST'])
def pow_op():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == "" or x2 == "":
        return render_template('lab4/pow.html', x1=x1, x2=x2, result=None, error='Оба поля должны быть заполнены')

    try:
        x1 = int(x1)
        x2 = int(x2)

        if x1 == 0 and x2 == 0: #это ключевое слово, которое инициирует исключение.
            raise ValueError("0  0 не определено") 

        result = x1 ** x2
    except ValueError as e: #для обработки исключений типа ValueError и позволяет получить к ним доступ, чтобы понять, что пошло не так. 
        return render_template('lab4/pow.html', x1=x1, x2=x2, result=None, error=str(e))

    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result, error=None)

tree_count = 0

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count

    if request.method == 'POST':
        operation = request.form.get('operation')

        # Увеличиваем или уменьшаем счётчик с проверками
        if operation == 'cut' and tree_count > 0:
            tree_count -= 1
        elif operation == 'plant' and tree_count < 10:
            tree_count += 1

        # POST/Redirect/GET для предотвращения повторной отправки данных
        return redirect('/lab4/tree')
    return render_template('lab4/tree.html', tree_count=tree_count)

# Авторизация
realname1 = '' #хранит полное имя пользователя, чтобы можно было вывести его после авторизации
users = [
    {'login': 'alex', 'password': '123', 'sex': 'male', 'realname': 'Алексей Иванов'},
    {'login': 'bob', 'password': '555','sex': 'male', 'realname': 'Боб Тотов'},
    {'login': '111', 'password': '111', 'sex': 'male', 'realname': 'Владимир Красное солнышко'},
    {'login': '444', 'password': '444','sex': 'male', 'realname': '444 444'},
]

@lab4.route('/lab4/login',methods =['GET','POST'])
def login():
    if request.method == 'GET':
        if 'login' in session: #если пользователь уже авторизован
            authorized = True
            login = session['login'] #извлекает логин текущего пользователя.
            for user in users:
                if login == user['login']:
                    global realname1
                    realname1 = user['realname']
        else:
            authorized = False
            login = ''
            realname1 = ''
        return render_template('lab4/login.html', authorized=authorized, realname=realname1)

    login = request.form.get('login')
    password = request.form.get('password')

    for user in users: #Если есть совпадение, логин сохраняется в session['login'], что создаёт сессию для пользователя
        if login == user['login'] and password == user['password']:
            session['login'] = login
            return redirect('/lab4/login')

    error = 'Неверный логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False, login=login)

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None) #удаляет логин пользователя из сессии, что означает завершение авторизации
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge/', methods = ['GET', 'POST'])
def fridge():
    temperature = request.form.get('temperature')
    message = ""

    if request.method == 'POST':
        if not temperature:
            message = "Ошибка: не задана температура"
        else:
            temperature = int(temperature)
            if temperature < -12:
                message = "Не удалось установить температуру — слишком низкое значение"
            elif temperature > -1:
                message = "Не удалось установить температуру — слишком высокое значение"
            elif -12 <= temperature <= -9:
                message = f"Установлена температура: {temperature}°С" + "❄️❄️❄️"
            elif -8 <= temperature <= -5:
                message = f"Установлена температура: {temperature}°С" + "❄️❄️"
            elif -4 <= temperature <= -1:
                message = f"Установлена температура: {temperature}°С" + "❄️"

    return render_template('lab4/fridge.html', message=message, temperature=temperature)

# Заказ зерна-------------------------------------------------------
@lab4.route('/lab4/ordergrain/', methods=['GET', 'POST'])
def order_grain():
    if request.method == 'POST':
        grain = request.form.get('grain')
        weight = request.form.get('weight')

        if not weight:
            error = 'Ошибка: не введен вес'
            return render_template('ordergrain.html', error=error)

        weight = float(weight) #Конвертация веса в число
        price_per_ton = {
            'ячмень': 12345,
            'овёс': 8522,
            'пшеница': 8722,
            'рожь': 14111
        }


        price = price_per_ton[grain] * weight

        if weight > 50:
            discount = 0.1 * price
            price -= discount
            discount_message = 'Применена скидка за большой объем.'
        else:
            discount_message = ''


        if weight > 500:
            error = 'Извините, такого объема сейчас нет в наличии.'
            return render_template('lab4/order_grain.html', error=error)

        if weight <= 0:
            error = 'Ошибка: введен недопустимый вес'
            return render_template('lab4/order_grain.html', error=error)

        message = f'Заказ успешно сформирован. Вы заказали {grain}. Вес: {weight} т. Сумма к оплате: {price} руб. {discount_message}'


        return render_template('lab4/order_grain.html', message=message)

    return render_template('lab4/order_grain.html')