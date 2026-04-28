from flask import Blueprint

# Define blueprints
home_bp = Blueprint('home', __name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
course_bp = Blueprint('course', __name__, url_prefix='/course')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Import routes untuk menghindari circular imports
from app.routes import home, auth, dashboard, course, admin
