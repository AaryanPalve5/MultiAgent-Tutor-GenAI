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
    def summarize(self, url: str) -> str:
        """
        Summarize a YouTube video by fetching its transcript and asking Gemini to
        produce concise bullet points (<=250 words).
        """
        # Extract video ID
        match = re.search(
            r"(?:youtube\.com/watch\?v=|youtu\.be/)([A-Za-z0-9_-]{11})", url
        )
        if not match:
            return "Invalid YouTube URL."
        video_id = match.group(1)

        # Fetch transcript with robust error handling
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(
                video_id, languages=["en"]
            )
        except TranscriptsDisabled:
            return "Transcripts are disabled for this video."
        except VideoUnavailable:
            return "The video is unavailable or does not exist."
        except NoTranscriptFound:
            return "No transcript found for this video."
        except Exception:
            # Fallback: list and fetch manually
            try:
                transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
                transcript = transcripts.find_transcript(["en", "en-US"])
                transcript_list = transcript.fetch()
            except Exception as e:
                return f"Could not retrieve transcript for this video: {e}"

        # Combine transcript text
        full_text = " ".join(seg.get("text", "") for seg in transcript_list)

        # Build prompt
        prompt = (
            "Summarize the following text from a YouTube video transcript into concise bullet points. "
            "Ensure the total summary does not exceed 250 words:\n\n"
            f"{full_text}"
        )

        # Call Gemini LLM
        try:
            summary = llm.invoke(prompt)
        except Exception as e:
            return f"Error generating summary: {e}"

        return summary
