from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from app import db, mail
from app.models import Incident, AWSResource
from app.forms import IncidentForm
from datetime import datetime
from flask_mail import Message

bp = Blueprint('incidents', __name__)

@bp.route('/report_incident', methods=['GET', 'POST'])
@login_required
def report_incident():
    form = IncidentForm()
    if form.validate_on_submit():
        incident = Incident(
            title=form.title.data,
            description=form.description.data,
            severity=form.severity.data,
            aws_service=form.aws_service.data,
            author=current_user,
            date_reported=datetime.utcnow()
        )
        db.session.add(incident)
        db.session.commit()
        flash('Incident reported successfully.')
        send_notification_email(incident)  # Send email notification
        return redirect(url_for('incidents.list_incidents'))
    return render_template('report_incident.html', title='Report Incident', form=form)

@bp.route('/incidents')
@login_required
def list_incidents():
    incidents = Incident.query.order_by(Incident.date_reported.desc()).all()
    return render_template('list_incidents.html', title='Incident List', incidents=incidents)

@bp.route('/incident/<int:id>')
@login_required
def incident_detail(id):
    incident = Incident.query.get_or_404(id)
    return render_template('incident_detail.html', title='Incident Detail', incident=incident)

@bp.route('/incident/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_incident(id):
    incident = Incident.query.get_or_404(id)
    form = IncidentForm()
    if form.validate_on_submit():
        incident.title = form.title.data
        incident.description = form.description.data
        incident.severity = form.severity.data
        incident.aws_service = form.aws_service.data
        db.session.commit()
        flash('Incident has been updated.')
        return redirect(url_for('incidents.incident_detail', id=incident.id))
    elif request.method == 'GET':
        form.title.data = incident.title
        form.description.data = incident.description
        form.severity.data = incident.severity
        form.aws_service.data = incident.aws_service
    return render_template('report_incident.html', title='Update Incident', form=form)

@bp.route('/incident/<int:id>/delete', methods=['POST'])
@login_required
def delete_incident(id):
    incident = Incident.query.get_or_404(id)
    if current_user.role.name != 'admin':
        flash('You do not have permission to delete this incident.')
        return redirect(url_for('incidents.incident_detail', id=id))
    db.session.delete(incident)
    db.session.commit()
    flash('Incident has been deleted.')
    return redirect(url_for('admin.admin_dashboard'))


@bp.route('/aws_resources')
@login_required
def aws_resources():
    resources = AWSResource.query.order_by(AWSResource.last_updated.desc()).all()
    return render_template('aws_resources.html', title='AWS Resources', resources=resources)

def send_notification_email(incident):
    msg = Message('New Incident Reported',
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[incident.author.email])
    msg.body = f'''
    Dear {incident.author.username},

    A new incident has been reported:
    
    Title: {incident.title}
    Description: {incident.description}
    Severity: {incident.severity}
    AWS Service: {incident.aws_service}
    
    Regards,
    Incident Management System
    '''
    mail.send(msg)
