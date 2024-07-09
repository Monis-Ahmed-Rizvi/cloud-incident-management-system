from app import create_app, db, socketio
from app.models import User, Incident, Role
from app.tasks import background_task
import threading
import os

app = create_app()

def start_background_tasks(app):
    def run_task():
        with app.app_context():
            background_task()

    aws_thread = threading.Thread(target=run_task)
    aws_thread.start()
    return aws_thread

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This ensures all tables are created
        
        # Create roles if they don't exist
        roles = ['user', 'admin', 'support']
        for role_name in roles:
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                role = Role(name=role_name)
                db.session.add(role)
        db.session.commit()
        print("Roles checked/created")

    aws_thread = start_background_tasks(app)
    
    debug = os.environ.get('FLASK_DEBUG', 'True') == 'True'
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    try:
        socketio.run(app, debug=debug, host=host, port=port)
    finally:
        aws_thread.join(timeout=1)