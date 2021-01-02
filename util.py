def is_tempare(tempare_test_list):
    tempare_list = []
    for tem in tempare_test_list:
        tempare_list.append(list(tem))

    sorted(tempare_list, key=lambda s: s[0])
    tempare_list.reverse()

    if len(tempare_list) < 3:
        return False

    if not (tempare_list[0][1] < 37.3 & tempare_list[1][1] < 37.3 & tempare_list[2][1] < 37.3):
        return False

    data1 = tempare_list[0][1][8:]
    data2 = tempare_list[1][1][8:]
    data3 = tempare_list[2][1][8:]

    if not ((data1 != data2) & (data2 != data3)):
        return False

    return True


def is_nucleic(nuc_leic_test):
    tem_list = []

    for tem in nuc_leic_test:
        tem_list.append(list(tem))

    sorted(tem_list, key=lambda s: s[0])
    tem_list.reverse()

    if len(tem_list) < 2:
        return False

    if not (tem_list[0][1] == 'negative' & tem_list[1][1] == 'negative'):
        return False

    data1 = tem_list[0][0][8:]
    data2 = tem_list[1][0][8:]

    if not data1 != data2:
        return False

    return True


def is_patient_discraged(patient_id):
    from entry import sql_select_patient_nucleic, sql_select_patient_tempare
    from auth import cursor

    sql_temperature = sql_select_patient_tempare % patient_id
    sql_nucleic = sql_select_patient_nucleic % patient_id
    cursor.execute(sql_temperature)
    temperature_list = cursor.fetchall()
    cursor.execute(sql_nucleic)
    nucleic_list = cursor.fetchall()

    if is_tempare(temperature_list) & is_nucleic(nucleic_list):
        return True
    else:
        return False


def get_symptoms(patient_id):
    from auth import cursor
    from entry import sql_select_patient_symptoms

    sql=sql_select_patient_symptoms % patient_id
    cursor.execute(sql)
    symptoms_list=cursor.fetchall()

    return symptoms_list


def get_temperature(patient_id):
    from entry import  sql_select_patient_tempare
    from auth import cursor

    sql_temperature = sql_select_patient_tempare % patient_id
    cursor.execute(sql_temperature)
    temperature_list = cursor.fetchall()

    tempare_list = []
    for tem in temperature_list:
        tempare_list.append(list(tem))

    sorted(tempare_list, key=lambda s: s[0])
    tempare_list.reverse()

    return temperature_list[0][1]


def get_patient_area(patient_id):
    from entry import sql_select_patient_area
    from auth import cursor

    sql=sql_select_patient_area % patient_id
    cursor.execute(sql)
    area=cursor.fetchall()

    if area is None:
        return None
    else:
        return area['area']



