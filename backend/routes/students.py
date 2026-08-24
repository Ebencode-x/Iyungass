from flask import Blueprint, request, jsonify
from models import db, Student

students_bp = Blueprint("students", __name__, url_prefix="/api/students")


def _get_or_404(admission_number):
    return Student.query.filter_by(admission_number=admission_number).first_or_404(
        description="No student found with that admission number"
    )


@students_bp.get("/<admission_number>")
def get_student(admission_number):
    student = _get_or_404(admission_number)
    return jsonify(student.to_dict()), 200


@students_bp.put("/<admission_number>")
def update_profile(admission_number):
    """Settings -> 'Edit profile' form: name, prev_school, guardian_phone, guardian_email."""
    student = _get_or_404(admission_number)
    data = request.get_json(force=True) or {}

    name = (data.get("name") or "").strip()
    guardian_phone = (data.get("guardian_phone") or "").strip()
    if not name or not guardian_phone:
        return jsonify({"error": "name and guardian_phone are required"}), 400

    guardian_email = (data.get("guardian_email") or "").strip() or None
    if guardian_email:
        clash = Student.query.filter(
            Student.guardian_email == guardian_email,
            Student.admission_number != admission_number,
        ).first()
        if clash:
            return jsonify({"error": "That guardian email is already linked to another account"}), 409

    student.name = name
    student.prev_school = (data.get("prev_school") or "").strip() or None
    student.guardian_phone = guardian_phone
    student.guardian_email = guardian_email

    db.session.commit()
    return jsonify({"message": "Profile updated", "student": student.to_dict()}), 200


@students_bp.put("/<admission_number>/password")
def change_password(admission_number):
    student = _get_or_404(admission_number)
    data = request.get_json(force=True) or {}

    current = data.get("current_password") or ""
    new = data.get("new_password") or ""

    if not student.check_password(current):
        return jsonify({"error": "Incorrect current password"}), 401
    if len(new) < 8:
        return jsonify({"error": "New password must be at least 8 characters"}), 400

    student.set_password(new)
    db.session.commit()
    return jsonify({"message": "Password updated"}), 200


@students_bp.delete("/<admission_number>")
def delete_account(admission_number):
    student = _get_or_404(admission_number)
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Account deleted"}), 200
