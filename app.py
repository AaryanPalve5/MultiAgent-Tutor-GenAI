# app.py
import os
from flask import Flask, request, jsonify, render_template
from agents.tutor_agent import classify_and_respond
from tools.document_summarizer import summarize_document
from tools.ocr_tool import ocr_image
from tools.youtube_summarizer import summarize_youtube_video
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask_text', methods=['POST'])
def ask_text():
    data = request.json
    query = data.get('query', '')
    response = classify_and_respond(query)
    return jsonify({'response': response})

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'response': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'response': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        summary = summarize_document(path)
        return jsonify({'response': summary})
    else:
        return jsonify({'response': 'File type not allowed'}), 400

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'response': 'No image part'}), 400
    image = request.files['image']
    if image.filename == '':
        return jsonify({'response': 'No selected image'}), 400
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(path)
        text = ocr_image(path)
        if not text.strip():
            return jsonify({'response': 'Could not read text from the image.'})
        # Treat extracted text as a normal query
        response = classify_and_respond(text)
        return jsonify({'response': response})
    else:
        return jsonify({'response': 'Image type not allowed'}), 400

@app.route('/youtube', methods=['POST'])
def youtube():
    data = request.json
    url = data.get('url', '')
    if not url:
        return jsonify({'response': 'No URL provided'}), 400
    summary = summarize_youtube_video(url)
    return jsonify({'response': summary})

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
