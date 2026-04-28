# Admin Panel Setup Guide

## Daftar Isi
1. [Ringkasan Fitur](#ringkasan-fitur)
2. [Struktur Admin Panel](#struktur-admin-panel)
3. [Membuat Admin User](#membuat-admin-user)
4. [Menggunakan Admin Panel](#menggunakan-admin-panel)
5. [Fitur-Fitur Admin](#fitur-fitur-admin)

## Ringkasan Fitur

Admin panel telah berhasil dibuat dengan fitur-fitur berikut:

### ✅ Login Terpisah
- **Admin Login**: `/admin/login` - Login khusus untuk admin
- **Student Login**: `/auth/login` - Login untuk mahasiswa
- Link ke Admin Login tersedia di navbar ketika belum login

### ✅ Dashboard Admin
- Statistik sistem (total user, mahasiswa, admin, course)
- Quick action buttons untuk navigasi cepat
- Ringkasan sistem dan status

### ✅ Manajemen User
- **List User**: Lihat semua user dengan filter (role, search)
- **Tambah User**: Buat user baru (mahasiswa atau admin)
- **Edit User**: Ubah data user, role, status aktif/nonaktif
- **Hapus User**: Menghapus user dari sistem
- Pagination untuk user list

### ✅ Manajemen Course
- **List Course**: Lihat semua course dengan filter (status, search)
- **Tambah Course**: Buat course baru
- **Edit Course**: Ubah judul, deskripsi, dan status course
- **Hapus Course**: Menghapus course dari sistem
- Pagination untuk course list

## Struktur Admin Panel

```
Admin Panel
├── Dashboard (/admin/dashboard)
│   └── Statistik dan Quick Actions
├── Manajemen User (/admin/users)
│   ├── List User
│   ├── Tambah User
│   └── Edit/Hapus User
└── Manajemen Course (/admin/courses)
    ├── List Course
    ├── Tambah Course
    └── Edit/Hapus Course
```

## Membuat Admin User

### Cara 1: Menggunakan Flask Shell (Recommended)

```bash
cd /Users/aim/Coding/python/aim-baper-digital
source venv/bin/activate
flask shell
```

Kemudian jalankan kode berikut:

```python
from app.models import db, User

# Buat admin user baru
admin = User(
    nim='123456789',
    name='Admin Sistem',
    faculty='IT',
    email='admin@example.com',
    role='admin',
    is_active=True
)
admin.set_password('admin123')  # Ganti dengan password yang kuat
db.session.add(admin)
db.session.commit()
print(f'Admin user berhasil dibuat: {admin.name}')
```

### Cara 2: Menggunakan Script Python

Buat file `create_admin.py`:

```python
from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Cek apakah admin sudah ada
    existing = User.query.filter_by(nim='123456789').first()
    if existing:
        print('Admin dengan NIM ini sudah ada!')
        exit(1)
    
    # Buat admin baru
    admin = User(
        nim='123456789',
        name='Admin Sistem',
        faculty='IT',
        email='admin@example.com',
        role='admin',
        is_active=True
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    
    print('✓ Admin user berhasil dibuat!')
    print(f'  NIM: {admin.nim}')
    print(f'  Nama: {admin.name}')
    print(f'  Role: {admin.role}')
```

Kemudian jalankan:
```bash
python create_admin.py
```

## Menggunakan Admin Panel

### Login sebagai Admin

1. Buka halaman login admin: `http://localhost:5000/admin/login`
2. Masukkan NIM dan password admin
3. Klik tombol "Login"
4. Akan diarahkan ke Admin Dashboard

### Logout

Klik menu "Logout" di sidebar admin panel

## Fitur-Fitur Admin

### 1. Dashboard Admin
**URL**: `/admin/dashboard`

Menampilkan:
- Total user dalam sistem
- Total mahasiswa
- Total admin
- Total course
- Course yang aktif
- Quick action buttons

### 2. Manajemen User

#### List User (/admin/users)
- Tampilkan semua user dalam tabel
- Filter berdasarkan role (Mahasiswa/Admin)
- Search berdasarkan nama, NIM, atau email
- Pagination (10 user per halaman)
- Action: Edit, Hapus

#### Tambah User (/admin/users/create)
- Form untuk membuat user baru
- Input: NIM, Nama, Fakultas, Email, Password, Role
- Validasi:
  - NIM harus unik
  - Email harus unik (jika diisi)
  - Password wajib diisi
  - Nama dan Fakultas wajib diisi

#### Edit User (/admin/users/<id>/edit)
- Edit nama, fakultas, email
- Ubah role (Student/Admin)
- Update password (opsional)
- Aktifkan/Nonaktifkan user

#### Hapus User (/admin/users/<id>/delete)
- Hapus user dari sistem
- Meminta konfirmasi sebelum menghapus

### 3. Manajemen Course

#### List Course (/admin/courses)
- Tampilkan semua course dalam tabel
- Filter berdasarkan status (Aktif/Nonaktif)
- Search berdasarkan judul
- Pagination (10 course per halaman)
- Action: Edit, Hapus

#### Tambah Course (/admin/courses/create)
- Form untuk membuat course baru
- Input: Judul, Deskripsi
- Course otomatis aktif saat dibuat
- Created_by otomatis diisi dengan user yang login

#### Edit Course (/admin/courses/<id>/edit)
- Edit judul dan deskripsi course
- Aktifkan/Nonaktifkan course

#### Hapus Course (/admin/courses/<id>/delete)
- Hapus course dari sistem
- Peringatan: Semua data related akan terhapus

## Keamanan

### Role-Based Access Control (RBAC)
- Hanya user dengan role 'admin' yang bisa akses admin panel
- Decorator `@admin_required` melindungi semua route admin
- Jika user biasa mencoba akses, akan diarahkan ke dashboard biasa

### Login Terpisah
- Admin dan student memiliki login page terpisah
- Jika student mencoba login dengan akun admin, akan ditolak
- Admin tidak bisa membuat course/manage user dari dashboard biasa

## Tips Penggunaan

1. **Create Admin First**: Selalu buat minimal satu admin user terlebih dahulu
2. **Unique NIM**: Pastikan NIM yang digunakan unik (tidak duplicate)
3. **Strong Password**: Gunakan password yang kuat untuk akun admin
4. **Backup Regular**: Backup database secara berkala
5. **Monitor User**: Pantau user list untuk mendeteksi aktivitas mencurigakan

## Troubleshooting

### Admin tidak bisa login
- Pastikan role user adalah 'admin' (bukan 'student')
- Verifikasi password benar
- Pastikan is_active = True

### Halaman admin tidak load
- Pastikan user sudah login sebagai admin
- Check decorator @admin_required melindungi route
- Verify role = 'admin' di database

### Course tidak tampil di list
- Pastikan course dibuat oleh admin yang sedang login
- Check status course (aktif/nonaktif)
- Verify database tidak corrupt

## File yang Ditambahkan

### Python Files
- `app/routes/admin.py` - Admin routes dan logic
- `app/utils/decorators.py` - @admin_required decorator

### Template Files
- `app/templates/admin/base.html` - Base template admin
- `app/templates/admin/login.html` - Admin login page
- `app/templates/admin/dashboard.html` - Admin dashboard
- `app/templates/admin/users_list.html` - List semua user
- `app/templates/admin/create_user.html` - Buat user baru
- `app/templates/admin/edit_user.html` - Edit user
- `app/templates/admin/courses_list.html` - List semua course
- `app/templates/admin/create_course.html` - Buat course baru
- `app/templates/admin/edit_course.html` - Edit course

### Modified Files
- `app/routes/__init__.py` - Tambah admin blueprint
- `app/__init__.py` - Register admin blueprint
- `app/routes/auth.py` - Update login untuk redirect admin
- `app/templates/base.html` - Tambah admin login link

## Versi
- Created: 2026-04-28
- Updated: 2026-04-28
