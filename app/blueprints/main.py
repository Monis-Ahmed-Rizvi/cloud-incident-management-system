from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.forms import ProfileForm
from app.decorators import role_required
from app.models import User, Incident  # Add this import

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home')

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('profile.html', title='Profile', form=form)

@bp.route('/admin_dashboard')
@login_required
@role_required('admin')
def admin_dashboard():
    users = User.query.all()
    incidents = Incident.query.order_by(Incident.date_reported.desc()).all()
    return render_template('admin_dashboard.html', title='Admin Dashboard', users=users, incidents=incidents)