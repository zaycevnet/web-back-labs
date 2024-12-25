from flask import Blueprint, url_for, redirect, render_template, request, make_response, session, current_app, jsonify
import sqlite3
import json
from os import path
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
zaycev_rgz = Blueprint('zaycev_rgz', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'ser_knowledge_base',
            user = 'ser_knowledge_base',
            password = '123'
            )

        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn,cur):
    conn.commit()
    cur.close()
    conn.close()



@zaycev_rgz.route('/zaycev_rgz')
def main_rgz():
    if 'login' in session:
        login = session['login']
        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute(f"SELECT * FROM employees")
            employees = cur.fetchall()
        else: 
            cur.execute(f"SELECT * FROM employees")
            employees = [dict(row) for row in cur.fetchall()]
        db_close(conn,cur)
        return render_template('/zaycev_rgz/emp.html', employees=employees, login=login)
    else:
        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute(f"SELECT * FROM employees")
            employees = cur.fetchall()
        else: 
            cur.execute(f"SELECT * FROM employees")
            employees = [dict(row) for row in cur.fetchall()]
        db_close(conn,cur)
        return render_template('/zaycev_rgz/emp.html', employees=employees)


@zaycev_rgz.route('/zaycev_rgz/full', methods=['GET', 'POST'])
def main_rgz_full():
    if 'login' in session:
        login = session['login']
        if request.method == 'POST':
            name = request.form.get('name')
            where = request.form.get('where')
            where2 = request.form.get('where2') 
            sex = request.form.get('sex')
            isp = request.form.get('isp')
            search_pattern = f"%{name.lower()}%"
            conn, cur = db_connect()

            if sex == 'no' and isp == 'no':
                if current_app.config['DB_TYPE'] == 'postgres':
                    query = f"SELECT * FROM employees WHERE LOWER({where}) LIKE %s ORDER BY {where2}"
                    cur.execute(query, (search_pattern,))  
                    employees = cur.fetchall()
                else: 
                    query = f"SELECT * FROM employees WHERE LOWER({where}) LIKE ? ORDER BY {where2}"
                    cur.execute(query, (search_pattern,))  
                    employees = [dict(row) for row in cur.fetchall()]

                db_close(conn, cur)
                return render_template('/zaycev_rgz/emp_full.html', employees=employees, name=name, where=where, where2=where2, sex=sex, isp=isp, login=login)
            
            if sex != 'no' and isp != 'no':
                if current_app.config['DB_TYPE'] == 'postgres':
                    query = f"SELECT * FROM employees WHERE LOWER({where}) LIKE %s AND gender = %s AND probationary_period = %s ORDER BY {where2}"
                    cur.execute(query, (search_pattern, sex, isp))  
                    employees = cur.fetchall()
                else: 
                    query = f"SELECT * FROM employees WHERE LOWER({where}) LIKE ? AND gender = ? AND probationary_period = ? ORDER BY {where2}"
                    cur.execute(query, (search_pattern, sex, isp))  
                    employees = [dict(row) for row in cur.fetchall()]

                db_close(conn, cur)
                return render_template('/zaycev_rgz/emp_full.html', employees=employees, name=name, where=where, where2=where2, sex=sex, isp=isp, login=login)

            if sex != 'no' and isp == 'no':
                if current_app.config['DB_TYPE'] == 'postgres':
                    query = f"SELECT * FROM employees WHERE LOWER({where}) LIKE %s AND gender = %s ORDER BY {where2}"
                    cur.execute(query, (search_pattern, sex))  
                    employees = cur.fetchall()
                else: 
                    query = f"SELECT * FROM employees WHERE LOWER({where}) LIKE ? AND gender = ? ORDER BY {where2}"
                    cur.execute(query, (search_pattern, sex))  
                    employees = [dict(row) for row in cur.fetchall()]

                db_close(conn, cur)
                return render_template('/zaycev_rgz/emp_full.html', employees=employees, name=name, where=where, where2=where2, sex=sex, isp=isp, login=login)


            if sex == 'no' and isp != 'no':
                if current_app.config['DB_TYPE'] == 'postgres':
                    query = f"SELECT * FROM employees WHERE LOWER({where}) LIKE %s AND probationary_period = %s ORDER BY {where2}"
                    cur.execute(query, (search_pattern, isp))  
                    employees = cur.fetchall()
                else: 
                    query = f"SELECT * FROM employees WHERE LOWER({where}) LIKE ? AND probationary_period = ? ORDER BY {where2}"
                    cur.execute(query, (search_pattern, isp))  
                    employees = [dict(row) for row in cur.fetchall()]

                db_close(conn, cur)
                return render_template('/zaycev_rgz/emp_full.html', employees=employees, name=name, where=where, where2=where2, sex=sex, isp=isp, login=login)


        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute(f"SELECT * FROM employees")
            employees = cur.fetchall()
        else: 
            cur.execute(f"SELECT * FROM employees")
            employees = [dict(row) for row in cur.fetchall()]
        db_close(conn,cur)
        return render_template('/zaycev_rgz/emp_full.html', employees=employees, login=login)
    else:
        if request.method == 'POST':
            name = request.form.get('name')
            where = request.form.get('where')
            where2 = request.form.get('where2') 
            sex = request.form.get('sex')
            isp = request.form.get('isp')
            search_pattern = f"%{name.lower()}%"
            conn, cur = db_connect()

            if sex == 'no' and isp == 'no':
                if current_app.config['DB_TYPE'] == 'postgres':
                    query = f"SELECT * FROM employees WHERE LOWER({where}) LIKE %s ORDER BY {where2}"
                    cur.execute(query, (search_pattern,))  
                    employees = cur.fetchall()
                else: 
                    query = f"SELECT * FROM employees WHERE LOWER({where}) LIKE ? ORDER BY {where2}"
                    cur.execute(query, (search_pattern,))  
                    employees = [dict(row) for row in cur.fetchall()]

                db_close(conn, cur)
                return render_template('/zaycev_rgz/emp_full.html', employees=employees, name=name, where=where, where2=where2, sex=sex, isp=isp)
            
            if sex != 'no' and isp != 'no':
                if current_app.config['DB_TYPE'] == 'postgres':
                    query = f"SELECT * FROM employees WHERE LOWER({where}) LIKE %s AND gender = %s AND probationary_period = %s ORDER BY {where2}"
                    cur.execute(query, (search_pattern, sex, isp))  
                    employees = cur.fetchall()
                else: 
                    query = f"SELECT * FROM employees WHERE LOWER({where}) LIKE ? AND gender = ? AND probationary_period = ? ORDER BY {where2}"
                    cur.execute(query, (search_pattern, sex, isp))  
                    employees = [dict(row) for row in cur.fetchall()]

                db_close(conn, cur)
                return render_template('/zaycev_rgz/emp_full.html', employees=employees, name=name, where=where, where2=where2, sex=sex, isp=isp)

            if sex != 'no' and isp == 'no':
                if current_app.config['DB_TYPE'] == 'postgres':
                    query = f"SELECT * FROM employees WHERE LOWER({where}) LIKE %s AND gender = %s ORDER BY {where2}"
                    cur.execute(query, (search_pattern, sex))  
                    employees = cur.fetchall()
                else: 
                    query = f"SELECT * FROM employees WHERE LOWER({where}) LIKE ? AND gender = ? ORDER BY {where2}"
                    cur.execute(query, (search_pattern, sex))  
                    employees = [dict(row) for row in cur.fetchall()]

                db_close(conn, cur)
                return render_template('/zaycev_rgz/emp_full.html', employees=employees, name=name, where=where, where2=where2, sex=sex, isp=isp)


            if sex == 'no' and isp != 'no':
                if current_app.config['DB_TYPE'] == 'postgres':
                    query = f"SELECT * FROM employees WHERE LOWER({where}) LIKE %s AND probationary_period = %s ORDER BY {where2}"
                    cur.execute(query, (search_pattern, isp))  
                    employees = cur.fetchall()
                else: 
                    query = f"SELECT * FROM employees WHERE LOWER({where}) LIKE ? AND probationary_period = ? ORDER BY {where2}"
                    cur.execute(query, (search_pattern, isp))  
                    employees = [dict(row) for row in cur.fetchall()]

                db_close(conn, cur)
                return render_template('/zaycev_rgz/emp_full.html', employees=employees, name=name, where=where, where2=where2, sex=sex, isp=isp)


        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute(f"SELECT * FROM employees")
            employees = cur.fetchall()
        else: 
            cur.execute(f"SELECT * FROM employees")
            employees = [dict(row) for row in cur.fetchall()]
        db_close(conn,cur)
        return render_template('/zaycev_rgz/emp_full.html', employees=employees)


