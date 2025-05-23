# app.py

import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

from agents.tutor_agent import classify_and_respond
from tools.document_summarizer import summarize_document
from tools.ocr_tool import ocr_image
from tools.youtube_summarizer import summarize_youtube_video

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask_text', methods=['POST'])
def ask_text():
    data = request.get_json() or {}
    query = data.get('query', '').strip()
    if not query:
        return jsonify(answer="Please enter a question."), 400

    # This will now always return a string, even on errors
    answer = classify_and_respond(query)
    return jsonify(answer=answer)

@app.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if not file or file.filename == '' or not allowed_file(file.filename):
        return jsonify(answer="Invalid or missing document."), 400

    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    summary = summarize_document(path)
    return jsonify(answer=summary)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    img = request.files.get('image')
    if not img or img.filename == '' or not allowed_file(img.filename):
        return jsonify(answer="Invalid or missing image."), 400

    filename = secure_filename(img.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img.save(path)

    text = ocr_image(path).strip()
    if not text:
        return jsonify(answer="Could not read text from the image.")

    answer = classify_and_respond(text)
    return jsonify(answer=answer)

@app.route('/youtube', methods=['POST'])
def youtube():
    data = request.get_json() or {}
    url = data.get('url', '').strip()
    if not url:
        return jsonify(answer="No YouTube URL provided."), 400

    summary = summarize_youtube_video(url)
    return jsonify(answer=summary)

if __name__ == '__main__':
    app.run(debug=True)
