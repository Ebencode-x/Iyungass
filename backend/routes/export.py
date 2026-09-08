import io
from flask import Blueprint, send_file
from openpyxl import Workbook
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from models import Student

export_bp = Blueprint("export", __name__, url_prefix="/api/export")

STUDENT_COLUMNS = [
    ("admission_number", "Admission No."),
    ("name", "Name"),
    ("form_level", "Form"),
    ("gender", "Gender"),
    ("guardian_name", "Guardian"),
    ("guardian_phone", "Guardian Phone"),
]


def _student_rows():
    students = Student.query.order_by(Student.form_level, Student.name).all()
    return [[getattr(s, field) or "" for field, _ in STUDENT_COLUMNS] for s in students]


@export_bp.get("/students/pdf")
def export_students_pdf():
    rows = _student_rows()
    headers = [label for _, label in STUDENT_COLUMNS]

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, title="Students Report")
    styles = getSampleStyleSheet()

    elements = [
        Paragraph("Iyunga Technical Secondary School - Students Report", styles["Title"]),
        Spacer(1, 12),
    ]

    table = Table([headers] + rows, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e2327")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.whitesmoke]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)

    return send_file(buffer, mimetype="application/pdf", as_attachment=True, download_name="students_report.pdf")


@export_bp.get("/students/xlsx")
def export_students_xlsx():
    rows = _student_rows()
    headers = [label for _, label in STUDENT_COLUMNS]

    wb = Workbook()
    ws = wb.active
    ws.title = "Students"
    ws.append(headers)
    for row in rows:
        ws.append(row)

    for cell in ws[1]:
        cell.font = cell.font.copy(bold=True)
    for col in ws.columns:
        max_len = max(len(str(c.value)) if c.value is not None else 0 for c in col)
        ws.column_dimensions[col[0].column_letter].width = max_len + 4

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="students_report.xlsx",
    )
