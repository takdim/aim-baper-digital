from flask import render_template, request, redirect, url_for, flash, send_file
from flask_login import current_user
from app.routes import course_bp
from app.models import db, Course, StudentCourse, Material, StudentEvaluation, Evaluation, VisitProof, Certificate, User, CertificateTemplate
from app.utils.decorators import student_required
from app.utils import generate_certificate_bytes, find_certificate_template
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from pathlib import Path


def _get_material_progress(material_id, student_id):
    """Hitung progress sebuah materi untuk student tertentu."""
    total_evaluations = Evaluation.query.filter_by(material_id=material_id).count()

    if total_evaluations == 0:
        return {
            'progress': 0.0,
            'answered': 0,
            'total': 0,
            'completed': False,
        }

    answered_count = (
        StudentEvaluation.query
        .join(Evaluation)
        .filter(
            StudentEvaluation.student_id == student_id,
            Evaluation.material_id == material_id
        )
        .count()
    )

    progress = round((answered_count / total_evaluations) * 100, 2)
    return {
        'progress': progress,
        'answered': answered_count,
        'total': total_evaluations,
        'completed': answered_count >= total_evaluations,
    }


def _update_course_progress(enrollment):
    """Update progress course berdasarkan materi yang sudah selesai."""
    materials = Material.query.filter_by(course_id=enrollment.course_id).all()
    total_materials = len(materials)

    if total_materials == 0:
        enrollment.progress = 0.0
        enrollment.status = 'enrolled'
        enrollment.completed_at = None
        return

    completed_materials = 0
    answered_any = False

    for material in materials:
        material_progress = _get_material_progress(material.id, enrollment.student_id)
        if material_progress['answered'] > 0:
            answered_any = True
        if material_progress['completed']:
            completed_materials += 1

    enrollment.progress = round((completed_materials / total_materials) * 100, 2)
    if completed_materials >= total_materials:
        enrollment.status = 'completed'
    elif answered_any:
        enrollment.status = 'in_progress'
    else:
        enrollment.status = 'enrolled'
    enrollment.completed_at = datetime.utcnow() if enrollment.status == 'completed' else None

