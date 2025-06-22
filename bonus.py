import pymupdf  # PyMuPDF
from PIL import Image
import pytesseract
import os

# ✅ Set tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_images_and_text_from_pdf(pdf_path, output_dir):
    doc = pymupdf.open(pdf_path)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    os.makedirs(output_dir, exist_ok=True)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=300)

        # Save image
        image_path = os.path.join(output_dir, f"{base_name}_page{page_num + 1}.png")
        pix.save(image_path)
        print(f"Saved image: {image_path}")

        # OCR - Extract text from image
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)

        # Save text
        text_path = os.path.join(output_dir, f"{base_name}_page{page_num + 1}.txt")
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"📝 Saved OCR text: {text_path}")

    doc.close()

# Run for all PDFs in folder
pdf_folder = "output_embedded"  # Folder containing PDF files
output_folder = "output_images_text"

for filename in os.listdir(pdf_folder):
    if filename.lower().endswith(".pdf"):
        extract_images_and_text_from_pdf(
            os.path.join(pdf_folder, filename),
            output_folder
        )

