import yt_dlp

url = input("YouTube URL: ")

options = {
    "format": "bestvideo+bestaudio/best",  # or just "best"
    # remove merge_output_format
}

with yt_dlp.YoutubeDL(options) as ydl:
    ydl.download([url])