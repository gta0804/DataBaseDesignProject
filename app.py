from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from entry import db
from auth import bp as auth_bp
from emergency_nurse import bp as emergency_nurse_bp
from ward_nurse import bp as ward_nurse_bp
from doctor import bp as doctor_bp
from head_nurse import bp as head_nurse_bp

sql_select_staff = 'SELECT * from  staff WHERE name=%s'
sql_select_staff_area = 'SELECT * from  staff_area WHERE staff_id=%s'
sql_select_patient = 'SELECT * from  patient WHERE nurse_id=%s'
sql_select_patient_tempare = 'SELECT * from  temperature_test WHERE patient_id=%s'
sql_select_patient_nucleic = 'SELECT * from  nucleic_test WHERE patient_id=%s'
sql_select_patient_symptoms = 'SELECT * from  symptoms WHERE patient_id=%s'
sql_select_patient_area = 'SELECT * from patient_area WHERE patient_id=%s'
sql_insert_new_patient="INSERT INTO patient( \
       name, gender, address, state_of_illness) \
       VALUES (%s, %s, %s, %s )"

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
        from util import is_patient_discharged, get_patient_area, get_symptoms, get_temperature, get_staff_area
        area = get_staff_area(session['user_name'])
        if session["role"] == 'doctor' or session["role"] == 'head_nurse':
            sql = "select * from patient natural join patient_area where patient_area.area =%s"
            cursor.execute(sql, area)
        elif session["role"] == "ward_nurse":
            sql = "select * from patient natural join patient_area where nurse_id =%s"
            cursor.execute(sql, session["user_id"])
        else:
            sql = "select * from patient natural left outer join patient_area"
            cursor.execute(sql)
        raw_patient_list = cursor.fetchall()
        patient_list = []

        for patient in raw_patient_list:
            patient_id = patient['patient_id']
            list = []
            list.append(patient_id)
            list.append(patient['name'])
            list.append(patient['gender'])
            list.append(patient['address'])
            list.append(get_temperature(patient_id))
            list.append(patient['life_status'])
            list.append(patient['state_of_illness'])
            list.append(patient["symptom"])
            list.append(get_patient_area(patient_id))
            list.append(is_patient_discharged(patient_id))
            list.append(patient["area"])
            patient_list.append(list)

        return render_template('all_patient.html', name=session['user_name'],
                               staff_id=session['user_id'], role=session['role'],
                               area=get_staff_area(session['user_name']), patients=patient_list)

    # return render_template('index.html')

    # @app.route('/InterpretableEval')
    # def InterpretableEval():
    #     return render_template('InterpretableEval/index.html')

    app.register_blueprint(auth_bp)
    app.register_blueprint(emergency_nurse_bp)
    app.register_blueprint(ward_nurse_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(head_nurse_bp)
    # app.register_blueprint(calculation_F1.bp)

    return app


if __name__ == "__main__":
    db.create_all()
    app = create_app()
    bootstrap = Bootstrap(app)
    app.run()