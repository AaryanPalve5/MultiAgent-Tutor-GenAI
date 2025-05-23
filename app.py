# File: D:\Tutor-AI\app.py

import os
import re
from flask import (
    Flask, render_template, request, session,
    redirect, url_for, flash
)
from dotenv import load_dotenv

# Load environment (including email creds)
load_dotenv()

from agents.mentor_agent import MentorAgent
from tools.email_tool import EmailTool

app = Flask(__name__)
app.secret_key = os.urandom(24)

mentor_agent = MentorAgent()
email_tool   = EmailTool()

def simple_format_markdown(text):
    """Convert **bold**, *italic*, `code`, and newlines to HTML."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    return text.replace('\n', '<br>')

@app.route('/', methods=['GET', 'POST'])
def index():
    conv = session.get('conversation', [])

    if request.method == 'POST':
        # User message
        user_input = request.form.get('question')
        conv.append({
            'role': 'user',
            'message': simple_format_markdown(user_input)
        })

        # AI response
        answer, _ = mentor_agent.handle_question(user_input)
        conv.append({
            'role': 'assistant',
            'message': simple_format_markdown(answer)
        })

        session['conversation'] = conv
        return redirect(url_for('index'))

    return render_template('index.html', conversation=conv)

@app.route('/send_email', methods=['POST'])
def send_email():
    recipient = request.form.get('recipient')
    if not recipient:
        flash("Please enter a valid email address.", "error")
        return redirect(url_for('index'))

    conv = session.get('conversation', [])
    if not conv:
        flash("No conversation to send.", "error")
        return redirect(url_for('index'))

    # Build a single HTML string of the entire chat
    html_parts = []
    for msg in conv:
        prefix = "You: " if msg['role']=='user' else "Tutor: "
        html_parts.append(f"<strong>{prefix}</strong>{msg['message']}<br>")
    full_html = "\n".join(html_parts)

    try:
        email_tool.send_pdf_email(recipient, full_html)
        flash(f"📧 PDF of entire chat sent to {recipient}!", "success")
    except Exception as e:
        flash(f"Failed to send email: {e}", "error")

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
