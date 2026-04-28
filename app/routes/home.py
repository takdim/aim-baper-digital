from flask import render_template
from flask_login import current_user
from app.routes import home_bp

@home_bp.route('/')
def index():
    """Halaman utama yang tetap bisa diakses semua user."""
    return render_template('home/index.html')

@home_bp.route('/about')
def about():
    """Halaman tentang BAPER Digital"""
    return render_template('home/about.html')

@home_bp.route('/help')
def help():
    """Halaman bantuan"""
    return render_template('home/help.html')
