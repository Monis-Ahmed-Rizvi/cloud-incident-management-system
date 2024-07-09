from flask import Blueprint, render_template, flash, redirect, url_for, current_app
from flask_login import login_required
from app.models import AWSResource
from app.aws_utils import update_aws_resources

bp = Blueprint('aws_resources', __name__)

@bp.route('/aws_resources')
@login_required
def list_aws_resources():
    resources = AWSResource.query.all()
    return render_template('aws_resources.html', resources=resources)

@bp.route('/update_resources')
@login_required
def update_aws_resources_view():
    update_aws_resources(current_app)
    flash('AWS resources updated successfully.')
    return redirect(url_for('aws_resources.list_aws_resources'))
