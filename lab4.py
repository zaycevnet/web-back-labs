from flask import Blueprint, render_template, request
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form/')
def div_form():
    return render_template('lab4/div-form.html')

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