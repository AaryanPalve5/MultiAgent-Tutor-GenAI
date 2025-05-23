# File: tools/ocr_tool.py

import pytesseract
from PIL import Image

# Ensure pytesseract knows where the tesseract binary is
# On Debian/Ubuntu systems, the binary is typically at /usr/bin/tesseract
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

class OCRTool:
    def extract_text(self, file_storage) -> str:
        """
        Reads a Flask-uploaded FileStorage (image), runs OCR, returns extracted text.
        """
        # Open the uploaded image stream with PIL and convert to RGB
        image = Image.open(file_storage.stream).convert("RGB")
        # Use pytesseract to extract text
        text = pytesseract.image_to_string(image)
        return text
