from app.models import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """
    User model untuk Student dan Admin
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    faculty = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='student', nullable=False)  # 'student', 'admin'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student_courses = db.relationship('StudentCourse', backref='student', lazy=True, foreign_keys='StudentCourse.student_id')
    student_evaluations = db.relationship('StudentEvaluation', backref='student', lazy=True)
    visit_proofs = db.relationship('VisitProof', backref='student', lazy=True, foreign_keys='VisitProof.student_id')
    certificates = db.relationship('Certificate', backref='student', lazy=True)
    
    def set_password(self, password):
        """Hash dan set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifikasi password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.nim} - {self.name}>'
