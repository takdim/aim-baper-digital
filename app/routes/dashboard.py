from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
from app.routes import dashboard_bp
from app.models import db, Course, StudentCourse
from app.utils.decorators import student_required

@dashboard_bp.route('/')
@student_required
def index():
    """Dashboard - tampilkan daftar course yang tersedia"""
    page = request.args.get('page', 1, type=int)
    courses = Course.query.filter_by(is_active=True).paginate(page=page, per_page=10)
    
    # Get enrolled courses untuk current user
    enrolled_courses = StudentCourse.query.filter_by(student_id=current_user.id).all()
    enrolled_course_ids = [ec.course_id for ec in enrolled_courses]
    enrolled_course_map = {ec.course_id: ec for ec in enrolled_courses}
    in_progress_count = sum(1 for ec in enrolled_courses if ec.status == 'in_progress')
    completed_count = sum(1 for ec in enrolled_courses if ec.status == 'completed' or ec.progress >= 100)
    
    return render_template('dashboard/index.html', 
                         courses=courses, 
                         enrolled_course_ids=enrolled_course_ids,
                         enrolled_course_map=enrolled_course_map,
                         enrolled_count=len(enrolled_courses),
                         in_progress_count=in_progress_count,
                         completed_count=completed_count)
