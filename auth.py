import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from models import Staff
from entry import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        gender = request.form['gender']
        name = request.form['name']
        password = request.form['password']
        age = request.form['age']
        phone_number = request.form['phone_number']
        salary = request.form['salary']

        error = None

        if not name:
            error = 'name is required.'
        elif not password:
            error = 'Password is required.'
        elif not age:
            error = 'age is required'
        elif not phone_number:
            error = 'phone_number is required.'
        elif not salary:
            error = 'salary is required.'
        elif Staff.query.filter(Staff.name == name).first() is not None:
            error = 'User {} {} is already registered.'.format(name)

        if error is None:
            u = Staff(gender,name, age, phone_number,
                      salary, password)
            db.session.add(u)
            db.session.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        staff_id = request.form['staff_id']
        password = request.form['password']
        error = None
        user = Staff.query.filter(Staff.staff_id == staff_id).first()

        if user is None:
            error = 'Incorrect staff_id.'
        elif user.password != password:
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            #return redirect(url_for('calculation_F1.index'))
            return render_template('base.html')

        flash(error)

    return render_template('auth/login.html')


def user2dict(user):
    return {
        'id': user.id,
        'name': user.name,
    }


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = user2dict(Staff.query.filter(Staff.id == user_id).first())


@bp.route('/logout')
def logout():
    session.clear()
    #return redirect(url_for('calculation_F1.index'))
    return render_template('base.html')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
