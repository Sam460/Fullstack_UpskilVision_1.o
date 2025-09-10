import os
from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth
from routes.course_routes import courses
from routes.audit_routes import audit


def create_app():
    app = Flask(__name__)

    # Define allowed origins: local + deployed Vercel frontend
    allowed_origins = [
        "http://localhost:5173",
        os.getenv("FRONTEND_URL", "").rstrip("/")  # e.g., https://your-frontend.vercel.app
    ]

    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": allowed_origins,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        },
        r"/auth/*": {
            "origins": allowed_origins,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        },
        r"/courses/*": {
            "origins": allowed_origins,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    # Register blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(courses, url_prefix='/courses')
    app.register_blueprint(audit, url_prefix='/api/audit')

    @app.after_request
    def after_request(response):
        origin = response.headers.get("Access-Control-Allow-Origin")
        # If no origin is set, allow local + vercel frontend
        if not origin:
            response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
            if os.getenv("FRONTEND_URL"):
                response.headers.add("Access-Control-Allow-Origin", os.getenv("FRONTEND_URL"))
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response

    return app


app = create_app()

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True, host='127.0.0.1', port=5000)