@course_bp.route('/get/<int:course_id>', methods=['POST'])
@student_required
def get_course(course_id):
    """Mahasiswa enroll/get course"""
    course = Course.query.get_or_404(course_id)
    
    # Check if already enrolled
    existing = StudentCourse.query.filter_by(
        student_id=current_user.id,
        course_id=course_id
    ).first()
    
    if existing:
        flash('Anda sudah enroll course ini', 'warning')
        return redirect(url_for('course.view', course_id=course_id))
    
    # Create enrollment
    enrollment = StudentCourse(student_id=current_user.id, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()
    
    flash(f'Berhasil enroll course {course.title}!', 'success')
    return redirect(url_for('course.view', course_id=course_id))

@course_bp.route('/<int:course_id>')
@student_required
def view(course_id):
    """Tampilkan detail course dan materials"""
    course = Course.query.get_or_404(course_id)
    
    # Check enrollment
    enrollment = StudentCourse.query.filter_by(
        student_id=current_user.id,
        course_id=course_id
    ).first()
    
    if not enrollment:
        flash('Anda belum enroll course ini. Silakan enroll terlebih dahulu.', 'warning')
        return redirect(url_for('dashboard.index'))
    
    materials = Material.query.filter_by(course_id=course_id).order_by(Material.order).all()
    material_progress_map = {
        material.id: _get_material_progress(material.id, current_user.id)
        for material in materials
    }
    
    # Get visit proof
    visit_proof = VisitProof.query.filter_by(
        student_id=current_user.id,
        course_id=course_id
    ).first()
    
    return render_template(
        'course/view.html',
        course=course,
        materials=materials,
        enrollment=enrollment,
        material_progress_map=material_progress_map,
        visit_proof=visit_proof,
    )

@course_bp.route('/material/<int:material_id>')
@student_required
def view_material(material_id):
    """Tampilkan materi dan evaluasi"""
    material = Material.query.get_or_404(material_id)
    course = material.course
    
    # Check enrollment
    enrollment = StudentCourse.query.filter_by(
        student_id=current_user.id,
        course_id=course.id
    ).first()
    
    if not enrollment:
        flash('Anda belum enroll course ini', 'danger')
        return redirect(url_for('dashboard.index'))
    
    evaluations = Evaluation.query.filter_by(material_id=material_id).order_by(Evaluation.order).all()
    current_question = request.args.get('question', 1, type=int)

    if evaluations:
        if current_question < 1:
            return redirect(url_for('course.view_material', material_id=material.id, question=1))
        if current_question > len(evaluations):
            return redirect(url_for('course.view_material', material_id=material.id, question=len(evaluations)))

    answered_count = (
        StudentEvaluation.query
        .join(Evaluation)
        .filter(
            StudentEvaluation.student_id == current_user.id,
            Evaluation.material_id == material.id
        )
        .count()
    )
    
    # Get student's previous answers
    student_answers = {}
    for evaluation in evaluations:
        answer = StudentEvaluation.query.filter_by(
            student_id=current_user.id,
            evaluation_id=evaluation.id
        ).first()
        if answer:
            student_answers[evaluation.id] = answer.answer
    
    return render_template('course/material.html', 
                         material=material, 
                         evaluations=evaluations,
                         student_answers=student_answers,
                         current_question=current_question,
                         active_evaluation=evaluations[current_question - 1] if evaluations else None,
                         answered_count=answered_count,
                         material_progress=round((answered_count / len(evaluations)) * 100, 2) if evaluations else 0)

@course_bp.route('/evaluation/<int:evaluation_id>', methods=['POST'])
@student_required
def submit_evaluation(evaluation_id):
    """Submit jawaban evaluasi"""
    evaluation = Evaluation.query.get_or_404(evaluation_id)
    material = evaluation.material
    course = material.course
    
    # Check enrollment
    enrollment = StudentCourse.query.filter_by(
        student_id=current_user.id,
        course_id=course.id
    ).first()
    
    if not enrollment:
        flash('Akses tidak diizinkan', 'danger')
        return redirect(url_for('dashboard.index'))
    
    answer = request.form.get(f'evaluation_{evaluation_id}') or request.form.get('answer')
    
    if not answer:
        flash('Jawaban tidak boleh kosong', 'danger')
        question_number = request.form.get('question_number', 1, type=int)
        return redirect(url_for('course.view_material', material_id=material.id, question=question_number))
    
    # Check if already answered
    existing_answer = StudentEvaluation.query.filter_by(
        student_id=current_user.id,
        evaluation_id=evaluation_id
    ).first()
    
    is_correct = None
    if evaluation.question_type == 'multiple_choice':
        is_correct = answer.upper() == evaluation.correct_answer
    
    if existing_answer:
        existing_answer.answer = answer
        existing_answer.is_correct = is_correct
    else:
        student_eval = StudentEvaluation(
            student_id=current_user.id,
            evaluation_id=evaluation_id,
            answer=answer,
            is_correct=is_correct
        )
        db.session.add(student_eval)
    
    _update_course_progress(enrollment)
    db.session.commit()

    evaluations = Evaluation.query.filter_by(material_id=material.id).order_by(Evaluation.order).all()
    question_number = request.form.get('question_number', 1, type=int)

    if question_number < len(evaluations):
        flash('Jawaban tersimpan. Lanjut ke soal berikutnya.', 'success')
        return redirect(url_for('course.view_material', material_id=material.id, question=question_number + 1))

    flash('Jawaban tersimpan. Semua soal pada materi ini sudah selesai.', 'success')
    return redirect(url_for('course.view', course_id=course.id))

@course_bp.route('/<int:course_id>/upload-proof', methods=['GET', 'POST'])
@student_required
def upload_visit_proof(course_id):
    """Upload bukti kunjungan perpustakaan"""
    course = Course.query.get_or_404(course_id)
    
    # Check enrollment
    enrollment = StudentCourse.query.filter_by(
        student_id=current_user.id,
        course_id=course_id
    ).first()
    
    if not enrollment:
        flash('Anda belum enroll course ini', 'danger')
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        if 'photo' not in request.files:
            flash('File tidak ditemukan', 'danger')
            return redirect(url_for('course.upload_visit_proof', course_id=course_id))
        
        file = request.files['photo']
        
        if file.filename == '':
            flash('File tidak dipilih', 'danger')
            return redirect(url_for('course.upload_visit_proof', course_id=course_id))
        
        # Validasi tipe file
        ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
        if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
            flash('Hanya file gambar yang diizinkan (jpg, jpeg, png, gif)', 'danger')
            return redirect(url_for('course.upload_visit_proof', course_id=course_id))
        
        # Buat folder uploads jika belum ada
        upload_folder = Path('app/static/uploads/proofs')
        upload_folder.mkdir(parents=True, exist_ok=True)
        
        # Generate nama file unik
        filename = secure_filename(f"{current_user.id}_{course_id}_{datetime.utcnow().timestamp()}_{file.filename}")
        filepath = upload_folder / filename
        
        # Simpan file
        file.save(filepath)
        
        # Delete existing proof jika ada
        existing_proof = VisitProof.query.filter_by(
            student_id=current_user.id,
            course_id=course_id
        ).first()
        
        if existing_proof:
            # Hapus file lama
            old_path = Path(f"app/static/{existing_proof.photo_path}")
            if old_path.exists():
                old_path.unlink()
            db.session.delete(existing_proof)
        
        # Create VisitProof record
        proof = VisitProof(
            student_id=current_user.id,
            course_id=course_id,
            photo_path=f"uploads/proofs/{filename}",
            status='pending'
        )
        db.session.add(proof)
        db.session.commit()
        
        flash('Bukti kunjungan berhasil diupload. Menunggu verifikasi admin.', 'success')
        return redirect(url_for('course.view', course_id=course_id))
    
    # Check if already uploaded
    existing_proof = VisitProof.query.filter_by(
        student_id=current_user.id,
        course_id=course_id
    ).first()
    
    return render_template('course/upload_proof.html', course=course, existing_proof=existing_proof)

@course_bp.route('/<int:course_id>/download-certificate')
@student_required
def download_certificate(course_id):
    """Download sertifikat (hanya jika sudah verified) - generated on-the-fly"""
    course = Course.query.get_or_404(course_id)
    
    # Check enrollment
    enrollment = StudentCourse.query.filter_by(
        student_id=current_user.id,
        course_id=course_id
    ).first()
    
    if not enrollment:
        flash('Anda belum enroll course ini', 'danger')
        return redirect(url_for('dashboard.index'))
    
    # Check visit proof approval
    visit_proof = VisitProof.query.filter_by(
        student_id=current_user.id,
        course_id=course_id
    ).first()
    
    if not visit_proof or visit_proof.status != 'approved':
        flash('Bukti kunjungan Anda belum diverifikasi oleh admin', 'danger')
        return redirect(url_for('course.view', course_id=course_id))
    
    # Get certificate template settings
    cert_template = CertificateTemplate.query.filter_by(course_id=course_id).first()
    if not cert_template:
        flash('Sertifikat belum dikonfigurasi untuk course ini', 'danger')
        return redirect(url_for('course.view', course_id=course_id))
    
    # Generate certificate number
    certificate_number = cert_template.get_next_certificate_number()
    
    # Find template JPEG
    template_jpeg = find_certificate_template(course_id)
    if not template_jpeg:
        flash('Template sertifikat tidak ditemukan', 'danger')
        return redirect(url_for('course.view', course_id=course_id))
    
    # Generate certificate PDF in memory
    pdf_bytes = generate_certificate_bytes(
        student_name=current_user.name,
        certificate_number=certificate_number,
        template_path=template_jpeg,
        head_name=cert_template.head_name,
        head_nip=cert_template.head_nip,
        head_title=cert_template.head_title,
        institution_name=cert_template.institution_name,
        institution_npp=cert_template.institution_npp,
        year=cert_template.year
    )
    
    if not pdf_bytes:
        flash('Gagal generate sertifikat', 'danger')
        return redirect(url_for('course.view', course_id=course_id))
    
    # Save to database for audit trail (optional)
    certificate = Certificate.query.filter_by(
        student_id=current_user.id,
        course_id=course_id
    ).first()
    
    if not certificate:
        certificate = Certificate(
            student_id=current_user.id,
            course_id=course_id,
            certificate_path=f"sertifikat_{current_user.id}_{course_id}_{certificate_number}",
            issued_at=datetime.utcnow()
        )
        db.session.add(certificate)
    
    certificate.downloaded_at = datetime.utcnow()
    db.session.commit()
    
    # Stream PDF directly to client
    filename = f"sertifikat_{current_user.name.replace(' ', '_')}_{course.title.replace(' ', '_')}.pdf"
    return send_file(
        pdf_bytes,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )
