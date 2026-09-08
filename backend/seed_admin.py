from app import app
from models import db, Admin

with app.app_context():
    db.create_all()
    if not Admin.query.filter_by(username="admin").first():
        a = Admin(username="admin", name="School Admin")
        a.set_password("ChangeMe123!")
        db.session.add(a)
        db.session.commit()
        print("Admin created: username=admin password=ChangeMe123!")
    else:
        print("Admin 'admin' already exists")
