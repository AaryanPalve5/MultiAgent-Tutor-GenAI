# File: youtube_summarizer.py

from youtube_transcript_api import YouTubeTranscriptApi
from agents.gemini_api import llm
import re

class YouTubeSummarizerTool:
    def summarize(self, url):
        # Extract the video ID from the URL (handles both youtube.com and youtu.be links)
        video_id_match = re.search(
            r"(?:youtube\.com/watch\?v=|youtu\.be/)([A-Za-z0-9_-]{11})", url
        )
        if not video_id_match:
            return "Invalid YouTube URL."
        video_id = video_id_match.group(1)

        try:
            # Fetch the transcript (a list of {"text": "...", ...} entries)
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        except Exception as e:
            return "Could not retrieve transcript for this video."

        # Combine all text segments into one string
        full_text = " ".join([seg["text"] for seg in transcript_list])

        # Construct a prompt asking Gemini to summarize with bullet points and a 250-word limit
        prompt = (
            "Summarize the following text from a YouTube video transcript into concise bullet points. "
            "Make sure the total summary is no more than 250 words:\n\n"
            f"{full_text}"
        )
        summary = llm(prompt)  # Directly call the Gemini model with the prompt
        return summary
