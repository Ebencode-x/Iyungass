from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from models import db
from routes.auth import auth_bp
from routes.students import students_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app, origins=app.config["ALLOWED_ORIGINS"], supports_credentials=True)

    app.register_blueprint(auth_bp)
    app.register_blueprint(students_bp)

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"}), 200

    return app


app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # creates tables in Supabase Postgres if they don't exist yet
    app.run(debug=True, port=5000)
