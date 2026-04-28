from app.models import db
from datetime import datetime

class CertificateTemplate(db.Model):
    """
    Model untuk template dan settings sertifikat
    """
    __tablename__ = 'certificate_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    
    # Settings sertifikat
    certificate_number_format = db.Column(db.String(100), nullable=False)  # Misal: {year}/UN4.1.1.5/TA.01.02/{seq}
    current_sequence = db.Column(db.Integer, default=1)  # Nomor urut terakhir
    year = db.Column(db.Integer, default=datetime.utcnow().year)
    
    # Data kepala perpustakaan
    head_name = db.Column(db.String(200), nullable=False)  # Nama kepala perpustakaan
    head_nip = db.Column(db.String(50), nullable=False)  # NIP kepala perpustakaan
    head_title = db.Column(db.String(100), default='Kepala Perpustakaan')  # Gelar/titel
    
    # Template design
    institution_name = db.Column(db.String(200), default='Universitas Hasanuddin')
    institution_npp = db.Column(db.String(50), default='NIP: 7034060100001')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    course = db.relationship('Course', backref='certificate_template', uselist=False)
    
    def get_next_certificate_number(self):
        """Generate nomor sertifikat berikutnya"""
        self.current_sequence += 1
        return self.certificate_number_format.format(
            year=self.year,
            seq=str(self.current_sequence).zfill(5)
        )
    
    def __repr__(self):
        return f'<CertificateTemplate {self.course_id}>'
