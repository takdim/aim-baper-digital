from app.models import db
from datetime import datetime

class StudentEvaluation(db.Model):
    """
    Model untuk jawaban/hasil evaluasi siswa
    """
    __tablename__ = 'student_evaluations'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    evaluation_id = db.Column(db.Integer, db.ForeignKey('evaluations.id'), nullable=False)
    answer = db.Column(db.String(255), nullable=False)  # Jawaban student (A, B, C, D untuk multiple choice, atau text untuk essay)
    is_correct = db.Column(db.Boolean, nullable=True)  # NULL untuk essay (menunggu verifikasi admin)
    score = db.Column(db.Float, nullable=True)  # Score untuk essay setelah diverifikasi
    answered_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('student_id', 'evaluation_id', name='uq_student_evaluation'),
    )
    
    def __repr__(self):
        return f'<StudentEvaluation {self.student_id} - {self.evaluation_id}>'
