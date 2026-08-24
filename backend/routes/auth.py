from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Student

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def generate_admission_number():
    year = datetime.utcnow().year
    count = Student.query.filter(
        Student.admission_number.like(f"IY-{year}-%")
    ).count() + 1
    return f"IY-{year}-{count:04d}"


@auth_bp.post("/register")
def register():
    data = request.get_json(force=True) or {}

    required = ["name", "dob", "gender", "form_level", "password",
                "guardian_name", "guardian_phone"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    if len(data["password"]) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    guardian_email = (data.get("guardian_email") or "").strip() or None
    if guardian_email and Student.query.filter_by(guardian_email=guardian_email).first():
        return jsonify({"error": "That guardian email is already linked to another account"}), 409

    try:
        dob = datetime.strptime(data["dob"], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "dob must be YYYY-MM-DD"}), 400

    student = Student(
        admission_number=generate_admission_number(),
        name=data["name"].strip(),
        dob=dob,
        gender=data["gender"],
        form_level=data["form_level"],
        prev_school=(data.get("prev_school") or "").strip() or None,
        guardian_name=data["guardian_name"].strip(),
        guardian_phone=data["guardian_phone"].strip(),
        guardian_email=guardian_email,
    )
    student.set_password(data["password"])

    db.session.add(student)
    db.session.commit()

    return jsonify({"message": "Application submitted", "student": student.to_dict()}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json(force=True) or {}
    identifier = (data.get("identifier") or "").strip()
    password = data.get("password") or ""

    if not identifier or not password:
        return jsonify({"error": "identifier and password are required"}), 400

    student = Student.query.filter(
        db.func.lower(Student.admission_number) == identifier.lower()
    ).first()
    if not student and "@" in identifier:
        student = Student.query.filter(
            db.func.lower(Student.guardian_email) == identifier.lower()
        ).first()

    if not student or not student.check_password(password):
        return jsonify({"error": "No matching account found. Check your admission number and password."}), 401

    return jsonify({"message": "Login successful", "student": student.to_dict()}), 200
