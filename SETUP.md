# Setup Guide - BAPER Digital

## Langkah-langkah Setup

### 1. Persiapan Awal

```bash
# Pastikan Anda sudah di folder project
cd /Users/aim/Coding/python/aim-baper-digital

# Aktifkan virtual environment (jika belum)
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Packages yang akan diinstall:
- **Flask** (2.3.3): Web framework
- **Flask-SQLAlchemy** (3.0.5): ORM untuk database
- **Flask-Login** (0.6.2): Authentication
- **Flask-WTF** (1.1.1): Form handling
- **mysql-connector-python** (8.0.33): MySQL driver
- **python-dotenv** (1.0.0): Environment variables
- **Pillow** (10.0.0): Image handling untuk foto

### 3. Setup MySQL Database

```bash
# Login ke MySQL
mysql -u root -p

# Masukkan password MySQL Anda
```

Kemudian jalankan query berikut:

```sql
-- Create database
CREATE DATABASE baper_digital DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Optional: Buat user khusus untuk app
CREATE USER 'baper_user'@'localhost' IDENTIFIED BY 'strong_password_here';
GRANT ALL PRIVILEGES ON baper_digital.* TO 'baper_user'@'localhost';
FLUSH PRIVILEGES;
```

### 4. Konfigurasi Environment Variables

Edit file `.env`:

```bash
nano .env  # atau gunakan editor favorit Anda
```

Sesuaikan database credentials:

```
FLASK_ENV=development
FLASK_APP=run.py
DATABASE_URL=mysql+mysqlconnector://root:password@localhost:3306/baper_digital
# atau jika menggunakan user khusus:
# DATABASE_URL=mysql+mysqlconnector://baper_user:strong_password_here@localhost:3306/baper_digital
SECRET_KEY=your-super-secret-key-please-change-this
```

### 5. Jalankan Aplikasi

```bash
python run.py
```

Aplikasi akan berjalan di: **http://localhost:5000**

Anda akan melihat output seperti ini:
```
 * Serving Flask app 'run.py'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### 6. Test Aplikasi

Buka browser dan akses:
- **http://localhost:5000** - Homepage
- **http://localhost:5000/auth/register** - Halaman Registrasi
- **http://localhost:5000/auth/login** - Halaman Login

### 7. Membuat Admin User (Opsional)

Untuk membuat admin user, Anda dapat menjalankan Python shell:

```bash
python
```

```python
from app import create_app
from app.models import db, User

app = create_app()
with app.app_context():
    # Create admin user
    admin = User(
        nim='ADMIN001',
        name='Administrator',
        faculty='IT',
        role='admin'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    print("Admin user created successfully!")
```

## Struktur Project

```
aim-baper-digital/
├── app/
│   ├── models/              # Database models
│   │   ├── __init__.py      # Models initialization
│   │   ├── user.py
│   │   ├── course.py
│   │   ├── student_course.py
│   │   ├── material.py
│   │   ├── evaluation.py
│   │   ├── student_evaluation.py
│   │   ├── visit_proof.py
│   │   └── certificate.py
│   ├── routes/              # Flask routes/blueprints
│   │   ├── __init__.py
│   │   ├── auth.py          # Registration & Login
│   │   ├── dashboard.py     # Dashboard routes
│   │   └── course.py        # Course management routes
│   ├── templates/           # HTML templates (belum dibuat)
│   ├── static/              # CSS, JS, Images (belum dibuat)
│   └── __init__.py          # Flask app factory
├── venv/                    # Virtual environment
├── config.py                # Configuration
├── run.py                   # Entry point
├── requirements.txt         # Dependencies
├── .env                     # Environment variables
├── .gitignore              # Git ignore rules
├── DATABASE_SCHEMA.md      # Database schema documentation
├── SETUP.md                # Setup guide (file ini)
└── README.md               # Project documentation
```

## Environment Variables Penjelasan

| Variable | Deskripsi |
|----------|-----------|
| `FLASK_ENV` | `development` untuk development mode, `production` untuk live |
| `FLASK_APP` | Entry point aplikasi (run.py) |
| `DATABASE_URL` | Connection string ke MySQL database |
| `SECRET_KEY` | Key untuk enkripsi session dan CSRF token |

## Troubleshooting

### Error: "No module named 'app'"

Pastikan Anda berada di directory yang benar dan virtual environment sudah diaktifkan.

```bash
source venv/bin/activate
echo $VIRTUAL_ENV  # Seharusnya menunjukkan path ke venv
```

### Error: "Can't connect to MySQL server"

1. Pastikan MySQL service sudah running
   ```bash
   # macOS dengan Homebrew
   brew services list
   brew services start mysql
   ```

2. Pastikan credentials di `.env` sudah benar

3. Verifikasi database sudah dibuat:
   ```bash
   mysql -u root -p -e "SHOW DATABASES;"
   ```

### Error: "ImportError: No module named 'mysql'"

Reinstall dependencies:
```bash
pip install --upgrade mysql-connector-python
```

### Database Tables Tidak Terbuat

Tabel akan dibuat otomatis saat pertama kali aplikasi dijalankan. Jika tidak:

```python
from app import create_app

app = create_app()
with app.app_context():
    from app.models import db
    db.create_all()
    print("Tables created successfully!")
```

## Next Steps

1. **Buat Templates**: Buat HTML templates di folder `app/templates/`
2. **Buat Static Files**: Tambahkan CSS dan JavaScript di folder `app/static/`
3. **Implementasi Admin Routes**: Buat routes untuk admin dashboard
4. **File Upload**: Implementasi file upload untuk bukti kunjungan dan sertifikat
5. **Testing**: Buat unit tests

## Referensi Dokumentasi

- Flask: https://flask.palletsprojects.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Flask-Login: https://flask-login.readthedocs.io/
- MySQL Connector: https://dev.mysql.com/doc/connector-python/en/
