from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def role_home():
    """Return home route sesuai role user yang sedang login."""
    if current_user.is_authenticated and current_user.role == 'admin':
        return url_for('admin.dashboard')
    return url_for('dashboard.index')

def admin_required(f):
    """Decorator untuk memastikan user adalah admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Silakan login terlebih dahulu', 'danger')
            return redirect(url_for('admin.admin_login'))
        if current_user.role != 'admin':
            flash('Anda tidak memiliki akses ke halaman ini', 'danger')
            return redirect(role_home())
        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    """Decorator untuk memastikan user adalah mahasiswa."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Silakan login terlebih dahulu', 'danger')
            return redirect(url_for('auth.login'))
        if current_user.role != 'student':
            flash('Halaman ini hanya untuk mahasiswa', 'warning')
            return redirect(role_home())
        return f(*args, **kwargs)
    return decorated_function
