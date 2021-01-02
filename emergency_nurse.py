from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from auth import session

bp = Blueprint('emergency_nurse', __name__, url_prefix='/emergency_nurse')


@bp.route('/new_patient', methods=('GET', 'POST'))
def new_patient():
    if request.method == 'GET':
        return render_template("emergency_nurse/new_patient.html",
                               username=session['user_name'], role=session['role'],
                               area=session['area'])
    else:
        patient_name = request.form['name']
        patient_gender = request.form['gender']
        patient_address = request.form['address']
        patient_state_of_illness = request.form['state_of_illness']

        from entry import sql_insert_new_patient, db
        from auth import cursor

        sql = sql_insert_new_patient % (patient_name, patient_gender, patient_address, patient_state_of_illness)
        cursor.execute(sql)
        db.connect()

        return render_template("emergency_nurse/new_patient.html",
                               username=session['user_name'], role=session['role'],
                               area=session['area'])