@zaycev_rgz.route('/zaycev_rgz/delete')
def delete_emp():
    isfull = request.args.get('list')
    id = request.args.get('id')
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM employees WHERE id=%s", (id,))
    else: 
        cur.execute("DELETE FROM employees WHERE id=?", (id,))
    db_close(conn,cur)
    return redirect('/zaycev_rgz')
    

@zaycev_rgz.route('/zaycev_rgz/redact_<int:id>', methods=['POST'])
def redact(id):
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM employees WHERE id=%s", (id,))
        employee = cur.fetchone()
    else: 
        cur.execute("SELECT * FROM employees WHERE id=?", (id,))
        employee = cur.lastrowid
    db_close(conn,cur)
    return render_template('/zaycev_rgz/redact.html', employee=employee, id=id)



@zaycev_rgz.route('/zaycev_rgz/redact', methods=['POST'])
def redact_full():
    fio = request.form.get('full_name')
    position = request.form.get('position')
    gender = str(request.form.get('sex'))
    phone = request.form.get('phone')
    prob = request.form.get('prob')
    email = request.form.get('email')
    data = request.form.get('data')
    id = request.form.get('id')

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE employees SET full_name=%s, position=%s, gender=%s, phone=%s, email=%s, probationary_period=%s, hire_date=%s WHERE id=%s;", (fio,position, gender, phone, email, prob, data, id))
    else: 
        cur.execute("UPDATE employees SET full_name=?, position=?, gender=?, phone=?, email=?, probationary_period=?, hire_date=? WHERE id=?;",
                     (fio,position, gender, phone, email, prob, data, id))
    db_close(conn,cur)

    return redirect('/zaycev_rgz')



