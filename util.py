def is_temperature(temperature_list):
    print("te_list",len(temperature_list))
    if len(temperature_list) < 3:
        return False

    for temperature in temperature_list:
        print(temperature["body_temperature"])
        if temperature["body_temperature"] >= 37.299999:
            return False
    date_list = []
    print("gg")
    for temperature in temperature_list:
        date_list.append(temperature["test_date"])
    print(is_continuous(date_list))
    if is_continuous(date_list):
        return True
    return False


def is_continuous(date_list):
    import datetime
    sorted(date_list, reverse=True)
    for x in range(len(date_list)-1):
        if not date_list[x]-datetime.timedelta(1) == date_list[x+1]:
            return False
    return True


def is_nucleic(nucleic_test):
    if len(nucleic_test) < 2:
        return False

    for result in nucleic_test:
        if not result["test_result"] == "negative":
            return False

    date_list = []
    for test in nucleic_test:
        date_list.append(test["test_date"])
    if is_continuous(date_list):
        return True
    return False


def is_patient_discharged(patient_id):
    from auth import cursor
    sql_temperature = "select * from temperature_test where patient_id =%s order by test_date desc limit 3"
    sql_nucleic = "select * from nucleic_test where patient_id=%s order by test_date desc limit 2 "
    cursor.execute(sql_temperature,patient_id)
    temperature_list = cursor.fetchall()
    cursor.execute(sql_nucleic,patient_id)
    nucleic_list = cursor.fetchall()
    if is_temperature(temperature_list) & is_nucleic(nucleic_list):
        return "是"
    else:
        return "否"


def get_staff_area(name):
    from auth import cursor
    sql_select = "select * from staff natural left outer join staff_area where name=%s"
    cursor.execute(sql_select, name)
    result = cursor.fetchone()
    if result["role"] == 'emergency_nurse':
        return all
    else:
        return result["area"]


def get_symptoms(patient_id):
    from auth import cursor
    from entry import sql_select_patient_symptoms

    sql=sql_select_patient_symptoms % patient_id
    cursor.execute(sql)
    symptoms_list=cursor.fetchall()

    return symptoms_list


def get_temperature(patient_id):
    from auth import cursor

    sql_temperature = "select body_temperature from temperature_test where patient_id =%s order by test_date desc limit 1"
    cursor.execute(sql_temperature,patient_id)
    temperature = cursor.fetchone()
    return temperature


def get_patient_area(patient_id):
    from entry import sql_select_patient_area
    from auth import cursor

    sql = sql_select_patient_area % patient_id
    cursor.execute(sql)
    area = cursor.fetchone()

    if area is None:
        return None
    else:
        return area['area']


def insert_patient_from_isolated(area):
    from auth import cursor
    from entry import db
    from emergency_nurse import has_nurse,has_space
    find_isolated = "select patient_id from patient where nurse_id is null and life_status='alive' and state_of_illness=%s  limit 1"
    cursor.execute(find_isolated,area)
    results = cursor.fetchall()
    if not len(results) == 1:
        return False
    patient_id = results[0]['patient_id']
    nurse_id = has_nurse(area)
    bed_id = has_space(area)
    update_patient = "update patient set nurse_id=%s where patient_id=%s"
    insert_patient_area = 'insert into patient_area(patient_id,area) values (%s,%s)'
    update_bed = "update bed set patient_id=%s where bed_id=%s"
    try:
        cursor.execute(update_patient,[nurse_id,patient_id])
        cursor.execute(insert_patient_area,[patient_id,area])
        cursor.execute(update_bed,[patient_id,bed_id])
    except Exception as e:
        db.rollback()
        print("在调用自动将隔离区病人转为住院时发生异常", e)
    db.commit()
    return True


def insert_patient_another(area):
    from auth import cursor
    from entry import db
    from emergency_nurse import has_nurse,has_space
    find_another = "select patient_id from patient natural join patient_area where state_of_illness=%s and" \
                   " state_of_illness <> area  and life_status='alive' limit 1"
    cursor.execute(find_another,area)
    results = cursor.fetchall()
    if not len(results) == 1:
        return False
    nurse_id = has_nurse(area)
    patient_id = results[0]['patient_id']
    bed_id = has_space(area)
    update_patient = "update patient set nurse_id=%s where patient_id=%s"
    update_patient_area = 'update patient_area(patient_id,area) set area=%s where patient_id=%s'
    update_original_bed = "update bed set patient_id=null where patient_id=%s"
    update_new_bed = "update bed set patient_id=%s where bed_id=%s"
    try:
        cursor.execute(update_patient, [nurse_id, patient_id])
        cursor.execute(update_patient_area, [area, patient_id])
        cursor.execute(update_original_bed,patient_id)
        cursor.execute(update_new_bed, [patient_id, bed_id])
    except Exception as e:
        db.rollback()
        print("在调用自动将不符合区域病人转区时发生异常", e)
    db.commit()
    return True