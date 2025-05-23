# File: tools/youtube_summarizer.py

import os
import re
from dotenv import load_dotenv
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)
from langchain_google_genai import GoogleGenerativeAI

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
    def extract_video_id(self, url: str) -> str:
        """Pull the 11-char video ID from a YouTube URL."""
        match = re.search(r"(?:youtube\.com/watch\?v=|youtu\.be/)([A-Za-z0-9_-]{11})", url)
        return match.group(1) if match else None

    def fetch_transcript(self, video_id: str):
        """
        Attempt to fetch the English transcript, with specific errors handled.
        Returns a list of {"text": ...} segments or None on failure.
        """
        try:
            return YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        except TranscriptsDisabled:
            return "Transcripts are disabled for this video."
        except VideoUnavailable:
            return "The video is unavailable or does not exist."
        except NoTranscriptFound:
            return "No transcript found for this video."
        except Exception as e:
            # Rate-limit handling
            if "429" in str(e) or "Too Many Requests" in str(e):
                return "YouTube transcript API rate limit exceeded. Please try again later."
            return None

    def summarize(self, url: str) -> str:
        """
        Fetch the transcript and ask Gemini to produce concise bullet points
        (max 250 words). Returns either the summary or an error string.
        """
        video_id = self.extract_video_id(url)
        if not video_id:
            return "Invalid YouTube URL."

        transcript_result = self.fetch_transcript(video_id)
        # If a descriptive error string was returned, pass it through:
        if isinstance(transcript_result, str):
            return transcript_result
        # If transcript_result is None, a generic failure:
        if transcript_result is None:
            return "Could not retrieve transcript for this video."

        # Combine text segments
        full_text = " ".join(seg.get("text", "") for seg in transcript_result)
        if not full_text.strip():
            return "Transcript was empty or could not be parsed."

        # Truncate to safe size for LLM
        MAX_CHARS = 18000
        if len(full_text) > MAX_CHARS:
            full_text = full_text[:MAX_CHARS] + "\n...[truncated]"

        prompt = (
            "Summarize the following text from a YouTube video transcript into concise bullet points. "
            "Ensure the entire summary does not exceed 250 words:\n\n"
            f"{full_text}"
        )

        try:
            # Use .invoke for LangChain GoogleGenerativeAI
            summary = llm.invoke(prompt)
            # If LangChain returns an object with .content:
            if hasattr(summary, "content"):
                return summary.content
            return str(summary)
        except Exception as e:
            return f"Error generating summary: {e}"
