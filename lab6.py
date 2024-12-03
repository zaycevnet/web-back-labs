from flask import Blueprint, render_template, request, session
lab6 = Blueprint('lab6', __name__)


offices = []
for i in range(1,11):
    offices.append({"number": i, "tenant": "", "price": 900+i%3})


@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    if data['method'] == 'info':
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }

    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error':{
                'code': 1,
                'message': 'Unauthorized'
            }
        }

    if data['method'] == 'price':
        if not login:
            return{
                'jsonrpc': '2.0',
                'error':{
                'code': 1,
                'message': 'Unauthorized'
            },
                'id': id
            }
        endprice = 0
        for office in offices:
            if office['tenant'] == login:
                endprice = endprice+office['price']

        return{
            'jsonrpc': '2.0',
            'endprice': endprice,
            'id': id
        }
    
    if data['method'] == 'booking':
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] != '':
                    return{
                        'jsonrpc': '2.0',
                        'error':{
                            'code': 2,
                            'message': 'Alredy booked'
                        },
                        'id': id
                    }
                office['tenant'] = login
                return {
                    'jsonrpc': '2.0',
                    'result': 'succes',
                    'id': id
                }
    if data['method'] == 'cancellation':
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] == '':
                    return {
                        'jsonroc': '2.0',
                        'error':{
                            'code': 3,
                            'message': 'Not booked'
                        },
                        'id': id
                    }
                if not login:
                    return{
                        'jsonrpc': '2.0',
                        'error':{
                        'code': 1,
                        'message': 'Unauthorized'
                    }
                    }
                if office['tenant'] != login:
                    return{
                        'jsonroc': '2.0',
                        'error':{
                            'code': 4,
                            'message': 'You cannot'
                        },
                        'id': id
                    }
                office['tenant'] = ''
                return {
                    'jsonrpc': '2.0',
                    'result': 'succes',
                    'id': id
                }
            
    return {
        'jsonrpc': '2.0',
        'error':{
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }