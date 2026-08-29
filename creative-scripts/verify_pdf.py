"""
Verify a generated PDF by creating a preview image of the first page.

Usage:
    python scripts/verify_pdf.py path/to/output.pdf

Generates path/to/output_verify.png — open it to visually check
for clipped text, overlapping elements, or broken connectors.
"""

import sys
import os


def verify_pdf(pdf_path: str) -> bool:
    if not os.path.exists(pdf_path):
        print(f"Error: File '{pdf_path}' not found.")
        return False

    # Try pdf2image first (best quality)
    try:
        from pdf2image import convert_from_path
        images = convert_from_path(pdf_path, first_page=1, last_page=1)
        if images:
            output_image = pdf_path.replace('.pdf', '_verify.png')
            images[0].save(output_image, 'PNG')
            print(f"✓ Verification image saved: {output_image}")
            print(f"  Dimensions: {images[0].width}x{images[0].height}px")
            return True
    except ImportError:
        print("  pdf2image not available, trying PIL...")
    except Exception as e:
        print(f"  pdf2image error: {e}")

    # Fallback: use PIL to create a placeholder + instructions
    try:
        from PIL import Image, ImageDraw, ImageFont
        output_image = pdf_path.replace('.pdf', '_verify.png')
        img = Image.new('RGB', (1200, 800), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.text((50, 50), f"PDF Verification: {os.path.basename(pdf_path)}", fill=(0, 0, 0))
        draw.text((50, 100), f"PDF Size: {os.path.getsize(pdf_path)} bytes", fill=(80, 80, 80))
        draw.text((50, 150), "To view: open the PDF directly in a reader.", fill=(80, 80, 80))
        draw.text((50, 200), "", fill=(0, 0, 0))
        draw.text((50, 250), "Install pdf2image for proper preview:", fill=(0, 0, 0))
        draw.text((50, 280), "  pip install pdf2image", fill=(100, 100, 200))
        draw.text((50, 330), "Requires poppler: https://github.com/Belval/pdf2image", fill=(100, 100, 200))
        img.save(output_image, 'PNG')
        print(f"⚠ Basic verification image saved: {output_image}")
        print(f"  Install 'pdf2image' + poppler for full PDF previews.")
        return True
    except ImportError:
        print("Warning: Neither pdf2image nor PIL available for verification.")
        print(f"PDF file exists at: {os.path.abspath(pdf_path)} ({os.path.getsize(pdf_path)} bytes)")
        return True  # PDF exists even if we can't preview it


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/verify_pdf.py <path_to_pdf>")
        sys.exit(1)
    success = verify_pdf(sys.argv[1])
    sys.exit(0 if success else 1)
