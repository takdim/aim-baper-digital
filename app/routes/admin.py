from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user
from app.routes import admin_bp
from app.models import db, User, Course, Material, Evaluation, VisitProof, StudentCourse, Certificate, CertificateTemplate
from app.utils.decorators import admin_required, role_home
from datetime import datetime


def _next_material_order(course_id):
    """Hitung urutan materi berikutnya dalam sebuah course."""
    max_order = db.session.query(db.func.max(Material.order)).filter_by(course_id=course_id).scalar()
    return (max_order or 0) + 1


def _next_evaluation_order(material_id):
    """Hitung urutan evaluasi berikutnya dalam sebuah materi."""
    max_order = db.session.query(db.func.max(Evaluation.order)).filter_by(material_id=material_id).scalar()
    return (max_order or 0) + 1


def _parse_order(raw_value, fallback):
    """Parse input urutan dan fallback jika kosong/tidak valid."""
    try:
        order = int(raw_value)
        return order if order > 0 else fallback
    except (TypeError, ValueError):
        return fallback


def _populate_evaluation_from_form(evaluation, form):
    """Isi object evaluasi dari request form dan validasi dasar."""
    question = (form.get('question') or '').strip()
    question_type = form.get('question_type', 'multiple_choice')
    order = _parse_order(form.get('order'), _next_evaluation_order(evaluation.material_id))

    if not question:
        return 'Pertanyaan evaluasi harus diisi'

    if question_type not in ['multiple_choice', 'essay']:
        return 'Tipe evaluasi tidak valid'

    evaluation.question = question
    evaluation.question_type = question_type
    evaluation.order = order

    if question_type == 'multiple_choice':
        options = {
            'A': (form.get('option_a') or '').strip(),
            'B': (form.get('option_b') or '').strip(),
            'C': (form.get('option_c') or '').strip(),
            'D': (form.get('option_d') or '').strip(),
        }
        correct_answer = (form.get('correct_answer') or '').strip().upper()

        if not all(options.values()):
            return 'Semua pilihan jawaban A sampai D wajib diisi untuk evaluasi pilihan ganda'

        if correct_answer not in options:
            return 'Jawaban benar harus salah satu dari A, B, C, atau D'

        evaluation.option_a = options['A']
        evaluation.option_b = options['B']
        evaluation.option_c = options['C']
        evaluation.option_d = options['D']
        evaluation.correct_answer = correct_answer
    else:
        evaluation.option_a = None
        evaluation.option_b = None
        evaluation.option_c = None
        evaluation.option_d = None
        evaluation.correct_answer = None

    return None

