import os
import re
import pandas as pd
# pyrefly: ignore [missing-import]
import pymupdf as fitz

# ==============================================================================
# COORDINATES & STYLING CONFIGURATION
# Positioned directly under 'This certificate is proudly present to :'
# ==============================================================================
NAME_X = 421.0       # Center horizontal position on landscape A4 (842 / 2)
NAME_Y = 270.0       # Vertical baseline position above the body text
FONT_SIZE = 28       # Font size for student name
FONT_NAME = "times-bold"  # Font style: 'times-bold', 'times-bolditalic', 'helvetica'
FONT_COLOR = (0.08, 0.08, 0.08)  # Deep Charcoal / Dark Black

TEMPLATE_PDF = "template.pdf"
CLEAN_CSV = "students_clean.csv"
OUTPUT_DIR = "output"

def sanitize_filename(name):
    """Sanitize student name for safe filename creation."""
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name.strip())

def generate_single_certificate(template_path, name, output_path):
    """Generate a single certificate PDF for a given student name."""
    doc = fitz.open(template_path)
    page = doc[0]  # First page

    # Calculate starting X coordinate to align center around NAME_X
    text_length = fitz.get_text_length(name, fontname=FONT_NAME, fontsize=FONT_SIZE)
    start_x = NAME_X - (text_length / 2)

    # Insert student name
    page.insert_text(
        fitz.Point(start_x, NAME_Y),
        name,
        fontsize=FONT_SIZE,
        fontname=FONT_NAME,
        color=FONT_COLOR
    )

    doc.save(output_path)
    doc.close()

def generate_certificates(clean_csv=CLEAN_CSV, template_pdf=TEMPLATE_PDF, output_dir=OUTPUT_DIR, test_one=False):
    if not os.path.exists(clean_csv):
        print(f"[ERROR] Clean CSV file '{clean_csv}' not found. Please run clean_data.py first.")
        return False

    if not os.path.exists(template_pdf):
        print(f"[ERROR] Template PDF file '{template_pdf}' not found.")
        return False

    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(clean_csv)

    if df.empty:
        print("[WARNING] No valid student records found in clean CSV.")
        return False

    print(f"Generating certificates in '{output_dir}/'...")
    success_count = 0
    fail_count = 0

    records_to_process = df.head(1).iterrows() if test_one else df.iterrows()

    for idx, row in records_to_process:
        student_name = str(row['name']).strip()
        safe_name = sanitize_filename(student_name)
        out_filename = os.path.join(output_dir, f"{safe_name}.pdf")

        try:
            generate_single_certificate(template_pdf, student_name, out_filename)
            print(f" [+] Generated certificate for: {student_name} -> {out_filename}")
            success_count += 1
        except Exception as e:
            print(f" [-] Failed to generate certificate for '{student_name}': {e}")
            fail_count += 1

    print(f"\nGeneration Complete: {success_count} succeeded, {fail_count} failed.\n")
    return True

if __name__ == "__main__":
    generate_certificates()
