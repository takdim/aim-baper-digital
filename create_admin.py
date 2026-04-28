#!/usr/bin/env python
"""
Script untuk membuat admin user
Usage: python create_admin.py
"""

from app import create_app, db
from app.models import User
import sys

def create_admin():
    """Buat admin user baru"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*50)
        print("CREATE ADMIN USER")
        print("="*50)
        
        # Input dari user
        nim = input("\n📋 Masukkan NIM Admin: ").strip()
        name = input("👤 Masukkan Nama Lengkap: ").strip()
        faculty = input("🏢 Masukkan Fakultas: ").strip()
        email = input("📧 Masukkan Email (opsional, Enter untuk skip): ").strip() or None
        password = input("🔐 Masukkan Password: ").strip()
        password_confirm = input("🔐 Konfirmasi Password: ").strip()
        
        # Validasi
        if not all([nim, name, faculty, password]):
            print("\n❌ Error: NIM, nama, fakultas, dan password harus diisi!")
            return False
        
        if password != password_confirm:
            print("\n❌ Error: Password tidak cocok!")
            return False
        
        if len(password) < 8:
            print("\n⚠️  Warning: Password sebaiknya minimal 8 karakter")
            confirm = input("   Lanjutkan? (y/n): ").strip().lower()
            if confirm != 'y':
                return False
        
        # Cek apakah NIM sudah ada
        existing_nim = User.query.filter_by(nim=nim).first()
        if existing_nim:
            print(f"\n❌ Error: NIM '{nim}' sudah terdaftar!")
            return False
        
        # Cek apakah email sudah ada
        if email:
            existing_email = User.query.filter_by(email=email).first()
            if existing_email:
                print(f"\n❌ Error: Email '{email}' sudah terdaftar!")
                return False
        
        # Buat admin user
        try:
            admin = User(
                nim=nim,
                name=name,
                faculty=faculty,
                email=email,
                role='admin',
                is_active=True
            )
            admin.set_password(password)
            
            db.session.add(admin)
            db.session.commit()
            
            print("\n" + "="*50)
            print("✅ ADMIN USER BERHASIL DIBUAT!")
            print("="*50)
            print(f"NIM      : {admin.nim}")
            print(f"Nama     : {admin.name}")
            print(f"Fakultas : {admin.faculty}")
            print(f"Email    : {admin.email or '-'}")
            print(f"Role     : {admin.role}")
            print(f"ID       : {admin.id}")
            print("\n💡 Gunakan kredensial di atas untuk login di /admin/login")
            print("="*50 + "\n")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    success = create_admin()
    sys.exit(0 if success else 1)
