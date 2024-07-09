from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import User, Incident
from app import db
from app.decorators import role_required

bp = Blueprint('admin', __name__)

@bp.route('/admin_dashboard')
@login_required
@role_required('admin')
def admin_dashboard():
    users = User.query.all()
    incidents = Incident.query.order_by(Incident.date_reported.desc()).all()
    return render_template('admin_dashboard.html', title='Admin Dashboard', users=users, incidents=incidents)