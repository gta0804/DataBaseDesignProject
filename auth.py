import functools
from pymysql.cursors import DictCursor

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from entry import db, sql_select_staff, sql_select_staff_area

bp = Blueprint('auth', __name__, url_prefix='/auth')
cursor = db.cursor(DictCursor)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        error = None
        sql = sql_select_staff % name
        cursor.execute(sql)
        user = cursor.fetchone()

        if user is None:
            error = 'Incorrect name.'
        elif password != user['password']:
            error = 'Incorrect password.'

        sql_area = sql_select_staff_area % user['staff_id']
        cursor.execute(sql_area)
        area = cursor.fetchone()
        area_list = []
        if user['role'] == 'emergency_nurse':
            area_list.append('soft')
            area_list.append('urgent')
            area_list.append('very_urgent')
        else:
            area_list.append(area['area'])

        if error is None:
            session.clear()
            session['user_id'] = user['staff_id']
            session['user_name'] = user['name']
            session['role'] = user['role']
            session['area'] = area_list
            # return redirect(url_for('calculation_F1.index'))
            print("success")
            return render_template('nav.html', role=user['role'], area=area_list, name=name)

        flash(error)

    return render_template('auth/login.html')


def user2dict(user):
    if user == None:
        return
    return {
        'id': user.staff_id,
        'name': user.name,
    }


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        name = session.set('user_name')
        sql = sql_select_staff % name
        cursor.execute(sql)
        user = cursor.fetchone()
        g.user = user2dict(user)


@bp.route('/logout')
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
