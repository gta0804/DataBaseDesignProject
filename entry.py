import pymysql
from flask import Flask, render_template
import auth as auth
import emergency_nurse as emergency_nurse
import ward_nurse as ward_nurse

db = pymysql.connect("localhost", "root", "123456xy", "pj")
sql_select_staff = 'SELECT * from  staff WHERE name=%s'
sql_select_staff_area = 'SELECT * from  staff_area WHERE staff_id=%s'
sql_select_patient = 'SELECT * from  patient WHERE nurse_id=%s'
sql_select_patient_tempare = 'SELECT * from  temperature_test WHERE patient_id=%s'
sql_select_patient_nucleic = 'SELECT * from  nucleic_test WHERE patient_id=%s'
sql_select_patient_symptoms = 'SELECT * from  symptoms WHERE patient_id=%s'
sql_select_patient_area = 'SELECT * from patient_area WHERE patient_id=%s'
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


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # 密码123456xy 启动mysql：sudo mysql.server start.mysql -u root -p

    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    '''
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    '''

    # a simple page that says hello
    @app.route('/hello_world')
    def hello():
        return 'Hello, World!'

    @app.route('/')
    def index():
        return render_template('templates/base.html')

    from auth import login_required, session, cursor

    @login_required
    @app.route('/all_patient')
    def all_patient():
        sql = sql_select_patient % session['user_id']
        cursor.execute(sql)
        raw_patient_list = cursor.fetchall()

        patient_list = []

        for patient in raw_patient_list:
            patient_id = patient['patient_id']

            from util import is_patient_discraged, get_patient_area, get_symptoms, get_temperature
            list = []
            list.append(patient_id)
            list.append(patient['gender'])
            list.append(patient['name'])
            list.append(patient['address'])
            list.append(get_temperature(patient_id))
            list.append(patient['life_status'])
            list.append(patient['state_of_illness'])
            list.append(get_symptoms(patient_id))
            list.append(get_patient_area(patient_id))
            list.append(is_patient_discraged(patient_id))
            patient_list.append(list)

        return render_template('all_patient.html', username=session['user_name'],
                               staff_id=session['user_id'], role=session['role'],
                               area=session['area'], patient=patient_list)

    # return render_template('index.html')

    # @app.route('/InterpretableEval')
    # def InterpretableEval():
    #     return render_template('InterpretableEval/index.html')

    app.register_blueprint(auth.bp)
    app.register_blueprint(emergency_nurse.bp)
    app.register_blueprint(ward_nurse.bp)
    # app.register_blueprint(calculation_F1.bp)

    return app
