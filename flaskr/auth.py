import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.models import Staff
from flaskr.entry import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        gender = request.form['gender']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        birth = request.form['birth']
        age = request.form['age']
        phone_number = request.form['phone_number']
        salary = request.form['salary']

        error = None

        if not first_name:
            error = 'first_name is required.'
        elif not password:
            error = 'Password is required.'
        elif not last_name:
            error = 'last_name is required.'
        elif not birth:
            error = 'birth is required.'
        elif not age:
            error = 'age is required'
        elif not phone_number:
            error = 'phone_number is required.'
        elif not salary:
            error = 'salary is required.'
        elif Staff.query.filter(Staff.first_name == first_name & Staff.last_name == last_name).first() is not None:
            error = 'User {} {} is already registered.'.format(first_name, last_name)

        if error is None:
            u = Staff(gender, first_name, last_name, birth, age, phone_number,
                      salary, password)
            db.session.add(u)
            db.session.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name=request.form['last_name']
        password = request.form['password']
        error = None
        user = Staff.query.filter(Staff.first_name == first_name&Staff.last_name==last_name).first()

        if user is None:
            error = 'Incorrect username.'
        elif user.password != password:
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            session['user_first_name'] = user.first_name
            session['user_last_name']=user.last_name
            #return redirect(url_for('calculation_F1.index'))
            return render_template('base.html')

        flash(error)

    return render_template('auth/login.html')


def user2dict(user):
    return {
        'id': user.id,
        'name': user.first_name+user.last_name,
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
