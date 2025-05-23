# File: tools/youtube_summarizer.py

import os
import re
import tempfile
import shutil
from dotenv import load_dotenv
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)
from langchain_google_genai import GoogleGenerativeAI
import whisper
import yt_dlp

# Load environment variables
load_dotenv()

# Initialize Gemini LLM
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GEMINI_API_KEY not set in environment variables.")

llm = GoogleGenerativeAI(
    model="models/gemini-1.5-flash",
    google_api_key=GOOGLE_API_KEY
)

class YouTubeSummarizerTool:
    def __init__(self):
        # Load Whisper model once for audio transcription fallback
        self.whisper_model = whisper.load_model("base")

    def extract_video_id(self, url: str) -> str:
        match = re.search(
            r"(?:youtube\.com/watch\?v=|youtu\.be/)([A-Za-z0-9_-]{11})", url
        )
        return match.group(1) if match else None

    def fetch_transcript(self, video_id: str):
        try:
            return YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        except (TranscriptsDisabled, VideoUnavailable, NoTranscriptFound):
            return None
        except Exception:
            # Fallback: list and fetch manually
            try:
                transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
                transcript = transcripts.find_transcript(["en", "en-US"])
                return transcript.fetch()
            except Exception:
                return None

    def download_audio(self, url: str):
        temp_dir = tempfile.mkdtemp()
        audio_path = os.path.join(temp_dir, "audio.mp3")
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': audio_path,
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return audio_path, temp_dir
        except Exception:
            shutil.rmtree(temp_dir)
            return None, None

    def transcribe_audio(self, audio_path: str) -> str:
        try:
            result = self.whisper_model.transcribe(audio_path, language='en')
            return result.get('text', '')
        except Exception:
            return ''

    def summarize(self, url: str) -> str:
        video_id = self.extract_video_id(url)
        if not video_id:
            return "Invalid YouTube URL."

        transcript_list = self.fetch_transcript(video_id)
        if transcript_list:
            full_text = " ".join(seg.get("text", "") for seg in transcript_list)
        else:
            # Fallback to audio transcription
            audio_path, temp_dir = self.download_audio(url)
            if audio_path:
                full_text = self.transcribe_audio(audio_path)
                shutil.rmtree(temp_dir)
                if not full_text.strip():
                    return "Could not transcribe audio. Video may be too long or unavailable."
            else:
                return "Could not retrieve transcript or audio for this video."

        # Limit size for LLM input
        MAX_CHARS = 18000
        if len(full_text) > MAX_CHARS:
            full_text = full_text[:MAX_CHARS] + "\n...[truncated]"

        prompt = (
            "Summarize the following text from a YouTube video transcript into concise bullet points. "
            "Ensure the total summary does not exceed 250 words:\n\n"
            f"{full_text}"
        )

        try:
            summary = llm.invoke(prompt)
            # If response is a LangChain object
            if hasattr(summary, 'content'):
                return summary.content
            return str(summary)
        except Exception as e:
            return f"Error generating summary: {e}"
