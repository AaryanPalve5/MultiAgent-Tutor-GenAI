# tools/ocr_tool.py
import pytesseract
from PIL import Image

def ocr_image(image_path: str) -> str:
    """
    Extract text from an image file using Tesseract OCR.
    """
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text.strip()
