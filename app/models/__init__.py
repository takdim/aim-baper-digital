from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.user import User
from app.models.course import Course
from app.models.student_course import StudentCourse
from app.models.material import Material
from app.models.evaluation import Evaluation
from app.models.student_evaluation import StudentEvaluation
from app.models.visit_proof import VisitProof
from app.models.certificate import Certificate

__all__ = [
    'db',
    'User',
    'Course',
    'StudentCourse',
    'Material',
    'Evaluation',
    'StudentEvaluation',
    'VisitProof',
    'Certificate'
]