@zaycev_rgz.route('/zaycev_rgz/new', methods=['POST'])
def new_emp():
    return render_template('/zaycev_rgz/new.html')



@zaycev_rgz.route('/zaycev_rgz/new_emp', methods=['POST'])
def new_emp2():



    fio = request.form.get('full_name')
    position = request.form.get('position')
    gender = request.form.get('sex')
    phone = request.form.get('phone')
    prob = request.form.get('prob')
    email = request.form.get('email')
    data = request.form.get('data')
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO employees(full_name, position, gender, phone, email, probationary_period, hire_date) VALUES(%s, %s, %s, %s, %s, %s, %s);", 
                    (fio,position, gender, phone, email, prob, data))
    else: 
        cur.execute("INSERT INTO employees(full_name, position, gender, phone, email, probationary_period, hire_date) VALUES(%s, %s, %s, %s, %s, %s, %s);", 
                    (fio,position, gender, phone, email, prob, data))
    db_close(conn,cur)

    return redirect('/zaycev_rgz')



@zaycev_rgz.route('/zaycev_rgz/find_emp')
def find_name():
    return render_template('/zaycev_rgz/find_name.html')


@zaycev_rgz.route('/zaycev_rgz/find_emp2', methods=['POST'])
def find_name2():
    name = request.form.get('name')
    where = request.form.get('where')
    where2 = request.form.get('where2') 
    sex = request.form.get('sex')
    isp = request.form.get('isp')
    search_pattern = f"%{name.lower()}%"
    conn, cur = db_connect()

    if sex == 'no' and isp == 'no':
        if current_app.config['DB_TYPE'] == 'postgres':
            query = f"SELECT * FROM employees WHERE LOWER({where}) LIKE %s ORDER BY {where2}"
            cur.execute(query, (search_pattern,))  
            employees = cur.fetchall()
        else: 
            query = f"SELECT * FROM employees WHERE LOWER({where}) LIKE ? ORDER BY {where2}"
            cur.execute(query, (search_pattern,))  
            employees = [dict(row) for row in cur.fetchall()]

        db_close(conn, cur)
        return render_template('/zaycev_rgz/emp.html', employees=employees, name=name, where=where, where2=where2, sex=sex, isp=isp)
    
    if sex != 'no' and isp != 'no':
        if current_app.config['DB_TYPE'] == 'postgres':
            query = f"SELECT * FROM employees WHERE LOWER({where}) LIKE %s AND gender = %s AND probationary_period = %s ORDER BY {where2}"
            cur.execute(query, (search_pattern, sex, isp))  
            employees = cur.fetchall()
        else: 
            query = f"SELECT * FROM employees WHERE LOWER({where}) LIKE ? AND gender = ? AND probationary_period = ? ORDER BY {where2}"
            cur.execute(query, (search_pattern, sex, isp))  
            employees = [dict(row) for row in cur.fetchall()]

        db_close(conn, cur)
        return render_template('/zaycev_rgz/emp.html', employees=employees, name=name, where=where, where2=where2, sex=sex, isp=isp)

    if sex != 'no' and isp == 'no':
        if current_app.config['DB_TYPE'] == 'postgres':
            query = f"SELECT * FROM employees WHERE LOWER({where}) LIKE %s AND gender = %s ORDER BY {where2}"
            cur.execute(query, (search_pattern, sex))  
            employees = cur.fetchall()
        else: 
            query = f"SELECT * FROM employees WHERE LOWER({where}) LIKE ? AND gender = ? ORDER BY {where2}"
            cur.execute(query, (search_pattern, sex))  
            employees = [dict(row) for row in cur.fetchall()]

        db_close(conn, cur)
        return render_template('/zaycev_rgz/emp.html', employees=employees, name=name, where=where, where2=where2, sex=sex, isp=isp)


    if sex == 'no' and isp != 'no':
        if current_app.config['DB_TYPE'] == 'postgres':
            query = f"SELECT * FROM employees WHERE LOWER({where}) LIKE %s AND probationary_period = %s ORDER BY {where2}"
            cur.execute(query, (search_pattern, isp))  
            employees = cur.fetchall()
        else: 
            query = f"SELECT * FROM employees WHERE LOWER({where}) LIKE ? AND probationary_period = ? ORDER BY {where2}"
            cur.execute(query, (search_pattern, isp))  
            employees = [dict(row) for row in cur.fetchall()]

        db_close(conn, cur)
        return render_template('/zaycev_rgz/emp.html', employees=employees, name=name, where=where, where2=where2, sex=sex, isp=isp)



