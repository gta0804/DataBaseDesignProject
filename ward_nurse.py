from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from entry import db

bp = Blueprint('ward_nurse', __name__, url_prefix='/emergency_nurse')


@bp.route("/report", methods=("GET", "POST"))
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
