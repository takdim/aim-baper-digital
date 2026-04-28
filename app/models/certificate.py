from app.models import db
from datetime import datetime

class Certificate(db.Model):
    """
    Model untuk Sertifikat
    """
    __tablename__ = 'certificates'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    certificate_path = db.Column(db.String(255), nullable=False)  # Path/URL sertifikat PDF atau gambar
    issued_at = db.Column(db.DateTime, default=datetime.utcnow)
    downloaded_at = db.Column(db.DateTime, nullable=True)
    
    __table_args__ = (
        db.UniqueConstraint('student_id', 'course_id', name='uq_certificate'),
    )
    
    def __repr__(self):
        return f'<Certificate {self.id} - {self.student_id}>'
