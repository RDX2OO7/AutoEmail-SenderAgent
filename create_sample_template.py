# pyrefly: ignore [missing-import]
import pymupdf as fitz

def draw_centered_text(page, center_x, y, text, fontsize=12, fontname="helv", color=(0, 0, 0)):
    length = fitz.get_text_length(text, fontname=fontname, fontsize=fontsize)
    start_x = center_x - (length / 2)
    page.insert_text(
        fitz.Point(start_x, y),
        text,
        fontsize=fontsize,
        fontname=fontname,
        color=color
    )

def generate_sample_template(filename="template.pdf"):
    # Create landscape A4 document (842 x 595 points)
    doc = fitz.open()
    page = doc.new_page(width=842, height=595)

    # Colors
    orange = (216 / 255, 67 / 255, 21 / 255)     # #D84315 - Bright Orange
    dark_gray = (50 / 255, 50 / 255, 50 / 255)  # #323232
    black = (20 / 255, 20 / 255, 20 / 255)
    light_gray = (180 / 255, 180 / 255, 180 / 255)

    shape = page.new_shape()

    # --- Geometric Corner Accents ---
    # Top-left orange & gray diagonal banners
    shape.draw_polyline([fitz.Point(0, 0), fitz.Point(180, 0), fitz.Point(0, 180)])
    shape.finish(color=orange, fill=orange)

    shape.draw_polyline([fitz.Point(0, 70), fitz.Point(230, 0), fitz.Point(260, 0), fitz.Point(0, 130)])
    shape.finish(color=dark_gray, fill=dark_gray)

    # Bottom-right orange & gray diagonal banners
    shape.draw_polyline([fitz.Point(842, 595), fitz.Point(662, 595), fitz.Point(842, 415)])
    shape.finish(color=orange, fill=orange)

    shape.draw_polyline([fitz.Point(842, 525), fitz.Point(612, 595), fitz.Point(582, 595), fitz.Point(842, 465)])
    shape.finish(color=dark_gray, fill=dark_gray)

    # --- Header Title Section ---
    draw_centered_text(page, 421, 140, "CERTIFICATE", fontsize=38, fontname="times-bold", color=orange)
    
    # Decorative lines beside "OF PARTICIPATION"
    shape.draw_line(fitz.Point(260, 172), fitz.Point(310, 172))
    shape.finish(color=orange, width=1.5)
    
    draw_centered_text(page, 421, 176, "O F   P A R T I C I P A T I O N", fontsize=14, fontname="helvetica", color=dark_gray)

    shape.draw_line(fitz.Point(532, 172), fitz.Point(582, 172))
    shape.finish(color=orange, width=1.5)

    # Subtitle
    draw_centered_text(page, 421, 215, "This certificate is proudly present to :", fontsize=14, fontname="helv", color=dark_gray)

    # --- Name Placeholder Area ---
    # Space reserved between Y=230 and Y=310 (Baseline at Y=275)
    # Light guide line (optional placeholder)
    shape.draw_line(fitz.Point(250, 285), fitz.Point(592, 285))
    shape.finish(color=(230 / 255, 230 / 255, 230 / 255), width=0.5)

    # --- Body Content ---
    draw_centered_text(page, 421, 318, "has successfully participated in and demonstrated commendable knowledge and enthusiasm in the", fontsize=11, fontname="helv", color=dark_gray)

    # Competition Title
    draw_centered_text(page, 421, 345, "ENTREPRENEURSHIP QUIZ COMPETITION", fontsize=16, fontname="times-bold", color=orange)
    draw_centered_text(page, 421, 368, "Held on 21 AUGUST, 2026", fontsize=12, fontname="helv", color=dark_gray)

    # Appreciation Paragraphs
    draw_centered_text(page, 421, 402, "Your participation and interest in entrepreneurship reflect a spirit of", fontsize=11, fontname="helv", color=dark_gray)
    draw_centered_text(page, 421, 418, "innovation, creativity, and leadership.", fontsize=11, fontname="helv", color=dark_gray)
    
    draw_centered_text(page, 421, 442, "We congratulate you on your achievement and wish you continued", fontsize=11, fontname="helv", color=dark_gray)
    draw_centered_text(page, 421, 458, "success in all your future entrepreneurial endeavors.", fontsize=11, fontname="helv", color=dark_gray)

    # --- Signatures Row ---
    # Signatory 1
    draw_centered_text(page, 150, 520, "MR. YOGESH CHANDAWADE", fontsize=9, fontname="times-bold", color=black)
    draw_centered_text(page, 150, 532, "MRS. RAJESHRI ITKARKAR", fontsize=8, fontname="helv", color=dark_gray)
    draw_centered_text(page, 150, 544, "FACULTY COORDINATORS", fontsize=8, fontname="times-bold", color=dark_gray)

    # Signatory 2
    draw_centered_text(page, 320, 520, "DR. S.B. DHONDE", fontsize=9, fontname="times-bold", color=black)
    draw_centered_text(page, 320, 532, "HOD (E&TC)", fontsize=8, fontname="helv", color=dark_gray)

    # Signatory 3
    draw_centered_text(page, 480, 520, "DR. VIDYA N PATIL", fontsize=9, fontname="times-bold", color=black)
    draw_centered_text(page, 480, 532, "DEAN OF IIEC", fontsize=8, fontname="helv", color=dark_gray)

    # Signatory 4
    draw_centered_text(page, 650, 520, "DR. D.S BORMANE", fontsize=9, fontname="times-bold", color=black)

    draw_centered_text(page, 650, 532, "THE PRINCIPAL", fontsize=8, fontname="helv", color=dark_gray)
    draw_centered_text(page, 650, 544, "AISSMS-COE", fontsize=8, fontname="helv", color=dark_gray)

    shape.commit()
    doc.save(filename)
    doc.close()
    print(f"Template created matching AISSMS design: {filename}")

if __name__ == "__main__":
    generate_sample_template()
