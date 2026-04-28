from app.models import db
from datetime import datetime

class Course(db.Model):
    """
    Course/Orientasi model
    """
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Admin yang membuat
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    materials = db.relationship('Material', backref='course', lazy=True, cascade='all, delete-orphan')
    student_courses = db.relationship('StudentCourse', backref='course', lazy=True, cascade='all, delete-orphan')
    visit_proofs = db.relationship('VisitProof', backref='course', lazy=True)
    certificates = db.relationship('Certificate', backref='course', lazy=True)
    admin = db.relationship('User', backref='created_courses', foreign_keys=[created_by])
    
    def __repr__(self):
        return f'<Course {self.id} - {self.title}>'