@zaycev_rgz.route('/zaycev_rgz/login', methods=['POST'])
def login_zaycev():
    login = request.form.get('login')
    password = request.form.get('password')
    employees = request.form.get('spisok')

    conn, cur = db_connect()


    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"SELECT * FROM admin WHERE login=%s;", (login,))
        user = cur.fetchone()
    else:
        cur.execute(f"SELECT * FROM admin WHERE login=?;", (login,))
        employees = cur.lastrowid

    if not user:
        db_close(conn,cur)
        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute(f"SELECT * FROM employees")
            employees = cur.fetchall()
        else: 
            cur.execute(f"SELECT * FROM employees")
            employees = [dict(row) for row in cur.fetchall()]
        db_close(conn,cur)
        return render_template('/zaycev_rgz/emp.html', employees=employees, error='Логин и/или пароль неверны')
    if not check_password_hash(user['password'], password):
        db_close(conn,cur)
        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute(f"SELECT * FROM employees")
            employees = cur.fetchall()
        else: 
            cur.execute(f"SELECT * FROM employees")
            employees = [dict(row) for row in cur.fetchall()]
        db_close(conn,cur)
        return render_template('/zaycev_rgz/emp.html', employees=employees, error='Логин и/или пароль неверны')
    
    session['login'] = login
    db_close(conn,cur)
    return redirect('/zaycev_rgz')


@zaycev_rgz.route('/zaycev_rgz/logout', methods=['POST'])
def logout_admin():
    session.pop('login', None)
    return redirect('/zaycev_rgz')