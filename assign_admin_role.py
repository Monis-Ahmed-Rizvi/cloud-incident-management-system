from app import create_app, db
from app.models import User, Role

app = create_app()

with app.app_context():
    user_email = 'munisc18@gmail.com'
    
    user = User.query.filter_by(email=user_email).first()
    if user:
        admin_role = Role.query.filter_by(name='admin').first()
        if admin_role:
            if admin_role not in user.roles:
                user.roles.append(admin_role)
                db.session.commit()
                print(f"Admin role assigned to user {user_email} successfully.")
            else:
                print(f"User {user_email} already has the admin role.")
        else:
            print("Admin role not found. Creating it now.")
            admin_role = Role(name='admin')
            db.session.add(admin_role)
            db.session.commit()
            user.roles.append(admin_role)
            db.session.commit()
            print(f"Admin role created and assigned to user {user_email}.")
        
        print(f"User roles: {[role.name for role in user.roles]}")
        print(f"Has admin role: {user.has_role('admin')}")
    else:
        print(f"User with email {user_email} not found.")