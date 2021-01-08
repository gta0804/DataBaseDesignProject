from flask import (
    Blueprint, render_template, request,
)
from auth import session, login_required
from pymysql.cursors import DictCursor
from entry import db
import datetime
from ward_nurse import compare
from util import get_staff_area
from util import insert_patient_from_isolated
from util import insert_patient_another
from emergency_nurse import has_space, has_nurse
bp = Blueprint('doctor', __name__, url_prefix='/doctor')
cursor = db.cursor(DictCursor)


@login_required
@bp.route("/show_head_nurse/<area_name>/")
def show_head_nurse(area_name):
    sql = "select * from staff natural join staff_area where role='head_nurse' and area=%s"
    cursor.execute(sql,area_name)
    result = cursor.fetchall()
    return render_template('doctor/head_nurse.html', name=session["user_name"], role=session["role"], area=get_staff_area(session["user_name"]), head_nurses=result)

@login_required
@bp.route("/show_ward_nurse/<area_name>")
def show_ward_nurse(area_name):
    sql = "select * from staff natural join staff_area where role='ward_nurse' and area=%s"
    cursor.execute(sql, area_name)
    result = cursor.fetchall()
    return render_template('doctor/head_nurse.html', name=session["user_name"], role=session["role"], area=get_staff_area(session["user_name"]), head_nurses=result)


@login_required
@bp.route("/new_nucleic_test")
def new_nucleic_test():
    return render_template('doctor/new_nucleic_test.html', name=session["user_name"], role=session["role"], area=get_staff_area(session["user_name"]), patient_id = request.args.get('patient_id'))


@login_required
@bp.route("/commit_new_nucleic_test", methods=('GET', 'POST'))
def commit_new_nucleic_test():
    patient_id = request.form['patient_id']
    test_date = datetime.datetime.strptime(request.form['test_date'],'%Y-%m-%d').date()
    find_latest_date = "select test_date from patient natural join nucleic_test" \
                       " where patient_id =%s order by test_date desc limit 1"
    cursor.execute(find_latest_date,patient_id)
    latest_date = cursor.fetchone()["test_date"]
    if compare(latest_date,test_date):
        message = '时间不符合要求'
        print(message)
        render_template("nav.html",name=session['user_name'], role=session['role'],
                                   area=get_staff_area(session['user_name']), message=message)

    insert_new_test = 'insert into nucleic_test(patient_id,test_date) values(%s,%s)'
    cursor.execute(insert_new_test,[patient_id,test_date])
    db.commit()
    return render_template('nav.html', name=session['user_name'], role=session['role'],
                                   area=get_staff_area(session['user_name']))


@login_required
@bp.route("/declare_death", methods=('GET', 'POST'))
def declare_death():
    area = get_staff_area(session["user_name"])
    patient_id = request.args.get('patient_id')
    modify_patient = "update patient set life_status='dead' where patient_id=%s"
    remove_patient = "delete from patient_area where patient_id=%s"

    remove_bed = "update bed set patient_id = null where patient_id=%s"
    remove_nurse = "update patient set nurse_id = null where patient_id =%s"
    try:
        cursor.execute(modify_patient, patient_id)
        cursor.execute(remove_patient, patient_id)
        cursor.execute(remove_bed, patient_id)
        cursor.execute(remove_nurse, patient_id)
    except Exception as e:
        db.rollback()
        print("移除死亡病人床位时出错", e)
    db.commit()
    if not insert_patient_from_isolated(area):
        insert_patient_another(area)
    return render_template('nav.html', name=session['user_name'], role=session['role'],
                                   area=get_staff_area(session['user_name']))


@login_required
@bp.route("/discharge", methods=('GET', 'POST'))
def discharge():
    area = get_staff_area(session["user_name"])
    patient_id = request.args.get('patient_id')
    modify_patient = "update patient set life_status='discharged' where patient_id=%s"
    remove_patient = "delete from patient_area where patient_id=%s"

    remove_bed = "update bed set patient_id = null where patient_id=%s"
    remove_nurse = "update patient set nurse_id = null where patient_id =%s"
    try:
        cursor.execute(modify_patient, patient_id)
        cursor.execute(remove_patient, patient_id)
        cursor.execute(remove_bed, patient_id)
        cursor.execute(remove_nurse, patient_id)
    except Exception as e:
        db.rollback()
        print("移除出院病人床位时出错", e)
    db.commit()
    if not insert_patient_from_isolated(area):
        insert_patient_another(area)
    return render_template('nav.html', name=session['user_name'], role=session['role'],
                           area=get_staff_area(session['user_name']))


@login_required
@bp.route("/modify_state_of_illness")
def modify_state_of_illness():
    patient_id = request.args.get("patient_id")
    return render_template("doctor/modify_state_of_illness.html",name=session['user_name'], role=session['role'],
                           area=get_staff_area(session['user_name']), patient_id=patient_id)


@login_required
@bp.route("/commit_modify", methods=('GET', 'POST'))
def commit_modify():
    patient_id = request.form['patient_id']
    area = request.form['area']
    new_nurse_id = has_nurse(area)
    new_bed_id = has_space(area)
    if new_nurse_id == 0 or new_bed_id == 0:
        message = '暂时无法插入'
        print(message)
        update_patient = "update patient set state_of_illness=%s where patient_id=%s"
        cursor.execute(update_patient, [area, patient_id])
        db.commit()
        return render_template("nav.html",name=session['user_name'], role=session['role'],
                           area=get_staff_area(session['user_name']), message=message)
    update_patient = "update patient set state_of_illness=%s, nurse_id=%s where patient_id=%s"
    update_area = "update patient_area set area =%s where patient_id=%s"
    update_old_bed = "update bed set patient_id=null where patient_id=%s"
    update_new_bed = "update bed set patient_id=%s where bed_id=%s"
    try:
        cursor.execute(update_patient,[area,new_nurse_id,patient_id])
        cursor.execute(update_area,[area,patient_id])
        cursor.execute(update_old_bed,patient_id)
        cursor.execute(update_new_bed,[patient_id,new_bed_id])
    except Exception as e:
        db.rollback()
        print("在更改病人病情状况时发生错误", e)
    db.commit()
    old_area = get_staff_area(session['user_name'])
    if not insert_patient_from_isolated(old_area):
        insert_patient_another(old_area)
    return render_template("nav.html", name=session['user_name'], role=session['role'],
                           area=get_staff_area(session['user_name']))


