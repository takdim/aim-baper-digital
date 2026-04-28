from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app.routes import auth_bp
from app.models import db, User
from app.utils.decorators import role_home

FACULTY_OPTIONS = [
    "Fakultas Ekonomi dan Bisnis",
    "Fakultas Hukum",
    "Fakultas Kedokteran",
    "Fakultas Teknik",
    "Fakultas Ilmu Budaya",
    "Fakultas Pertanian",
    "Fakultas Matematika dan Ilmu Pengetahuan Alam (MIPA)",
    "Fakultas Ilmu Sosial dan Ilmu Politik (FISIP)",
    "Fakultas Kedokteran Gigi",
    "Fakultas Kesehatan Masyarakat",
    "Fakultas Ilmu Kelautan dan Perikanan",
    "Fakultas Kehutanan",
    "Fakultas Peternakan",
    "Fakultas Farmasi",
    "Fakultas Keperawatan",
    "Fakultas Vokasi",
    "Sekolah Pascasarjana",
]

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register page untuk mahasiswa baru"""
    if current_user.is_authenticated:
        return redirect(role_home())
        
    if request.method == 'POST':
        nim = request.form.get('nim')
        name = request.form.get('name')
        faculty = request.form.get('faculty')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        # Validation
        if not all([nim, name, faculty, password, password_confirm]):
            flash('Semua field harus diisi', 'danger')
            return redirect(url_for('auth.register'))
        
        if password != password_confirm:
            flash('Password tidak cocok', 'danger')
            return redirect(url_for('auth.register'))

        if faculty not in FACULTY_OPTIONS:
            flash('Fakultas yang dipilih tidak valid', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(nim=nim).first():
            flash('NIM sudah terdaftar', 'danger')
            return redirect(url_for('auth.register'))
        
        # Create user
        user = User(nim=nim, name=name, faculty=faculty, role='student')
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registrasi berhasil! Silakan login', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', faculty_options=FACULTY_OPTIONS)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page untuk mahasiswa"""
    if current_user.is_authenticated:
        return redirect(role_home())
        
    if request.method == 'POST':
        nim = request.form.get('nim')
        password = request.form.get('password')
        
        user = User.query.filter_by(nim=nim).first()
        
        if user and user.check_password(password):
            if user.role == 'admin':
                flash('Gunakan login admin untuk akun admin', 'info')
                return redirect(url_for('admin.admin_login'))
            
            # Login berhasil dengan Flask-Login
            login_user(user, remember=True)
            flash(f'Login berhasil! Selamat datang {user.name}', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(role_home())
        else:
            flash('NIM atau password salah', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """Logout"""
    logout_user()
    flash('Anda telah logout', 'info')
    return redirect(url_for('home.index'))
