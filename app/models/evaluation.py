from app.models import db
from datetime import datetime

class Evaluation(db.Model):
    """
    Model untuk Evaluasi/Kuis di setiap Materi
    """
    __tablename__ = 'evaluations'
    
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), default='multiple_choice', nullable=False)  # 'multiple_choice', 'essay'
    option_a = db.Column(db.Text, nullable=True)  # Untuk multiple choice
    option_b = db.Column(db.Text, nullable=True)
    option_c = db.Column(db.Text, nullable=True)
    option_d = db.Column(db.Text, nullable=True)
    correct_answer = db.Column(db.String(1), nullable=True)  # 'A', 'B', 'C', 'D' atau untuk essay bisa NULL
    order = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student_evaluations = db.relationship('StudentEvaluation', backref='evaluation', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Evaluation {self.id} - {self.question[:50]}>'
