from database import db
from sqlalchemy import UniqueConstraint
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # store hashed password
    role = db.Column(db.String(50), nullable=False)       # e.g., Instructor, Manager, HR Admin, Participant
    status = db.Column(db.String(50), default='pending')  # pending, approved, rejected
    otp = db.Column(db.String(6), nullable=True)          # for email/OTP verification
    auth_session_token = db.Column(db.String(200), unique=True, nullable=True)

    __table_args__ = (
        UniqueConstraint('auth_session_token', name='uq_user_auth_session_token'),
    )

    def __init__(self, first_name, last_name, email, password, role, status='pending'):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.role = role
        self.status = status

    def get_auth_session_token(self):
        return self.auth_session_token
