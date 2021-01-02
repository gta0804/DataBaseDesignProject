from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from entry import db
from auth import login_required

bp = Blueprint('ward_nurse', __name__, url_prefix='/emergency_nurse')


@bp.route("/report", methods=("GET", "POST"))
@login_required
def report():
    patient_id = request.form['patient_id']
    from entry import sql_select_patient
    from auth import cursor, session

    sql = sql_select_patient % patient_id
    cursor.execute(sql)
    patient = cursor.fetchone()

    return render_template("ward_nurse/report.html", patient_id=patient_id,
                           name=patient['name'], username=session['user_name'],
                           role=session['role'], area=session['area'])


@bp.route("/commit_report", methods=("GET", "POST"))
@login_required
def report():
    patient_id = request.form['patient_id']
    patient_name = request.form['name']
    patient_temperature = request.form['temperature']
    patient_symptom = request.form['symptom']
    patient_life_status = request.form['life_status']

    from auth import cursor

    sql_insert_symptom = "INSERT INTO symptom( \
       patient_id,symptonm) \
       VALUES (%s, %s )" % (patient_id, patient_symptom)
    cursor.execute(sql_insert_symptom)
    db.commit()

    import time
    today = time.strftime("%Y-%m-%d", time.localtime(time.time()))

    sql_insert_temperature = "INSERT INTO temperature_test( \
       test_date,body_temperature,patient_id,) \
       VALUES (%s, %s,%s )" % (today, patient_temperature, patient_id)
    cursor.execute(sql_insert_temperature)
    db.commit()

    sql_update_life_status = "UPDATE patient SET life_status=%s WHERE patient_id=%s" % (patient_life_status, patient_id)
    cursor.execute(sql_update_life_status)
    db.commit()

    return render_template('nav.html')
