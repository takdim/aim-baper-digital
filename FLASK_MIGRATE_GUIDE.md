# Flask-Migrate Setup - BAPER Digital

## ✅ Setup Selesai!

Flask-Migrate dan database migrations sudah berhasil dikonfigurasi.

---

## 📝 Admin Account yang Telah Dibuat

```
NIM: ADMIN
Password: papua123
Role: admin
```

---

## 🔧 Flask-Migrate Commands

### 1. Initialize Migrations (Sudah Dilakukan)
```bash
flask db init
```
Membuat folder `migrations/` dengan template Alembic.

### 2. Create Migration (Sudah Dilakukan)
```bash
flask db migrate -m "Initial migration - create all models"
```
Generate migration file dari model changes.

### 3. Upgrade Database (Sudah Dilakukan)
```bash
flask db upgrade
```
Apply migration ke database.

### 4. Downgrade (Jika Diperlukan)
```bash
flask db downgrade
```
Revert migration ke state sebelumnya.

---

## 📂 Struktur Migrations

```
migrations/
├── alembic.ini              # Alembic configuration
├── env.py                   # Migration environment setup
├── script.py.mako           # Migration template
├── versions/                # Folder untuk migration files
│   └── 2bb2e651de5a_initial_migration_create_all_models.py
└── README                   # Alembic README
```

---

## 🛠️ Development Workflow

### 1. Membuat Model Baru
```python
# app/models/new_model.py
class NewModel(db.Model):
    __tablename__ = 'new_models'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
```

### 2. Import Model di `app/models/__init__.py`
```python
from app.models.new_model import NewModel
```

### 3. Generate Migration
```bash
flask db migrate -m "Add new_models table"
```

### 4. Review Migration File (Optional)
Periksa file di `migrations/versions/` untuk memastikan benar.

### 5. Apply Migration
```bash
flask db upgrade
```

---

## 🧬 Database Schema

Database `baper_digital` sudah dibuat dengan 8 tabel:

| Tabel | Deskripsi |
|-------|-----------|
| users | Mahasiswa & Admin |
| courses | Orientasi/Kursus |
| student_courses | Enrollment |
| materials | Materi Pembelajaran |
| evaluations | Kuis/Evaluasi |
| student_evaluations | Jawaban Mahasiswa |
| visit_proofs | Bukti Kunjungan |
| certificates | Sertifikat |

---

## 💡 Tips & Best Practices

### 1. Always Review Migrations
Sebelum upgrade, selalu review file migration untuk memastikan tidak ada yang terlewat.

### 2. Test di Development Dulu
Jangan langsung upgrade di production. Test di development terlebih dahulu.

### 3. Backup Database
Sebelum upgrade, selalu backup database:
```bash
mysqldump -u root -p baper_digital > backup.sql
```

### 4. Version Control
Commit migration files ke git:
```bash
git add migrations/versions/
git commit -m "Add migration for new features"
```

### 5. Naming Convention
Gunakan nama yang jelas dan deskriptif:
```bash
# ✅ Good
flask db migrate -m "Add email field to users table"

# ❌ Bad
flask db migrate -m "update"
```

---

## 🔙 Rollback/Downgrade

Jika ada error, Anda bisa rollback:

```bash
# Lihat history migrations
flask db history

# Downgrade ke revision tertentu
flask db downgrade <revision_id>

# Downgrade satu langkah
flask db downgrade
```

---

## 📊 Melihat Status Migrations

```bash
# Lihat current revision
flask db current

# Lihat history
flask db history

# Lihat branches (jika ada)
flask db branches
```

---

## 🚀 Manajemen Versions

### Current Versions
```
2bb2e651de5a - Initial migration - create all models
```

### Add to Git
```bash
git add migrations/
git commit -m "Initial database schema with all models"
```

---

## 📖 Dokumentasi Lengkap

- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/orm/)

---

## ⚠️ Common Issues & Solutions

### Issue: "Can't determine join between tables..."
**Solusi**: Specify `foreign_keys` dalam relationship definition

```python
relationship = db.relationship('Model', foreign_keys=[column])
```

### Issue: "Duplicate column name..."
**Solusi**: Hapus auto-generated migration file dan edit manual

### Issue: Migration stuck
**Solusi**: Check `alembic_version` table dan update manually jika perlu

```sql
-- Check current version
SELECT * FROM alembic_version;

-- Manual update (rare cases only)
UPDATE alembic_version SET version_num = '<revision_id>';
```

---

## 📞 Commands Quick Reference

```bash
# Initialize migrations folder
flask db init

# Generate migration from model changes
flask db migrate -m "Description"

# Apply all pending migrations
flask db upgrade

# Rollback last migration
flask db downgrade

# Show current revision
flask db current

# Show migration history
flask db history

# Merge conflicting branches
flask db merge <revision> <revision>
```

---

## ✅ Checklist

- [x] Flask-Migrate installed
- [x] Migrations folder initialized
- [x] Initial migration created
- [x] Database upgraded
- [x] Admin account created (NIM: ADMIN, Password: papua123)
- [x] Models fixed (foreign keys)
- [ ] Create sample data (optional)

---

Last Updated: April 28, 2026
