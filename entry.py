import pymysql

db = pymysql.connect("localhost", "root", "password", "pj")
sql_select_staff = 'SELECT * from  staff WHERE name=%s'
sql_select_staff_area = 'SELECT * from  staff_area WHERE staff_id=%s'
sql_select_patient = 'SELECT * from  patient WHERE nurse_id=%s'
sql_select_patient_tempare = 'SELECT * from  temperature_test WHERE patient_id=%s'
sql_select_patient_nucleic = 'SELECT * from  nucleic_test WHERE patient_id=%s'
sql_select_patient_symptoms = 'SELECT * from  symptom WHERE patient_id=%s'
sql_select_patient_area = 'SELECT * from patient_area WHERE patient_id=%s'
sql_insert_new_patient="INSERT INTO patient( \
       name, gender, address, state_of_illness) \
       VALUES (%s, %s, %s, %s )"

# import auth
# import calculation_F1
'''
(base) qinghua@MacBook-Pro-2 flaskr % source activate db-pj
(db-pj) qinghua@MacBook-Pro-2 flaskr % cd ..
(db-pj) qinghua@MacBook-Pro-2 DataBaseDesignProject % python3
Python 3.7.9 (default, Aug 31 2020, 07:22:35) 
[Clang 10.0.0 ] :: Anaconda, Inc. on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from flaskr.app import db
>>> from flaskr.entry import db,create_app
>>> db.create_all(app=create_app())
>>>
'''
