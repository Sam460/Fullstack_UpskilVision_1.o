import os;
from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth
from routes.course_routes import courses
from routes.audit_routes import audit


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True, origins=[os.getenv("FRONTEND_URL")])
    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173","https://fullstack-upskil-vision-1-c8giitbmg.vercel.app"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        },
        r"/auth/*": {
            "origins": ["http://localhost:5173","https://fullstack-upskil-vision-1-c8giitbmg.vercel.app"],
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
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173', 'https://fullstack-upskil-vision-1-c8giitbmg.vercel.app')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    return app

app = create_app()

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True, host='127.0.0.1', port=5000)