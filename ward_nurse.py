from flask import (
    Blueprint,  render_template, request, session
)
from entry import db
from auth import login_required
from auth import cursor
from util import get_staff_area
from util import insert_patient_from_isolated
from util import insert_patient_another
import datetime
bp = Blueprint('ward_nurse', __name__, url_prefix='/ward_nurse')


@bp.route("/report", methods=("GET", "POST"))
@login_required
def report():
    return render_template("ward_nurse/report.html", patient_id=request.args.get('patient_id'),
                            name=session['user_name'],
                           role=session['role'], area=get_staff_area(session['user_name']))


@bp.route("/commit_report", methods=("GET", "POST"))
@login_required
def commit_report():
    area = get_staff_area(session["user_name"])
    if request.method == "POST":
        patient_id = request.form['patient_id']
        patient_temperature = request.form['temperature']
        patient_symptom = request.form['symptom']
        patient_life_status = request.form['life_status']
        test_date = datetime.datetime.strptime(request.form['test_date'], '%Y-%m-%d').date()

        find_latest_date = "select test_date from patient natural join temperature_test" \
                          " where nurse_id=%s and patient_id =%s order by test_date desc limit 1"
        cursor.execute(find_latest_date, [session["user_id"],patient_id])
        result = cursor.fetchall()
        if len(result) > 0 and compare(result[0]['test_date'] , test_date):
            message = '插入时间不符合要求'
            print(message)
            return render_template('nav.html', name=session['user_name'], role=session['role'],
                                   area=get_staff_area(session['user_name']), message=message)
        update_patient = "update patient set life_status=%s,symptom=%s  where patient_id=%s"
        insert_temperature_test = "insert into  temperature_test" \
                                  "(patient_id,body_temperature,test_date) values (%s,%s,%s)"
        remove_patient = "delete from patient_area where patient_id=%s"

        remove_bed = "update bed set patient_id = null where patient_id=%s"
        remove_nurse = "update patient set nurse_id = null where patient_id =%s"
        try:
            cursor.execute(update_patient, [patient_life_status, patient_symptom,patient_id])
            cursor.execute(insert_temperature_test, [patient_id, patient_temperature, test_date])
            if patient_life_status == 'dead':
                cursor.execute(remove_patient, patient_id)
                cursor.execute(remove_bed, patient_id)
                cursor.execute(remove_nurse, patient_id)
        except Exception as e:
            db.rollback()
            print("添加病人日常信息时发生异常", e)
        db.commit()
        if patient_life_status == 'dead':
            if not insert_patient_from_isolated(area):
                insert_patient_another(area)
        return render_template('nav.html', name=session['user_name'],
                               role=session['role'], area=get_staff_area(session['user_name']))


def compare(latest_date, request_date):
    if request_date <= latest_date:
        return True
    return False


@bp.route("/show_nucleic_tests_to_report", methods=["GET","POST"])
def show_nucleic_tests_to_report():
    area = get_staff_area(session['user_name'])
    if not area:
        return render_template('nav.html', name=session['user_name'],
                               role=session['role'], area=get_staff_area(session['user_name']))
    find_to_report = "select * from  patient natural join nucleic_test where nurse_id=%s and test_result is null"
    cursor.execute(find_to_report, session["user_id"])
    nucleic_reports = cursor.fetchall()
    return render_template('ward_nurse/nucleic_report.html', name=session['user_name'],
                               role=session['role'], area=area, nucleic_reports=nucleic_reports)


@bp.route("/nucleic_test", methods=["GET","POST"])
def nucleic_test():
    patient_id = request.args.get("patient_id")
    test_date = request.args.get("test_date")
    return render_template('ward_nurse/nucleic_report_form.html', name=session['user_name'],
                               role=session['role'], area=get_staff_area(session['user_name']), patient_id=patient_id, test_date=test_date)


@bp.route("/commit_nucleic_test", methods=["GET","POST"])
def commit_nucleic_test():
    patient_id = request.form['patient_id']
    test_date = request.form['test_date']
    test_result = request.form['test_result']
    update_report = "update nucleic_test set test_result=%s where patient_id=%s and test_date=%s"
    cursor.execute(update_report, [test_result, patient_id, test_date])
    db.commit()
    return render_template('nav.html', name=session['user_name'],
                               role=session['role'], area=get_staff_area(session['user_name']))