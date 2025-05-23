# File: app.py

from flask import Flask, render_template, request, session
from agents.mentor_agent import MentorAgent
import re, os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed for session

mentor_agent = MentorAgent()

def simple_format_markdown(text):
    """Lightweight markdown formatting for **bold**, *italic*, and `code`."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    text = text.replace('\n', '<br>')
    return text

@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize conversation history in session if not present
    if 'conversation' not in session:
        session['conversation'] = []
    
    if request.method == 'POST':
        user_input = request.form.get('question')
        # Append user's message to conversation
        conversation = session['conversation']
        conversation.append({'role': 'user', 'message': simple_format_markdown(user_input)})

        # Get response from mentor agent (subject or summarizer)
        answer, subject = mentor_agent.handle_question(user_input)
        # Format answer (it may contain markdown-like symbols)
        answer_html = simple_format_markdown(answer)
        conversation.append({'role': 'assistant', 'message': answer_html})

        # Save back to session
        session['conversation'] = conversation

    # Render the chat interface with the conversation history
    return render_template('index.html', conversation=session.get('conversation', []))

if __name__ == "__main__":
    app.run(debug=True)
