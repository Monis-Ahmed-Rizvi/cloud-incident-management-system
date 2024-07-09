from app.aws_utils import update_aws_resources
import time
from flask import current_app

def background_task():
    while True:
        try:
            with current_app.app_context():
                update_aws_resources(current_app, current_app.extensions['sqlalchemy'].db)
        except Exception as e:
            current_app.logger.error(f"Error in background task: {str(e)}")
        time.sleep(300)  # Sleep for 5 minutes