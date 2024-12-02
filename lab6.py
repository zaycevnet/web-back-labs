from flask import Blueprint, url_for, redirect, render_template, request, make_response, session, current_app
import sqlite3
from os import path
lab6 = Blueprint('lab6', __name__)
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash


@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')