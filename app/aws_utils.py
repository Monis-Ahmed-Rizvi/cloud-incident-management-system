import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from app import db
from app.models import AWSResource

def init_aws(app):
    app.config['AWS_CLIENT'] = boto3.client('ec2',
        aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'],
        region_name=app.config['AWS_REGION']
    )

def update_aws_resources(app):
    ec2 = app.config['AWS_CLIENT']
    try:
        response = ec2.describe_instances()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                resource = AWSResource.query.filter_by(resource_id=instance['InstanceId']).first()
                if not resource:
                    resource = AWSResource(
                        resource_id=instance['InstanceId'],
                        resource_type='EC2',
                        region=instance['Placement']['AvailabilityZone'][:-1],
                        status=instance['State']['Name'],
                        instance_type=instance['InstanceType'],
                        launch_time=instance['LaunchTime']
                    )
                    db.session.add(resource)
                else:
                    resource.status = instance['State']['Name']
                    resource.instance_type = instance['InstanceType']
                    resource.launch_time = instance['LaunchTime']
                    resource.last_updated = datetime.utcnow()
        db.session.commit()
    except ClientError as e:
        app.logger.error(f"An error occurred while updating AWS resources: {e}")
    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {e}")

