# File: tools/ocr_tool.py

import os
from dotenv import load_dotenv
import requests
from PIL import Image
import io

# Load environment variables from .env
load_dotenv()

class OCRTool:
    def __init__(self):
        """
        Initialize the OCRTool with the OCR.space API key from environment.
        """
        self.api_url = "https://api.ocr.space/parse/image"
        self.api_key = os.getenv('OCR_SPACE_API_KEY')
        if not self.api_key:
            raise ValueError("OCR_SPACE_API_KEY not set in environment variables.")

    def extract_text(self, file_storage) -> str:
        """
        Reads a Flask-uploaded FileStorage (image), sends it to OCR.space API,
        and returns the extracted text.
        """
        # Read image into bytes
        image_bytes = file_storage.read()

        payload = {
            'isOverlayRequired': False,
            'apikey': self.api_key,
            'language': 'eng'
        }
        files = {
            'file': (file_storage.filename, image_bytes)
        }

        try:
            response = requests.post(self.api_url, data=payload, files=files)
            response.raise_for_status()
            result = response.json()
            parsed_text = result.get('ParsedResults', [{}])[0].get('ParsedText', '')
        except Exception as e:
            parsed_text = f"[ERROR: Could not extract text ({e})]"

        return parsed_text.strip()
