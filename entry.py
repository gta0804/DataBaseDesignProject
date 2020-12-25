from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from flask import Flask, render_template
import auth as auth
import emergency_nurse as emergency_nurse
import ward_nurse as ward_nurse


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
        SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:password@127.0.0.1:3306/pj?charset=utf8',
        # 密码123456xy 启动mysql：sudo mysql.server start.mysql -u root -p
        SQLALCHEMY_COMMIT_ON_TEARDOWN=True,
        SQLALCHEMY_POOL_SIZE=5,
        SQLALCHEMY_POOL_TIMEOUT=15,
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    db.init_app(app)

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

    # return render_template('index.html')

    # @app.route('/InterpretableEval')
    # def InterpretableEval():
    #     return render_template('InterpretableEval/index.html')

    app.register_blueprint(auth.bp)
    app.register_blueprint(emergency_nurse.bp)
    app.register_blueprint(ward_nurse.bp)
    # app.register_blueprint(calculation_F1.bp)

    return app


