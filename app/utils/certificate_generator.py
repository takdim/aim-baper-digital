"""
Certificate generation utility
Generate certificate PDF on-the-fly dengan overlay text pada JPEG template
"""
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from pathlib import Path
import os


def generate_certificate_bytes(
    student_name,
    certificate_number,
    template_path,
    head_name,
    head_nip,
    head_title,
    institution_name,
    institution_npp,
    year
):
    """
    Generate certificate PDF as BytesIO (in-memory) dengan overlay text di atas JPEG template
    Hanya tampilkan NAMA MAHASISWA saja (sesuai template JPEG yang sudah punya data lainnya)
    
    Returns:
        BytesIO object jika sukses, None jika gagal
    """
    try:
        if not os.path.exists(template_path):
            print(f"Template tidak ditemukan: {template_path}")
            return None
        
        img = Image.open(template_path).convert('RGB')
        draw = ImageDraw.Draw(img)
        
        base_static_dir = Path(__file__).resolve().parents[1] / 'static'

        # Prioritaskan font custom sertifikat dari project
        font_candidates = [
            str(base_static_dir / 'font' / 'asteria_font.ttf'),
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
            "/System/Library/Fonts/HelveticaNeue.ttc",
            "/System/Library/Fonts/SFNS.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
        font_path = next((path for path in font_candidates if os.path.exists(path)), None)

        try:
            if font_path:
                font_name = ImageFont.truetype(font_path, 80)
            else:
                font_name = ImageFont.load_default()
        except Exception:
            font_name = ImageFont.load_default()
        
        width, height = img.size
        scale_factor = width / 2480.0
        
        # Reload font dengan size scaled berdasarkan template size
        try:
            if font_path and os.path.exists(font_path):
                # Jaga ukuran font tetap masuk akal agar render teks tidak gagal
                font_size = max(36, min(180, int(120 * scale_factor)))
                font_name = ImageFont.truetype(font_path, font_size)
        except Exception:
            pass
        
        text_color = (0, 0, 0)
        
        # HANYA TAMPILKAN NAMA MAHASISWA (center, ~50% dari atas)
        # Posisi nama di tengah-tengah sertifikat
        y_name = int(height * 0.40)
        text_bbox = draw.textbbox((0, 0), student_name, font=font_name)
        x_name = (width - (text_bbox[2] - text_bbox[0])) // 2
        draw.text((x_name, y_name), student_name, fill=text_color, font=font_name)
        
        # Convert image directly to PDF using PIL
        pdf_bytes = BytesIO()
        img.save(pdf_bytes, 'PDF')
        pdf_bytes.seek(0)
        
        return pdf_bytes
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def find_certificate_template(course_id):
    """Find certificate template image using paths relative to the app package."""
    static_dir = Path(__file__).resolve().parents[1] / 'static'
    template_dir = static_dir / 'uploads' / 'certificate_templates'

    candidates = [
        template_dir / f'course_{course_id}_template.jpg',
        template_dir / f'course_{course_id}_template.jpeg',
        template_dir / f'course_{course_id}_template.png',
        template_dir / 'template.jpg',
        template_dir / 'template.jpeg',
        template_dir / 'template.png',
        static_dir / 'resource' / 'template_certif_baper.JPEG',
    ]

    for candidate in candidates:
        if candidate.exists():
            return str(candidate)

    if template_dir.exists():
        for pattern in ('*.jpg', '*.jpeg', '*.JPG', '*.JPEG', '*.png', '*.PNG'):
            for file in template_dir.glob(pattern):
                if 'template' in file.name.lower() or 'sertifikat' in file.name.lower():
                    return str(file)

    return None
