from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy import text

from config import Config
from models import db
from routes.auth import auth_bp
from routes.students import students_bp
from routes.export import export_bp
from routes.admin import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app, origins=app.config["ALLOWED_ORIGINS"], supports_credentials=True)

    app.register_blueprint(auth_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(export_bp)
    app.register_blueprint(admin_bp)

    @app.get("/api/health")
    def health():
        try:
            db.session.execute(text("SELECT 1"))
            return jsonify({"status": "ok", "db": "ok"}), 200
        except Exception:
            return jsonify({"status": "ok", "db": "unreachable"}), 200

    return app


app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # creates tables in Supabase Postgres if they don't exist yet
    app.run(debug=True, port=5000)
