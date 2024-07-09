from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_socketio import SocketIO
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
mail = Mail()
socketio = SocketIO()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    socketio.init_app(app)

    from app.blueprints import auth, main, incidents, chat, aws_resources, admin
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(incidents.bp)
    app.register_blueprint(chat.bp)
    app.register_blueprint(aws_resources.bp)
    app.register_blueprint(admin.bp)  # Register admin blueprint

    from app.models import User, Role
    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.aws_utils import init_aws
    init_aws(app)

    from app.chatbot import init_chatbot
    init_chatbot(app)

    @app.route('/update_resources')
    def update_resources():
        from app.aws_utils import update_aws_resources
        update_aws_resources(app)
        return redirect(url_for('aws_resources.list_aws_resources'))

    @app.cli.command("create-roles")
    def create_roles():
        try:
            roles = ['user', 'admin', 'support']
            for role_name in roles:
                role = Role.query.filter_by(name=role_name).first()
                if role is None:
                    role = Role(name=role_name)
                    db.session.add(role)
            db.session.commit()
            print("Roles created successfully")
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred while creating roles: {str(e)}")

    return app
