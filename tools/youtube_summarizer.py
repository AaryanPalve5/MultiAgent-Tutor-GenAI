# tools/youtube_summarizer.py
from youtube_transcript_api import YouTubeTranscriptApi
from agents.gemini_api import generate_content

def get_video_id(url: str) -> str:
    """
    Extracts the YouTube video ID from a URL.
    """
    # Example URL: https://www.youtube.com/watch?v=VIDEO_ID
    if "v=" in url:
        return url.split("v=")[-1].split("&")[0]
    return url

def summarize_youtube_video(youtube_url: str) -> str:
    """
    Fetches the transcript of the YouTube video and returns a summary.
    """
    video_id = get_video_id(youtube_url)
    try:
        # Fetch transcript (default to English)
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([entry['text'] for entry in transcript_list])
    except Exception as e:
        return f"Could not retrieve transcript: {e}"

    # Ask Gemini to summarize the transcript
    prompt = f"Summarize the following lecture:\n\n{full_text}"
    return generate_content(prompt)
