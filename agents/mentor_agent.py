# File: D:\Tutor-AI\agents\mentor_agent.py

import os
import sys
import re

# ─── Add project root to sys.path so we can import from agents/ and tools/ ───
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Also add the tools directory to sys.path
TOOLS_DIR = os.path.join(PROJECT_ROOT, "tools")
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

from agents.subject_classifier import classify_subject
from agents.tutor_agent import TutorAgent
from tools.youtube_summarizer import YouTubeSummarizerTool


class MentorAgent:
    def __init__(self):
        self.tutor = TutorAgent()
        self.summarizer = YouTubeSummarizerTool()

    def handle_question(self, question):
        # 1) If the user pasted a YouTube URL, run the summarizer tool
        if re.search(r"(youtu\.be/|youtube\.com/watch\?v=)", question):
            summary = self.summarizer.summarize(question)
            return summary, "YouTube Video"

        # 2) Otherwise, classify subject and route to the math/physics/biology agent
        subject = classify_subject(question)
        answer = self.tutor.route_question(subject, question)
        return answer, subject
