from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from models import Staff
from entry import db

bp = Blueprint('emergency_nurse', __name__, url_prefix='/emergency_nurse')

@bp.route('/new_patient', methods=('GET', 'POST'))

def new_patient():
    return render_template("emergency_nurse/new_patient.html", role='emergency_nurse',name='12345')