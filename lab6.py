from flask import Blueprint, render_template, request, session
lab6 = Blueprint('lab6', __name__)


offices = [] #Каждый офис — это словарь с номером, арендатором и ценой аренды
for i in range(1,11):
    offices.append({"number": i, "tenant": "", "price": 1000})


@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')


#этот маршрут обрабатывает запросы, которые приходят к серверу в формате JSON (это и есть API)
@lab6.route('/lab6/json-rpc-api/', methods=['POST']) #Метод POST используется для получения данных от клиента
def api():
    data = request.json # Получаем данные из запроса в формате JSON
    id = data['id'] # Извлекаем ID запроса, который нужен для ответа
    if data['method'] == 'info': # Если в методе запроса указано 'info'
        return {
            'jsonrpc': '2.0',
            'result': offices, # Отправляем список офисов
            'id': id # Возвращаем ID запроса
        }

    login = session.get('login')
    if not login: # Если пользователя нет в сессии, возвращаем ошибку авторизации
        return {
            'jsonrpc': '2.0',
            'error':{
                'code': 1, # Код ошибки "Неавторизован"
                'message': 'Unauthorized'
            }
        }

    if data['method'] == 'price': #получение суммы стоимости аренды всех офисов для текущего пользователя
        if not login:
            return{
                'jsonrpc': '2.0',
                'error':{
                'code': 1,
                'message': 'Unauthorized'
            },
                'id': id
            }
        priceofend = 0 # Инициализируем переменную для подсчета общей стоимости аренды
        for office in offices: # Проходим по списку офисов и суммируем стоимость аренды для офисов, арендованных текущим пользователем
            if office['tenant'] == login:
                priceofend = priceofend+office['price']

        return{
            'jsonrpc': '2.0',
            'priceofend': priceofend, # Отправляем общую стоимость аренды
            'id': id
        }
    
    if data['method'] == 'booking': # Обработка метода 'booking' — бронирование офиса
        office_number = data['params'] # Получаем номер офиса из параметров запроса
        for office in offices:
            if office['number'] == office_number:
                # Если офис уже забронирован, отправляем ошибку
                if office['tenant'] != '':
                    return{
                        'jsonrpc': '2.0',
                        'error':{
                            'code': 2,
                            'message': 'Alredy booked'
                        },
                        'id': id
                    }
                office['tenant'] = login # Если офис свободен, бронируем его за текущим пользователем
                return {
                    'jsonrpc': '2.0',
                    'result': 'succes',
                    'id': id
                }
    if data['method'] == 'cancellation':
        office_number = data['params']
        for office in offices:  # Проходим по списку офисов и ищем нужный офис по номеру
            if office['number'] == office_number:
                # Если офис не был забронирован, возвращаем ошибку
                if office['tenant'] == '':
                    return {
                        'jsonroc': '2.0',
                        'error':{
                            'code': 3,
                            'message': 'Not booked'
                        },
                        'id': id
                    }
                if not login: # Если логин не найден в сессии, отправляем ошибку авторизации
                    return{
                        'jsonrpc': '2.0',
                        'error':{
                        'code': 1,
                        'message': 'Unauthorized'
                    }
                    }
                if office['tenant'] != login: # Если текущий пользователь не является арендатором этого офиса, возвращаем ошибку
                    return{
                        'jsonroc': '2.0',
                        'error':{
                            'code': 4,
                            'message': 'You cannot'
                        },
                        'id': id
                    }
                office['tenant'] = '' # Если все проверки прошли, освобождаем офис
                return {
                    'jsonrpc': '2.0',
                    'result': 'succes',
                    'id': id
                }
            
    return { # Если метод не найден, возвращаем ошибку "Метод не найден"
        'jsonrpc': '2.0',
        'error':{
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }