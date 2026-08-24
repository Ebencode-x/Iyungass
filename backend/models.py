from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    # Login identity
    admission_number = db.Column(db.String(30), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # Student details (register.html "Student details" section)
    name = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    form_level = db.Column(db.String(20), nullable=False)   # "Form 1".."Form 6"
    prev_school = db.Column(db.String(150))

    # Guardian details
    guardian_name = db.Column(db.String(120), nullable=False)
    guardian_phone = db.Column(db.String(20), nullable=False)
    guardian_email = db.Column(db.String(120), index=True)  # optional, doubles as alt login identifier

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)

    def to_dict(self):
        return {
            "admission_number": self.admission_number,
            "name": self.name,
            "dob": self.dob.isoformat() if self.dob else None,
            "gender": self.gender,
            "form_level": self.form_level,
            "prev_school": self.prev_school,
            "guardian_name": self.guardian_name,
            "guardian_phone": self.guardian_phone,
            "guardian_email": self.guardian_email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
