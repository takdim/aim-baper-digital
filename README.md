# BAPER Digital - Sistem Orientasi Perpustakaan Digital

Aplikasi web untuk memberikan orientasi perpustakaan digital kepada mahasiswa baru.

## Fitur

- **Registrasi & Login**: Mahasiswa dapat mendaftar dengan NIM, nama, fakultas, dan password
- **Dashboard**: Menampilkan daftar orientasi yang tersedia
- **Enrollment**: Mahasiswa dapat mengambil course orientasi
- **Materi Pembelajaran**: Akses ke materi pembelajaran yang disediakan admin
- **Evaluasi**: Quiz/evaluasi untuk setiap materi
- **Bukti Kunjungan**: Upload foto sebagai bukti kunjungan ke perpustakaan
- **Verifikasi Admin**: Admin memverifikasi bukti kunjungan
- **Sertifikat**: Download sertifikat setelah menyelesaikan course

## Teknologi

- Flask (Python Web Framework)
- MySQL (Database)
- SQLAlchemy (ORM)
- Flask-Login (Authentication)

## Instalasi

### 1. Clone Repository
```bash
git clone <repository-url>
cd aim-baper-digital
```

### 2. Setup Virtual Environment
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Database
```bash
# Buat database MySQL
mysql -u root -p
CREATE DATABASE baper_digital DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Konfigurasi Environment
Buat file `.env` dan sesuaikan:
```
FLASK_ENV=development
FLASK_APP=run.py
DATABASE_URL=mysql+mysqlconnector://username:password@localhost:3306/baper_digital
SECRET_KEY=your-secret-key
```

### 6. Run Application
```bash
python run.py
```

Aplikasi akan berjalan di `http://localhost:5000`

## Struktur Project

```
aim-baper-digital/
├── app/
│   ├── models/          # Database models
│   ├── routes/          # Flask blueprints & routes
│   ├── templates/       # HTML templates
│   ├── static/          # CSS, JS, images
│   └── __init__.py      # Flask app factory
├── config.py            # Configuration
├── run.py               # Entry point
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
└── README.md            # This file
```

## Database Models

### User
- Menyimpan data mahasiswa dan admin
- **Fields**: id, nim, name, faculty, email, password_hash, role, is_active, created_at, updated_at

### Course
- Orientasi/kursus yang tersedia
- **Fields**: id, title, description, created_by (admin), is_active, created_at, updated_at

### StudentCourse
- Enrollment: hubungan antara mahasiswa dan course
- **Fields**: id, student_id, course_id, status, progress, enrolled_at, completed_at

### Material
- Materi pembelajaran dalam setiap course
- **Fields**: id, course_id, title, content, order, created_at, updated_at

### Evaluation
- Kuis/evaluasi di setiap materi
- **Fields**: id, material_id, question, question_type, option_a, option_b, option_c, option_d, correct_answer, order

### StudentEvaluation
- Jawaban mahasiswa terhadap evaluasi
- **Fields**: id, student_id, evaluation_id, answer, is_correct, score, answered_at

### VisitProof
- Bukti kunjungan mahasiswa ke perpustakaan
- **Fields**: id, student_id, course_id, photo_path, status (pending/approved/rejected), notes, verified_by, verified_at

### Certificate
- Sertifikat yang diberikan kepada mahasiswa
- **Fields**: id, student_id, course_id, certificate_path, issued_at, downloaded_at

## Penggunaan

### Sebagai Mahasiswa

1. **Registrasi**: Isi form registrasi dengan NIM, nama, fakultas, password
2. **Login**: Masuk dengan NIM dan password
3. **Dashboard**: Lihat daftar orientasi yang tersedia
4. **Get Course**: Klik "Ambil Course" untuk enroll
5. **Belajar**: Akses materi dan kerjakan evaluasi
6. **Upload Bukti**: Upload foto kunjungan ke perpustakaan
7. **Download Sertifikat**: Download sertifikat setelah diverifikasi admin

### Sebagai Admin

- Membuat course baru
- Menambahkan materi pembelajaran
- Membuat evaluasi/kuis
- Memverifikasi bukti kunjungan
- Generate dan menyimpan sertifikat

## Kontribusi

Pull requests welcome! Untuk perubahan besar, buka issue terlebih dahulu untuk mendiskusikan perubahan yang diinginkan.

## Lisensi

This project is licensed under the MIT License.