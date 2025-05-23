# File: D:\Tutor-AI\tools\ocr_tool.py

import pytesseract
from PIL import Image

class OCRTool:
    def extract_text(self, file_storage) -> str:
        """
        Reads a Flask-uploaded FileStorage (image), runs OCR, returns extracted text.
        """
        # PIL can open directly from the file stream
        image = Image.open(file_storage.stream).convert("RGB")
        # pytesseract to extract
        text = pytesseract.image_to_string(image)
        return text
