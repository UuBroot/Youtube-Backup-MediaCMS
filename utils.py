import os
import subprocess
from pathlib import Path
from django.core.files import File
from files.models import Media

YT_DLP_BINARY = os.path.join(os.path.dirname(__file__), 'yt-dlp_linux')
DOWNLOAD_DIR = '/tmp/youtube_downloads'

def download_youtube_video(url, user):
    # Ensure the download folder exists
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # Run yt-dlp
    subprocess.run(
        [
            YT_DLP_BINARY,
            "-f", "bestvideo+bestaudio/best",
            "-o", f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
            url
        ],
        check=True
    )

    # Find all downloaded files
    downloaded_files = list(Path(DOWNLOAD_DIR).glob("*"))
    created_media = []

    for file_path in downloaded_files:
        if file_path.is_file():
            # Sanitize filename
            safe_name = "".join(c for c in file_path.stem if c.isalnum()) + file_path.suffix

            # Open the file first
            with open(file_path, 'rb') as f:
                django_file = File(f, name=safe_name)

                # Create Media with the file attached immediately
                media = Media(
                    user=user,
                    title=file_path.stem,
                    encoding_status='pending'
                )
                media.media_file.save(django_file.name, django_file, save=True)

            created_media.append(media)

            # Optional: clean up local file
            os.remove(file_path)

    return created_media
