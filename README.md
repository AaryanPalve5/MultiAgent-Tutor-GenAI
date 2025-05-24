# MultiAgent GenAI Tutor

### Live Demo - Deployed Link
[![Live Demo Link](https://img.shields.io/badge/demo-video-grey)](https://multiagent-tutor-genai-1.onrender.com/)  

### Video Demonstration of MultiAgent GenAI Tutor
[![Demo Video Link](https://img.shields.io/badge/demo-video-grey)](https://www.youtube.com/watch?v=rvKiMwnTaLM)  



A **Flask**-powered web application that implements a **multi-agent** tutoring assistant using Google’s Gemini LLM and specialized tools. Users can ask questions in math, physics, chemistry, or biology; upload images for OCR; or paste YouTube URLs for AI-generated summaries.

---

## Table of Contents
1. [Features](#features)  
2. [Architecture & Flow](#architecture--flow)  
3. [Setup & Installation](#setup--installation)  
4. [Environment Variables](#environment-variables)  
5. [Running Locally](#running-locally)  
6. [Deployment](#deployment)  
7. [Folder Structure](#folder-structure)  
8. [Screenshots](#screenshots)  
9. [Agent–Tool Interaction](#agent–tool-interaction)  
10. [Challenges & Solutions](#challenges--solutions)  

---

## Features
- **Text Chat**: Ask any question in math, physics, chemistry, or biology.  
- **OCR**: Upload an image of a question; gets converted to text.  
- **YouTube Summarizer**: Paste a `youtube.com` or `youtu.be` link and receive concise bullet points.  
- **Calculator**: Automatic math expression evaluation via `CalculatorTool`.  
- **Email Transcript**: Receive a PDF copy of your full chat via email.

---

## Architecture & Flow

![MultiAgent-Tutor-GenAI-flowchart](https://raw.githubusercontent.com/1543siddhant/MultiAgent-Tutor-GenAI/refs/heads/main/static/MultiAgent-WorkFlow.png)

1. **User Input**  
   - Text question → MentorAgent  
   - Image upload → OCRTool → text → MentorAgent  
   - YouTube URL → YouTubeSummarizerTool  

2. **MentorAgent**  
   - Detects YouTube URLs (regex).  
   - Otherwise, classifies the subject (math/physics/chemistry/biology) via a Gemini prompt.  

3. **TutorAgent**  
   - Routes by subject to the appropriate agent (MathAgent, PhysicsAgent, BiologyAgent).  
   - If subject is unknown or unsupported, returns a friendly fallback.

4. **Subject Agents**  
   - **MathAgent**: Checks for numeric expressions, uses CalculatorTool if found; else asks Gemini.  
   - **PhysicsAgent/BiologyAgent/ChemistryAgent**: Delegate directly to Gemini with subject-specific prompts.

5. **Tools**  
   - **CalculatorTool**: Safe `eval` of math expressions.  
   - **OCRTool**: PIL + Tesseract OCR.  
   - **YouTubeSummarizerTool**: Fetches transcript, uses Gemini to summarize.  
   - **EmailTool**: Converts chat to PDF and emails it.

---

## Setup & Installation

1. **Clone**  
   ```bash
   git clone https://github.com/yourusername/MultiAgent-Tutor-GenAI.git
   cd MultiAgent-Tutor-GenAI
   ```
   
2. **Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install --upgrade pip
   pip install -r requirements.txt

   Tesseract OCR
   Ubuntu: sudo apt-get install tesseract-ocr
   Windows: Download MSI from https://github.com/tesseract-ocr/tesseract
  ```

```

### Tesseract OCR

#### Ubuntu

```bash
sudo apt-get install tesseract-ocr
```

#### Windows

Download and install from: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)

---

## Environment Variables

Create a `.env` file in the project root:

```ini
# Gemini LLM API
GEMINI_API_KEY=your_google_gemini_api_key

# Flask session
FLASK_SECRET_KEY=a_random_secret_key

# (Optional) EmailTool SMTP
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@example.com
SENDER_PASSWORD=your_email_password
```

---

## Running Locally

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## Deployment

Deployed on Render.
**Live App:** [https://your-app-on-render.example.com](https://your-app-on-render.example.com)
(Replace with your actual URL once available.)

---

## Folder Structure

```bash
MultiAgent-Tutor-GenAI/
├── agents/
│   ├── mentor_agent.py      # Orchestrator
│   ├── subject_classifier.py
│   ├── tutor_agent.py
│   ├── math_agent.py
│   ├── physics_agent.py
│   ├── biology_agent.py
│   └── chemistry_agent.py
├── tools/
│   ├── calculator_tool.py
│   ├── ocr_tool.py
│   ├── youtube_summarizer.py
│   └── email_tool.py
├── templates/
│   └── index.html
├── static/
│   └── ss1.png
│   └── ss2.png
├── .env
├── requirements.txt
└── app.py
```

---

## Screenshots

![MultiAgent-Tutor-GenAI](https://raw.githubusercontent.com/1543siddhant/MultiAgent-Tutor-GenAI/refs/heads/main/static/output1.png)
![MultiAgent-Tutor-GenAI](https://raw.githubusercontent.com/1543siddhant/MultiAgent-Tutor-GenAI/refs/heads/main/static/output2.png)
![MultiAgent-Tutor-GenAI](https://raw.githubusercontent.com/1543siddhant/MultiAgent-Tutor-GenAI/refs/heads/main/static/output5.png)
---

## Agent–Tool Interaction

**Flow:**

```
User → MentorAgent → [OCRTool | Subject Classifier] → TutorAgent → [CalculatorTool or Gemini LLM] → Response
```

**Extensibility:**

Add new agents (e.g. `HistoryAgent`) by implementing `answer()` and registering it in `tutor_agent.py`.

**Prompt Control:**

Carefully engineered prompts ensure consistent outputs:

* Single-word classification
* 250-word bullet summaries

---

## Challenges & Solutions

### Subject Classification Errors

**Fix:** Prompt refinement to enforce exact category keywords and handle “unknown” fallback.

### OCR Misreads

**Fix:** Pre-processing images (contrast adjustments) and error handling for blank extractions.

### LLM Hallucinations in Math

**Fix:** Offload pure computations to the `CalculatorTool` whenever possible.

### Session Size

**Fix:** Consider truncating very long transcripts or migrating to a database for persistence.

---
