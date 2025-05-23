# File: D:\Tutor-AI\tools\email_tool.py

import os
import io
import re
import html
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from email.message import EmailMessage
import smtplib

# Load EMAIL credentials from .env
load_dotenv()
SENDER_EMAIL    = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
SMTP_SERVER     = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT       = int(os.getenv("SMTP_PORT", 587))

class EmailTool:
    def clean_html(self, html_text: str) -> str:
        """
        Convert <br> to newlines, strip HTML tags, unescape entities.
        """
        text = re.sub(r'(?i)<br\s*/?>', '\n', html_text)
        text = re.sub(r'<[^>]+>', '', text)
        return html.unescape(text)

    def generate_pdf(self, conversation_html: str) -> bytes:
        """
        Make a PDF from the full chat conversation (HTML), return bytes.
        """
        # Convert the entire conversation HTML to plain text
        text_content = self.clean_html(conversation_html)

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        margin = 40
        text_obj = p.beginText(margin, height - margin)
        text_obj.setFont("Helvetica", 12)

        # Wrap and draw each line
        for line in text_content.splitlines():
            for chunk in [line[i:i+80] for i in range(0, len(line), 80)]:
                text_obj.textLine(chunk)
        p.drawText(text_obj)
        p.showPage()
        p.save()

        buffer.seek(0)
        return buffer.read()

    def send_pdf_email(self, to_address: str, conversation_html: str) -> None:
        """
        Generate a PDF of the full conversation and email it.
        """
        pdf_bytes = self.generate_pdf(conversation_html)
        filename = "tutor_conversation.pdf"

        msg = EmailMessage()
        msg["From"]    = SENDER_EMAIL
        msg["To"]      = to_address
        msg["Subject"] = "Your Full AI Tutor Conversation"
        msg.set_content("Attached is the PDF containing your full conversation with the AI Tutor.")

        msg.add_attachment(
            pdf_bytes,
            maintype="application",
            subtype="pdf",
            filename=filename
        )

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
