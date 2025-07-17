import bcrypt
import jwt
import datetime
from flask import current_app
from sqlalchemy.orm import Session
from models import user  # your SQLAlchemy model

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def hash_password(self, plain_password):
        return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, plain_password, hashed_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def create_user(self, first_name, last_name, email, password, role="participant"):
        existing_user = self.db.query(user).filter_by(email=email).first()
        if existing_user:
            raise ValueError("User already exists")

        hashed_pwd = self.hash_password(password)
        user = user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_pwd,
            role=role,
            status="active"
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate_user(self, email, password):
        user = self.db.query(user).filter_by(email=email).first()
        if not user:
            raise ValueError("User not found")
        if not self.verify_password(password, user.password):
            raise ValueError("Invalid credentials")
        return user

    def generate_jwt(self, user_id, email):
        payload = {
            'user_id': user_id,
            'email': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, current_app.config['JWT_SECRET'], algorithm='HS256')
        return token

    def decode_jwt(self, token):
        try:
            payload = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

    def get_user_by_token(self, token):
        payload = self.decode_jwt(token)
        user = self.db.query(user).filter_by(id=payload['user_id']).first()
        return user