# ==================== ADMIN DASHBOARD ====================
@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard dengan statistik"""
    total_users = User.query.count()
    total_students = User.query.filter_by(role='student').count()
    total_admins = User.query.filter_by(role='admin').count()
    total_courses = Course.query.count()
    active_courses = Course.query.filter_by(is_active=True).count()
    
    stats = {
        'total_users': total_users,
        'total_students': total_students,
        'total_admins': total_admins,
        'total_courses': total_courses,
        'active_courses': active_courses,
    }
    
    return render_template('admin/dashboard.html', stats=stats)

# ==================== USER MANAGEMENT ====================
@admin_bp.route('/users')
@admin_required
def users_list():
    """List semua users dengan filter"""
    page = request.args.get('page', 1, type=int)
    role_filter = request.args.get('role', 'all')
    search = request.args.get('search', '')
    
    query = User.query
    
    if role_filter != 'all':
        query = query.filter_by(role=role_filter)
    
    if search:
        query = query.filter(
            db.or_(
                User.name.ilike(f'%{search}%'),
                User.nim.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%')
            )
        )
    
    users = query.paginate(page=page, per_page=10)
    
    return render_template('admin/users_list.html', users=users, role_filter=role_filter, search=search)

@admin_bp.route('/users/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    """Buat user baru (admin atau student)"""
    if request.method == 'POST':
        nim = request.form.get('nim')
        name = request.form.get('name')
        faculty = request.form.get('faculty')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'student')
        
        # Validation
        if not all([nim, name, faculty, password]):
            flash('NIM, nama, fakultas, dan password harus diisi', 'danger')
            return redirect(url_for('admin.create_user'))
        
        if User.query.filter_by(nim=nim).first():
            flash('NIM sudah terdaftar', 'danger')
            return redirect(url_for('admin.create_user'))
        
        if email and User.query.filter_by(email=email).first():
            flash('Email sudah terdaftar', 'danger')
            return redirect(url_for('admin.create_user'))
        
        # Create user
        user = User(nim=nim, name=name, faculty=faculty, email=email, role=role)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'User berhasil dibuat: {name}', 'success')
        return redirect(url_for('admin.users_list'))
    
    return render_template('admin/create_user.html')

@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    """Edit user"""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.name = request.form.get('name', user.name)
        user.faculty = request.form.get('faculty', user.faculty)
        user.email = request.form.get('email', user.email)
        role = request.form.get('role')
        
        if role in ['student', 'admin']:
            user.role = role
        
        is_active = request.form.get('is_active') == 'on'
        user.is_active = is_active
        
        password = request.form.get('password')
        if password:
            user.set_password(password)
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash(f'User {user.name} berhasil diperbarui', 'success')
        return redirect(url_for('admin.users_list'))
    
    return render_template('admin/edit_user.html', user=user)

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    """Hapus user"""
    user = User.query.get_or_404(user_id)
    user_name = user.name
    
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {user_name} berhasil dihapus', 'success')
    return redirect(url_for('admin.users_list'))

# ==================== COURSE MANAGEMENT ====================
@admin_bp.route('/courses')
@admin_required
def courses_list():
    """List semua courses"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'all')
    search = request.args.get('search', '')
    
    query = Course.query
    
    if status_filter == 'active':
        query = query.filter_by(is_active=True)
    elif status_filter == 'inactive':
        query = query.filter_by(is_active=False)
    
    if search:
        query = query.filter(Course.title.ilike(f'%{search}%'))
    
    courses = query.paginate(page=page, per_page=10)
    
    return render_template('admin/courses_list.html', courses=courses, status_filter=status_filter, search=search)

