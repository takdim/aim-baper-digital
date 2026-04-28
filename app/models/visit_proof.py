from app.models import db
from datetime import datetime

class VisitProof(db.Model):
    """
    Model untuk Bukti Kunjungan ke Perpustakaan
    """
    __tablename__ = 'visit_proofs'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    photo_path = db.Column(db.String(255), nullable=False)  # Path/URL foto
    status = db.Column(db.String(20), default='pending', nullable=False)  # 'pending', 'approved', 'rejected'
    notes = db.Column(db.Text, nullable=True)  # Catatan dari admin
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Admin yang verifikasi
    verified_at = db.Column(db.DateTime, nullable=True)
    
    __table_args__ = (
        db.UniqueConstraint('student_id', 'course_id', name='uq_visit_proof'),
    )
    
    verifier = db.relationship('User', foreign_keys=[verified_by], backref='verified_proofs')
    
    def __repr__(self):
        return f'<VisitProof {self.id} - {self.status}>'
