from flask import Blueprint, request, jsonify
from models import db, Admin, Student
from auth_utils import admin_required, generate_admin_token

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.post("/login")
def admin_login():
    """Read (auth) - Admin logs in."""
    data = request.get_json(force=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    admin = Admin.query.filter(db.func.lower(Admin.username) == username.lower()).first()
    if not admin or not admin.check_password(password):
        return jsonify({"error": "Invalid admin credentials"}), 401

    token = generate_admin_token(admin.id)
    return jsonify({"message": "Login successful", "admin": admin.to_dict(), "token": token}), 200


@admin_bp.get("/students")
@admin_required
def list_students():
    """Read - Admin views all student applications, optional ?status=pending filter."""
    status = request.args.get("status")
    query = Student.query
    if status:
        query = query.filter_by(status=status)
    students = query.order_by(Student.created_at.desc()).all()
    return jsonify([s.to_dict() for s in students]), 200


@admin_bp.put("/students/<admission_number>/status")
@admin_required
def update_student_status(admission_number):
    """Update - Admin approves or rejects a student's application."""
    student = Student.query.filter_by(admission_number=admission_number).first_or_404(
        description="No student found with that admission number"
    )
    data = request.get_json(force=True) or {}
    new_status = data.get("status")

    if new_status not in ("pending", "approved", "rejected"):
        return jsonify({"error": "status must be pending, approved, or rejected"}), 400

    student.status = new_status
    db.session.commit()
    return jsonify({"message": "Status updated", "student": student.to_dict()}), 200


@admin_bp.delete("/students/<admission_number>")
@admin_required
def delete_application(admission_number):
    """Delete - Admin removes a student application entirely."""
    student = Student.query.filter_by(admission_number=admission_number).first_or_404(
        description="No student found with that admission number"
    )
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Application deleted"}), 200
