# YouTube Video Summarizer

This project provides a tool to automatically fetch transcripts from YouTube videos and generate concise summaries of their content.

## Features

- Fetch transcripts from YouTube videos using video URLs
- Generate AI-powered summaries of video content
- (Future) Support for monitoring subscribed channels
- (Future) Email notifications using Amazon SES

## Setup

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the script with a YouTube video URL:

```bash
python summarize_video.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

## Future Enhancements

- Add support for monitoring multiple YouTube channels
- Implement email notifications using Amazon SES
- Add support for different summary formats and lengths
- Add support for multiple languages
- Add a web interface for easier interaction
