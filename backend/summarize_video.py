#!/usr/bin/env python3

import os
import sys
from typing import Optional, Tuple
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from openai import OpenAI
from dotenv import load_dotenv

def extract_video_id(url: str) -> Optional[str]:
    """Extract the video ID from a YouTube URL."""
    if 'youtu.be' in url:
        return url.split('/')[-1].split('?')[0]
    elif 'youtube.com' in url:
        if 'v=' in url:
            return url.split('v=')[1].split('&')[0]
    return None

def get_transcript(video_id: str) -> str:
    """Fetch and format the transcript for a given YouTube video ID."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = TextFormatter()
        return formatter.format_transcript(transcript)
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        sys.exit(1)

def summarize_text(text: str, api_key: str) -> Tuple[str, str]:
    """Generate a title and summary of the given text using OpenAI's API."""
    client = OpenAI(api_key=api_key)
    
    try:
        # First, generate a title
        title_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates concise, engaging titles for YouTube videos based on their content. The title should be descriptive but brief (5-10 words), and should capture the main topic or theme of the video. Do not include any special characters or formatting, just plain text."},
                {"role": "user", "content": f"Create a concise, engaging title for a YouTube video with the following transcript:\n\n{text[:1000]}..."}  # Use first 1000 chars for context
            ],
            max_tokens=50,
            temperature=0.7
        )
        title = title_response.choices[0].message.content.strip()

        # Then generate the summary
        summary_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes YouTube video transcripts. Format your response as a bullet point list, with each main point or key takeaway starting with a '-'. Focus on the most important information and keep each point concise. Aim for 5-7 key points."},
                {"role": "user", "content": f"Please summarize the following transcript as bullet points:\n\n{text}"}
            ],
            max_tokens=500,
            temperature=0.7
        )
        summary = summary_response.choices[0].message.content

        return title, summary
    except Exception as e:
        print(f"Error generating content: {e}")
        sys.exit(1)

def main():
    # Load environment variables
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables")
        sys.exit(1)

    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python summarize_video.py <youtube_url>")
        sys.exit(1)

    # Get video URL from command line
    video_url = sys.argv[1]
    video_id = extract_video_id(video_url)
    
    if not video_id:
        print("Error: Invalid YouTube URL")
        sys.exit(1)

    transcript = get_transcript(video_id)
    title, summary = summarize_text(transcript, api_key)
    
    # Print the title and summary
    print(f"\n=== {title} ===")
    print(summary)
    
    # Return both title and summary for the API
    return title, summary

if __name__ == "__main__":
    main() 