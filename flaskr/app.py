from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.entry import create_app,db

app = create_app()


'''
@app.route('/')
def hello_world():
	# return 'Hello, World!'
	return render_template('index.html')
'''

if __name__ == "__main__":
    db.create_all()
    app.run()