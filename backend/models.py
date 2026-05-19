from datetime import datetime, timezone
from .extensions import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    analyses = db.relationship('AnalysisHistory', backref='user', lazy=True, cascade='all, delete-orphan')

class AnalysisHistory(db.Model):
    __tablename__ = 'analysis_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    input_data = db.Column(db.JSON, nullable=False)
    prediction = db.Column(db.String(255), nullable=False)
    confidence = db.Column(db.Float, nullable=True)
    probabilities = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
