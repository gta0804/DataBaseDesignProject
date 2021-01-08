import functools
from pymysql.cursors import DictCursor
from entry import db
from util import get_staff_area
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
sql_select_staff = 'SELECT * from  staff WHERE name=%s'
sql_select_staff_area = 'SELECT * from  staff_area WHERE staff_id=%s'
sql_select_patient = 'SELECT * from  patient WHERE nurse_id=%s'
sql_select_patient_tempature = 'SELECT * from  temperature_test WHERE patient_id=%s'
sql_select_patient_nucleic = 'SELECT * from  nucleic_test WHERE patient_id=%s'
sql_select_patient_symptoms = 'SELECT * from  symptom WHERE patient_id=%s'
sql_select_patient_area = 'SELECT * from patient_area WHERE patient_id=%s'
sql_insert_new_patient = "INSERT INTO patient( \
       name, gender, address, state_of_illness) \
       VALUES (%s, %s, %s, %s )"

bp = Blueprint('auth', __name__, url_prefix='/auth')
cursor = db.cursor(DictCursor)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        error = None
        cursor.execute(sql_select_staff,name)
        user = cursor.fetchone()

        if user is None:
            error = 'Incorrect name.'
        elif password != user['password']:
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['staff_id']
            session['user_name'] = user['name']
            session['role'] = user['role']
            # return redirect(url_for('calculation_F1.index'))
            print("success")
            return render_template('nav.html', role=user['role'], area=get_staff_area(name), name=name)

        flash(error)

    return render_template('auth/login.html')


def user2dict(user):
    if user == None:
        return
    return {
        'id': user['staff_id'],
        'name': user['name'],
        'role': user['role']
    }


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        print(user_id)
        name = session.get('user_name')
        cursor.execute(sql_select_staff,name)
        user = cursor.fetchone()
        g.user = user2dict(user)


@bp.route('/logout',methods=('GET', 'POST'))
def logout():
    session.clear()
    # return redirect(url_for('calculation_F1.index'))
    return render_template('auth/login.html')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

