from app.models import db
from datetime import datetime

class StudentCourse(db.Model):
    """
    Model untuk enrollment - hubungan antara Student dan Course
    """
    __tablename__ = 'student_courses'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    status = db.Column(db.String(20), default='enrolled', nullable=False)  # 'enrolled', 'in_progress', 'completed'
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    progress = db.Column(db.Float, default=0.0)  # Persentase progress 0-100
    
    __table_args__ = (
        db.UniqueConstraint('student_id', 'course_id', name='uq_student_course'),
    )
    
    def __repr__(self):
        return f'<StudentCourse {self.student_id} - {self.course_id}>'
