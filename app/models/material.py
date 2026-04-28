from app.models import db
from datetime import datetime

class Material(db.Model):
    """
    Model untuk Materi dalam Course
    """
    __tablename__ = 'materials'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, nullable=False)  # Urutan materi
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    evaluations = db.relationship('Evaluation', backref='material', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Material {self.id} - {self.title}>'