@admin_bp.route('/courses/create', methods=['GET', 'POST'])
@admin_required
def create_course():
    """Buat course baru"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        if not title:
            flash('Judul course harus diisi', 'danger')
            return redirect(url_for('admin.create_course'))
        
        course = Course(
            title=title,
            description=description,
            created_by=current_user.id,
            is_active=True
        )
        
        db.session.add(course)
        db.session.commit()
        
        flash(f'Course "{title}" berhasil dibuat', 'success')
        return redirect(url_for('admin.courses_list'))
    
    return render_template('admin/create_course.html')

@admin_bp.route('/courses/<int:course_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_course(course_id):
    """Edit course"""
    course = Course.query.get_or_404(course_id)
    
    if request.method == 'POST':
        course.title = request.form.get('title', course.title)
        course.description = request.form.get('description', course.description)
        course.is_active = request.form.get('is_active') == 'on'
        course.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash(f'Course "{course.title}" berhasil diperbarui', 'success')
        return redirect(url_for('admin.courses_list'))
    
    return render_template('admin/edit_course.html', course=course)


@admin_bp.route('/courses/<int:course_id>/content')
@admin_required
def course_content(course_id):
    """Kelola materi dan evaluasi untuk sebuah course."""
    course = Course.query.get_or_404(course_id)
    materials = Material.query.filter_by(course_id=course.id).order_by(Material.order.asc(), Material.created_at.asc()).all()

    editing_material_id = request.args.get('edit_material', type=int)
    editing_evaluation_id = request.args.get('edit_evaluation', type=int)

    editing_material = None
    if editing_material_id:
        editing_material = Material.query.filter_by(id=editing_material_id, course_id=course.id).first()

    editing_evaluation = None
    if editing_evaluation_id:
        editing_evaluation = (
            Evaluation.query
            .join(Material)
            .filter(Evaluation.id == editing_evaluation_id, Material.course_id == course.id)
            .first()
        )

    return render_template(
        'admin/course_content.html',
        course=course,
        materials=materials,
        editing_material=editing_material,
        editing_evaluation=editing_evaluation,
    )


@admin_bp.route('/courses/<int:course_id>/materials/create', methods=['POST'])
@admin_required
def create_material(course_id):
    """Tambah materi baru ke course."""
    course = Course.query.get_or_404(course_id)
    title = (request.form.get('title') or '').strip()
    content = (request.form.get('content') or '').strip()
    order = _parse_order(request.form.get('order'), _next_material_order(course.id))

    if not title or not content:
        flash('Judul dan isi materi harus diisi', 'danger')
        return redirect(url_for('admin.course_content', course_id=course.id))

    material = Material(course_id=course.id, title=title, content=content, order=order)
    db.session.add(material)
    db.session.commit()

    flash(f'Materi "{title}" berhasil ditambahkan', 'success')
    return redirect(url_for('admin.course_content', course_id=course.id))


@admin_bp.route('/materials/<int:material_id>/update', methods=['POST'])
@admin_required
def update_material(material_id):
    """Perbarui materi course."""
    material = Material.query.get_or_404(material_id)
    title = (request.form.get('title') or '').strip()
    content = (request.form.get('content') or '').strip()
    order = _parse_order(request.form.get('order'), material.order)

    if not title or not content:
        flash('Judul dan isi materi harus diisi', 'danger')
        return redirect(url_for('admin.course_content', course_id=material.course_id, edit_material=material.id))

    material.title = title
    material.content = content
    material.order = order
    material.updated_at = datetime.utcnow()

    db.session.commit()

    flash(f'Materi "{title}" berhasil diperbarui', 'success')
    return redirect(url_for('admin.course_content', course_id=material.course_id))


@admin_bp.route('/materials/<int:material_id>/delete', methods=['POST'])
@admin_required
def delete_material(material_id):
    """Hapus materi course."""
    material = Material.query.get_or_404(material_id)
    course_id = material.course_id
    title = material.title

    db.session.delete(material)
    db.session.commit()

    flash(f'Materi "{title}" berhasil dihapus', 'success')
    return redirect(url_for('admin.course_content', course_id=course_id))


@admin_bp.route('/materials/<int:material_id>/evaluations/create', methods=['POST'])
@admin_required
def create_evaluation(material_id):
    """Tambah evaluasi ke materi."""
    material = Material.query.get_or_404(material_id)
    evaluation = Evaluation(material_id=material.id, order=_next_evaluation_order(material.id))
    error = _populate_evaluation_from_form(evaluation, request.form)

    if error:
        flash(error, 'danger')
        return redirect(url_for('admin.course_content', course_id=material.course_id))

    db.session.add(evaluation)
    db.session.commit()

    flash('Evaluasi berhasil ditambahkan', 'success')
    return redirect(url_for('admin.course_content', course_id=material.course_id))


@admin_bp.route('/evaluations/<int:evaluation_id>/update', methods=['POST'])
@admin_required
def update_evaluation(evaluation_id):
    """Perbarui evaluasi materi."""
    evaluation = Evaluation.query.get_or_404(evaluation_id)
    error = _populate_evaluation_from_form(evaluation, request.form)

    if error:
        flash(error, 'danger')
        return redirect(url_for('admin.course_content', course_id=evaluation.material.course_id, edit_evaluation=evaluation.id))

    evaluation.updated_at = datetime.utcnow()
    db.session.commit()

    flash('Evaluasi berhasil diperbarui', 'success')
    return redirect(url_for('admin.course_content', course_id=evaluation.material.course_id))


@admin_bp.route('/evaluations/<int:evaluation_id>/delete', methods=['POST'])
@admin_required
def delete_evaluation(evaluation_id):
    """Hapus evaluasi dari materi."""
    evaluation = Evaluation.query.get_or_404(evaluation_id)
    course_id = evaluation.material.course_id

    db.session.delete(evaluation)
    db.session.commit()

    flash('Evaluasi berhasil dihapus', 'success')
    return redirect(url_for('admin.course_content', course_id=course_id))

@admin_bp.route('/courses/<int:course_id>/delete', methods=['POST'])
@admin_required
def delete_course(course_id):
    """Hapus course"""
    course = Course.query.get_or_404(course_id)
    course_title = course.title
    
    db.session.delete(course)
    db.session.commit()
    
    flash(f'Course "{course_title}" berhasil dihapus', 'success')
    return redirect(url_for('admin.courses_list'))

# ==================== VERIFIKASI VISIT PROOF ====================
@admin_bp.route('/courses/<int:course_id>/proofs')
@admin_required
def course_proofs(course_id):
    """List visit proofs untuk verifikasi per course"""
    course = Course.query.get_or_404(course_id)
    
    # Get all proofs for this course
    proofs = VisitProof.query.filter_by(course_id=course_id).order_by(VisitProof.uploaded_at.desc()).all()
    
    return render_template('admin/course_proofs.html', course=course, proofs=proofs)

@admin_bp.route('/proofs/<int:proof_id>/approve', methods=['POST'])
@admin_required
def approve_proof(proof_id):
    """Setujui visit proof"""
    proof = VisitProof.query.get_or_404(proof_id)
    course_id = proof.course_id
    
    proof.status = 'approved'
    proof.verified_by = current_user.id
    proof.verified_at = datetime.utcnow()
    
    db.session.commit()
    
    flash(f'Bukti kunjungan dari {proof.student.name} disetujui', 'success')
    return redirect(url_for('admin.course_proofs', course_id=course_id))

@admin_bp.route('/proofs/<int:proof_id>/reject', methods=['POST'])
@admin_required
def reject_proof(proof_id):
    """Tolak visit proof"""
    proof = VisitProof.query.get_or_404(proof_id)
    course_id = proof.course_id
    
    notes = request.form.get('notes', '')
    
    proof.status = 'rejected'
    proof.verified_by = current_user.id
    proof.verified_at = datetime.utcnow()
    proof.notes = notes
    
    db.session.commit()
    
    flash(f'Bukti kunjungan dari {proof.student.name} ditolak', 'warning')
    return redirect(url_for('admin.course_proofs', course_id=course_id))

# ==================== CERTIFICATE TEMPLATE ====================
@admin_bp.route('/courses/<int:course_id>/certificate')
@admin_required
def certificate_settings(course_id):
    """Kelola template sertifikat per course"""
    course = Course.query.get_or_404(course_id)
    
    # Get or create certificate template
    cert_template = CertificateTemplate.query.filter_by(course_id=course_id).first()
    
    if not cert_template:
        cert_template = CertificateTemplate(
            course_id=course_id,
            certificate_number_format=f'{{year}}/UN4.1.1.5/TA.01.02/{{seq}}',
            year=datetime.utcnow().year,
            head_name='Prof. Dr. Nama Kepala',
            head_nip='197105101998031234',
        )
        db.session.add(cert_template)
        db.session.commit()
    
    return render_template('admin/certificate_settings.html', course=course, cert_template=cert_template)

@admin_bp.route('/certificates/<int:cert_id>/update', methods=['POST'])
@admin_required
def update_certificate_settings(cert_id):
    """Update sertifikat settings"""
    cert = CertificateTemplate.query.get_or_404(cert_id)
    course_id = cert.course_id
    
    cert.certificate_number_format = (request.form.get('number_format') or '').strip()
    cert.year = int(request.form.get('year') or datetime.utcnow().year)
    cert.current_sequence = int(request.form.get('current_sequence') or 0)
    cert.head_name = (request.form.get('head_name') or '').strip()
    cert.head_nip = (request.form.get('head_nip') or '').strip()
    cert.head_title = (request.form.get('head_title') or 'Kepala Perpustakaan').strip()
    cert.institution_name = (request.form.get('institution_name') or '').strip()
    cert.institution_npp = (request.form.get('institution_npp') or '').strip()
    
    if not cert.certificate_number_format:
        flash('Format nomor sertifikat harus diisi', 'danger')
        return redirect(url_for('admin.certificate_settings', course_id=course_id))
    
    if not cert.head_name or not cert.head_nip:
        flash('Nama dan NIP kepala perpustakaan harus diisi', 'danger')
        return redirect(url_for('admin.certificate_settings', course_id=course_id))
    
    db.session.commit()
    flash('Settings sertifikat berhasil diupdate', 'success')
    return redirect(url_for('admin.certificate_settings', course_id=course_id))

# ==================== ADMIN LOGIN ====================
@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if current_user.is_authenticated:
        return redirect(role_home())
    
    if request.method == 'POST':
        nim = request.form.get('nim')
        password = request.form.get('password')
        
        user = User.query.filter_by(nim=nim).first()
        
        if user and user.check_password(password):
            if user.role != 'admin':
                flash('NIM ini bukan akun admin', 'danger')
                return redirect(url_for('admin.admin_login'))
            
            login_user(user, remember=True)
            flash(f'Login admin berhasil! Selamat datang {user.name}', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('NIM atau password salah', 'danger')
    
    return render_template('admin/login.html')
