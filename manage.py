#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Management script untuk BAPER Digital
Gunakan: python manage.py <command>
"""
import os
import click
from flask.cli import with_appcontext
from app import create_app, db
from app.models import User

app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Make shell context for flask shell"""
    return {
        'db': db,
        'User': User
    }

@app.cli.command()
def init_admin():
    """Membuat admin account"""
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(nim='ADMIN').first()
        if admin:
            click.echo(click.style('❌ Admin account sudah ada!', fg='red'))
            return
        
        # Create admin
        admin = User(
            nim='ADMIN',
            name='Administrator',
            faculty='IT',
            role='admin',
            is_active=True
        )
        admin.set_password('papua123')
        
        db.session.add(admin)
        db.session.commit()
        
        click.echo(click.style('✅ Admin account berhasil dibuat!', fg='green'))
        click.echo(f'  NIM: ADMIN')
        click.echo(f'  Password: papua123')
        click.echo(f'  Role: admin')

@app.cli.command()
def create_sample_data():
    """Membuat sample data untuk testing"""
    with app.app_context():
        # Create sample student
        student = User.query.filter_by(nim='STU001').first()
        if not student:
            student = User(
                nim='STU001',
                name='Mahasiswa Test',
                faculty='Teknik Informatika',
                role='student'
            )
            student.set_password('password123')
            db.session.add(student)
            db.session.commit()
            click.echo(click.style('✅ Sample student berhasil dibuat!', fg='green'))
            click.echo(f'  NIM: STU001')
            click.echo(f'  Password: password123')
        else:
            click.echo(click.style('ℹ️  Sample student sudah ada', fg='yellow'))

if __name__ == '__main__':
    app.cli()
