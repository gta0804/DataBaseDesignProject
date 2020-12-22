from flask import Flask, render_template,sessions
from flask_bootstrap import Bootstrap
from entry import create_app, db
app = create_app()
bootstrap = Bootstrap(app)

if __name__ == "__main__":
    db.create_all()
    app.run()


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
    return render_template("all_patient.html",role=role,name=name)


@app.route("/show_login")
def show():
    return render_template("auth/login.html")


@app.route("/logout")
def logout():
    sessions["name"] = None
    sessions["role"] = None
    return render_template("auth/login.html")