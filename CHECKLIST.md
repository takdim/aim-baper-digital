# BAPER Digital - Project Checklist

## ✅ Sudah Selesai

### Project Setup
- [x] Membuat struktur folder project
- [x] Setup Python virtual environment (venv)
- [x] Membuat requirements.txt dengan semua dependencies yang diperlukan
- [x] Membuat file konfigurasi (config.py)
- [x] Membuat file environment (.env)
- [x] Membuat .gitignore
- [x] Install semua dependencies ke venv
- [x] Setup Flask-Migrate

### Database Models (8 Models)
- [x] User (mahasiswa & admin)
- [x] Course (orientasi/kursus)
- [x] StudentCourse (enrollment)
- [x] Material (materi pembelajaran)
- [x] Evaluation (kuis/evaluasi)
- [x] StudentEvaluation (jawaban mahasiswa)
- [x] VisitProof (bukti kunjungan perpustakaan)
- [x] Certificate (sertifikat)

### Flask-Migrate & Database Migrations
- [x] Flask-Migrate installed
- [x] flask db init - Inisialisasi folder migrations/
- [x] flask db migrate - Generate initial migration
- [x] flask db upgrade - Apply migration ke database
- [x] Admin account created (NIM: ADMIN, Password: papua123)
- [x] Database verified (9 tables created successfully)
- [x] Bug fixes: Foreign key relationships di User model
- [x] Auth Routes: Register, Login, Logout
- [x] Dashboard Routes: List available courses
- [x] Course Routes: Enroll, View materials, Submit evaluations
- [x] Course Routes: Upload visit proof

### Documentation
- [x] Membuat README.md dengan dokumentasi lengkap
- [x] Membuat DATABASE_SCHEMA.md dengan SQL schema
- [x] Membuat SETUP.md dengan panduan instalasi
- [x] Membuat FLASK_MIGRATE_GUIDE.md dengan migration workflows
- [x] Membuat GETTING_STARTED.md dengan quick start
- [x] Membuat MIGRATION_SETUP_COMPLETE.md dengan completion details

### Flask App Factory
- [x] Membuat app/__init__.py dengan Flask app factory
- [x] Mengintegrasikan Flask-SQLAlchemy
- [x] Mengintegrasikan Flask-Login
- [x] Blueprint registration

## ⏳ TODO - Belum Dikerjakan

### Frontend Templates (HTML/CSS)
- [ ] Base template dengan navigation
- [ ] Homepage/Landing page
- [ ] Register page
- [ ] Login page
- [ ] Dashboard - List courses
- [ ] Course detail page
- [ ] Material view page
- [ ] Evaluation/Quiz page
- [ ] Upload bukti kunjungan page
- [ ] Certificate download page
- [ ] Admin panel (dashboard, manage courses, manage materials, verify proofs)

### Admin Routes & Functionality
- [ ] Course management (create, edit, delete, list)
- [ ] Material management (create, edit, delete)
- [ ] Evaluation management (create, edit, delete)
- [ ] Verify visit proofs
- [ ] Generate & manage certificates
- [ ] Admin dashboard

### File Upload & Storage
- [ ] Implement file upload for visit proof photos
- [ ] Setup file storage system
- [ ] Generate & store certificates
- [ ] Add file validation (format, size)

### Authentication Enhancement
- [ ] Integrate Flask-Login dengan routes
- [ ] Add login_required decorators
- [ ] Add role-based access control (RBAC)
- [ ] Add forgot password functionality (optional)

### Evaluation System
- [ ] Scoring system untuk multiple choice
- [ ] Essay evaluation handling
- [ ] Progress calculation
- [ ] Completion status tracking

### Testing
- [ ] Unit tests untuk models
- [ ] Integration tests untuk routes
- [ ] Test authentication
- [ ] Test database operations

### Security
- [ ] Input validation & sanitization
- [ ] SQL injection prevention (SQLAlchemy ORM already prevents this)
- [ ] CSRF protection (Flask-WTF)
- [ ] Password hashing (Werkzeug already implemented)
- [ ] Rate limiting (optional)
- [ ] HTTPS configuration untuk production

### Additional Features (Optional)
- [ ] Email notification system
- [ ] Search & filtering functionality
- [ ] Student progress tracking
- [ ] Course statistics/reports
- [ ] PDF certificate generation
- [ ] Email notifications untuk students

### Deployment
- [ ] Setup production database
- [ ] Configure production environment
- [ ] Setup error logging
- [ ] Configure email service (jika diperlukan)
- [ ] Deploy to server/hosting

## 📝 Model Struktur Summary

```
User (1) ──┬─→ StudentCourse → Course ──┬─→ Material → Evaluation
           │                                │
           ├─→ StudentEvaluation → Evaluation
           │
           ├─→ VisitProof → Course
           │
           └─→ Certificate → Course
```

## 🎯 Priority Order Rekomendasi

1. **High Priority**: 
   - Frontend templates (basis untuk testing)
   - Admin routes & functionality
   - File upload system
   - Login/logout integration

2. **Medium Priority**:
   - Evaluation scoring system
   - Role-based access control
   - Certificate generation

3. **Low Priority**:
   - Additional features
   - Advanced testing
   - Production optimization

## 📊 Progress Estimasi

- Setup & Database Models: ✅ 100%
- Database Migrations & Admin: ✅ 100%
- Routes (Basic): ✅ 70%
- Frontend: ⏳ 0%
- Admin Panel: ⏳ 0%
- File Management: ⏳ 0%
- Testing: ⏳ 0%
- Deployment: ⏳ 0%

**Overall Progress: ~30%**

---

Last Updated: April 28, 2026
