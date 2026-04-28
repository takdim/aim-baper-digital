# Database Schema - BAPER Digital

## Tabel: users
Menyimpan data mahasiswa dan admin

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nim VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    faculty VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'student',  -- 'student' atau 'admin'
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_nim (nim),
    INDEX idx_role (role)
);
```

## Tabel: courses
Menyimpan data orientasi/kursus

```sql
CREATE TABLE courses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    created_by INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_is_active (is_active)
);
```

## Tabel: student_courses
Menyimpan enrollment mahasiswa ke course

```sql
CREATE TABLE student_courses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    status VARCHAR(20) DEFAULT 'enrolled',  -- 'enrolled', 'in_progress', 'completed'
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    progress FLOAT DEFAULT 0.0,  -- 0-100
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    UNIQUE KEY uq_student_course (student_id, course_id),
    INDEX idx_status (status)
);
```

## Tabel: materials
Menyimpan materi pembelajaran

```sql
CREATE TABLE materials (
    id INT PRIMARY KEY AUTO_INCREMENT,
    course_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    content LONGTEXT NOT NULL,
    `order` INT NOT NULL,  -- Urutan materi
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    INDEX idx_course_order (course_id, `order`)
);
```

## Tabel: evaluations
Menyimpan evaluasi/kuis untuk setiap materi

```sql
CREATE TABLE evaluations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    material_id INT NOT NULL,
    question LONGTEXT NOT NULL,
    question_type VARCHAR(20) DEFAULT 'multiple_choice',  -- 'multiple_choice', 'essay'
    option_a TEXT,
    option_b TEXT,
    option_c TEXT,
    option_d TEXT,
    correct_answer VARCHAR(1),  -- 'A', 'B', 'C', 'D'
    `order` INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (material_id) REFERENCES materials(id) ON DELETE CASCADE,
    INDEX idx_material_order (material_id, `order`)
);
```

## Tabel: student_evaluations
Menyimpan jawaban mahasiswa pada evaluasi

```sql
CREATE TABLE student_evaluations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    evaluation_id INT NOT NULL,
    answer VARCHAR(255) NOT NULL,
    is_correct BOOLEAN,  -- NULL untuk essay (menunggu verifikasi)
    score FLOAT,  -- Untuk essay setelah diverifikasi
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (evaluation_id) REFERENCES evaluations(id) ON DELETE CASCADE,
    UNIQUE KEY uq_student_evaluation (student_id, evaluation_id),
    INDEX idx_student_id (student_id)
);
```

## Tabel: visit_proofs
Menyimpan bukti kunjungan mahasiswa ke perpustakaan

```sql
CREATE TABLE visit_proofs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    photo_path VARCHAR(255) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',  -- 'pending', 'approved', 'rejected'
    notes TEXT,  -- Catatan dari admin
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified_by INT,
    verified_at TIMESTAMP NULL,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (verified_by) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE KEY uq_visit_proof (student_id, course_id),
    INDEX idx_status (status)
);
```

## Tabel: certificates
Menyimpan sertifikat

```sql
CREATE TABLE certificates (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    certificate_path VARCHAR(255) NOT NULL,
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    downloaded_at TIMESTAMP NULL,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    UNIQUE KEY uq_certificate (student_id, course_id)
);
```

## Relationships Diagram

```
users (1) ---< (N) student_courses (N) ---> (1) courses
users (1) ---< (N) student_evaluations (N) ----> (1) evaluations
users (1) ---< (N) visit_proofs (N) ----> (1) courses
users (1) ---< (N) certificates (N) ----> (1) courses
courses (1) ---< (N) materials (N) ----> (?) evaluations
materials (1) ---< (N) evaluations
```

## Catatan

- `order` pada materials dan evaluations digunakan untuk mengatur urutan tampilan
- Status di student_courses: 'enrolled' (baru enroll), 'in_progress' (sedang belajar), 'completed' (sudah selesai)
- Status di visit_proofs: 'pending' (menunggu verifikasi), 'approved' (sudah diverifikasi), 'rejected' (ditolak)
- Password disimpan dalam bentuk hash menggunakan werkzeug.security
