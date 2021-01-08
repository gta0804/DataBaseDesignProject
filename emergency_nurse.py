from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from auth import session,login_required
from util import get_staff_area
from entry import sql_insert_new_patient, db
from auth import cursor

bp = Blueprint('emergency_nurse', __name__, url_prefix='/emergency_nurse')


@bp.route('/new_patient', methods=('GET', 'POST'))
@login_required
def new_patient():
    if request.method == 'GET':
        return render_template("emergency_nurse/new_patient.html",
                               username=session['user_name'], role=session['role'],
                               area=get_staff_area(session['user_name']))
    else:
        patient_name = request.form['name']
        patient_gender = request.form['gender']
        patient_address = request.form['address']
        patient_state_of_illness = request.form['state_of_illness']
        patient_age = request.form['age']
        test_date = request.form['test_date']
        room_id = has_space(patient_state_of_illness)
        nurse_id = has_nurse(patient_state_of_illness)
        if nurse_id == 0 or room_id == 0:
            print("here")
            if nurse_id == 0:
                message = '没有空闲的护士'
            else:
                message = '没有空余房间'
            insert_patient = "insert into patient(name,gender,address,state_of_illness,age," \
                             "life_status) values(%s,%s,%s,%s,%s,'alive')"
            insert_nucleic_test = "insert into nucleic_test (test_date,test_result,patient_id) values(%s,'positive',%s)"
            try:
              cursor.execute(insert_patient,[patient_name,patient_gender,patient_address,patient_state_of_illness,patient_age])
              sql_get_patient_id = "select patient_id from patient where name=%s"
              cursor.execute(sql_get_patient_id, patient_name)
              patient_id = cursor.fetchone()["patient_id"]
              cursor.execute(insert_nucleic_test, [test_date, patient_id])
            except Exception as e:
                db.rollback()
                print("添加新病人至隔离区失败", e)
            db.commit()
            return render_template("nav.html", username=session['user_name'], role=session['role'],
                                   area=get_staff_area(session['user_name']), message=message)

        insert_patient = "insert into patient(name,gender,address,state_of_illness,age," \
                         "nurse_id,life_status) values(%s,%s,%s,%s,%s,%s,'alive')"
        insert_nucleic_test = "insert into nucleic_test (test_date,test_result,patient_id) values(%s,'positive',%s)"
        insert_patient_area ="insert into patient_area(patient_id,area) values(%s,%s)"
        update_room = "update bed set patient_id=%s where bed_id =%s"
        try:
            cursor.execute(insert_patient, [patient_name,patient_gender,patient_address,patient_state_of_illness,
                           patient_age, nurse_id])
            sql_get_patient_id = "select patient_id from patient where name=%s"
            cursor.execute(sql_get_patient_id, patient_name)
            patient_id = cursor.fetchone()["patient_id"]
            cursor.execute(insert_patient_area,[patient_id,patient_state_of_illness])
            cursor.execute(insert_nucleic_test, [test_date, patient_id])
            cursor.execute(update_room, [patient_id, room_id])
        except Exception as e:
            db.rollback()
            print('添加新病人失败', e)
        db.commit()
        return render_template("nav.html", username=session['user_name'], role=session['role'],
                                   area=get_staff_area(session['user_name']))



def has_space(area):
    sql = "select bed_id from bed where area=%s and patient_id is null order by bed_id limit 1"
    cursor.execute(sql, area)
    result = cursor.fetchall()
    if len(result) < 1:
        return 0
    return result[0]["bed_id"]


def has_nurse(area):
    limit_number = 0
    if area == 'soft':
        limit_number = 3
    elif area == 'urgent':
        limit_number = 2
    elif area == 'very_urgent':
        limit_number = 1
    sql = "select staff_id from staff natural join staff_area where area =%s and role='ward_nurse' "
    cursor.execute(sql, area)
    results = cursor.fetchall()
    list_nurses = []

    for result in results:
        list_nurses.append(result["staff_id"])

    for nurse_id in list_nurses:
        find_related = "select count(nurse_id) as count_nurse from patient  where nurse_id = %s"
        cursor.execute(find_related, nurse_id)
        count = cursor.fetchone()["count_nurse"]
        if count < limit_number:
            return nurse_id
    return 0
