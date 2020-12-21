from flask import Flask, render_template
from flask_bootstrap import Bootstrap
app = Flask(__name__)

bootstrap = Bootstrap(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/user/showAll")
def show_all():
    patient1 = {'name': '张三','gender': '男','age': 26,'address': '上海市虹口区松花江路2500号', 'temperature': '36.5'}
    patient2 = {'name': '李四','gender': '女','age': 29,'address': '上海市虹口区松花江路2500号', 'temperature': '38.9'}
    patients = [patient1,patient2]
    role = 'doctor'
    name = '李四'
    return render_template("all_patient.html", patients=patients, role=role, name=name)


@app.route("/doctor/nav")
def doctor_nav():
    role = 'doctor'
    name = '李四'
    return render_template("all_patient.html", role=role, name=name)
