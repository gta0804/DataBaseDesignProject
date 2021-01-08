from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from entry import db
from auth import cursor
from util import get_staff_area
bp = Blueprint('head_nurse', __name__, url_prefix='/head_nurse')


@bp.route("/bed", methods=['GET','POST'])
def bed():
    area = get_staff_area(session['user_name'])
    get_beds = "select * from bed natural left outer join patient where area =%s"
    cursor.execute(get_beds,area)
    results = cursor.fetchall()
    beds = []
    for result in results:
        beds.append(result)

    return render_template("head_nurse/bed.html", name=session['user_name'], area=area, role=session['role'],
                           staff_id=session['user_id'], beds=beds)


@bp.route("/nurse", methods=['GET', 'POST'])
def nurse():
    area = get_staff_area(session['user_name'])
    get_nurse = "select * from staff natural join staff_area where area=%s and role='ward_nurse'"
    cursor.execute(get_nurse, area)
    results = cursor.fetchall()
    nurses = []
    for result in results:
        nurse = []
        nurse_id = result['staff_id']
        get_patients = "select patient_id from patient where nurse_id=%s"
        cursor.execute(get_patients, nurse_id)
        patients = list(cursor.fetchall())
        nurse.append(result['staff_id'])
        nurse.append(result['name'])
        nurse.append(result['gender'])
        nurse.append(result['age'])
        nurse.append(result['area'])
        nurse.append(patients)
        if len(patients) == 0:
           nurse.append("没有病人")
        nurses.append(nurse)

    get_free_nurse = "select * from staff natural left outer join staff_area where area is null and role='ward_nurse'"
    cursor.execute(get_free_nurse)
    free_nurses_results = cursor.fetchall()

    free_nurses = []
    for result in free_nurses_results:
        nurse = []
        nurse.append(result['staff_id'])
        nurse.append(result['name'])
        nurse.append(result['gender'])
        nurse.append(result['age'])
        free_nurses.append(nurse)


    return render_template("head_nurse/nurse.html", name=session['user_name'], area=area, role=session['role'],
                           staff_id=session['user_id'], nurses=nurses, free_nurses=free_nurses)


@bp.route("/delete_nurse")
def delete_nurse():
    nurse_id = request.args.get("staff_id")
    del_nurse = "delete from staff_area where staff_id=%s"
    cursor.execute(del_nurse, nurse_id)
    db.commit()
    return render_template("nav.html", name=session['user_name'], area=get_staff_area(session['user_name']), role=session['role'],staff_id=session['user_id'])


@bp.route("/add_nurse")
def add_nurse():
    area = get_staff_area(session['user_name'])
    nurse_id = request.args.get("staff_id")
    ad_nurse = "insert into staff_area(staff_id,area) values(%s,%s)"
    cursor.execute(ad_nurse, [nurse_id,area])
    db.commit()
    return render_template("nav.html", name=session['user_name'], area=get_staff_area(session['user_name']), role=session['role'],staff_id=session['user_id'])