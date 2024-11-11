from flask import Flask, Blueprint, render_template, redirect, url_for
lab5 = Blueprint('lab5', __name__)

app = Flask(__name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', username="anonymous")

# @lab5.route('/login')
# def login():
#     return render_template('login.html')

# @lab5.route('/register')
# def register():
#     return render_template('register.html')

# @lab5.route('/list')
# def list_articles():
#     return render_template('list.html')

# @lab5.route('/create')
# def create_article():
#     return render_template('create.html')

