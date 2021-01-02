from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from entry import db

bp = Blueprint('ward_nurse', __name__, url_prefix='/emergency_nurse')


@bp.route("/report",methods=("GET","POST"))
def report():
    return render_template("ward_nurse/report.html", patient_id=2, name="张三")