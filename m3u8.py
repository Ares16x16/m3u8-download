import subprocess
import os
from urllib.parse import parse_qs, urlparse


def convert_m3u8_to_mp3(m3u8_url, output_name):
    """
    Convert an .m3u8 URL to an .mp3 file using FFmpeg.

    Args:
        m3u8_url (str): The .m3u8 URL to download.
        output_name (str): Base name for the output files (without extension).
    """
    temp_mp4 = f"{output_name}.mp4"
    final_mp3 = f"{output_name}.mp3"

    try:
        print(f"Downloading {m3u8_url} to {temp_mp4}...")
        ffmpeg_download_cmd = ["ffmpeg", "-i", m3u8_url, "-c", "copy", "-y", temp_mp4]
        subprocess.run(ffmpeg_download_cmd, check=True, stderr=subprocess.PIPE)

        print(f"Converting {temp_mp4} to {final_mp3}...")
        ffmpeg_convert_cmd = [
            "ffmpeg",
            "-i",
            temp_mp4,
            "-vn",
            "-acodec",
            "mp3",
            "-y",
            final_mp3,
        ]
        subprocess.run(ffmpeg_convert_cmd, check=True, stderr=subprocess.PIPE)

        if os.path.exists(temp_mp4):
            os.remove(temp_mp4)
            print(f"Cleaned up temporary file: {temp_mp4}")

        print(f"Success! Audio saved as {final_mp3}")

    except subprocess.CalledProcessError as e:
        print(f"Error during FFmpeg execution for {output_name}: {e.stderr.decode()}")
    except FileNotFoundError:
        print("FFmpeg not found. Please install FFmpeg and ensure it's in your PATH.")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred for {output_name}: {str(e)}")


def decode_brightcove_url(tracking_url):
    """
    Extract .m3u8 URL from a Brightcove tracking URL.

    Args:
        tracking_url (str): The Brightcove tracking URL.

    Returns:
        str: The .m3u8 URL or None if invalid.
    """
    try:
        parsed_url = urlparse(tracking_url)
        params = parse_qs(parsed_url.query)

        m3u8_url = params.get("media_url", [None])[0]
        if not m3u8_url:
            print(f"No 'media_url' found in: {tracking_url}")
            return None

        return m3u8_url

    except Exception as e:
        print(f"Failed to decode URL: {tracking_url}\nError: {str(e)}")
        return None


def sanitize_filename(name):
    """
    Sanitize a filename by replacing spaces with underscores and removing invalid characters.

    Args:
        name (str): The raw name.

    Returns:
        str: A sanitized filename.
    """
    sanitized = name.strip().replace(" ", "")
    # Remove invalid filesystem characters
    sanitized = "".join(c for c in sanitized if c not in '<>:"/\\|?*')
    return sanitized


def process_links_from_file(file_path):
    """
    Read Brightcove tracking URLs and names from a text file, process them with custom naming.

    Args:
        file_path (str): Path to the text file containing URLs and names.
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        exit(1)

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Split on the first space to separate URL and name
        parts = line.split(" ", 1)
        if len(parts) != 2:
            print(f"Line {i}: Skipping invalid line (expected URL and name): '{line}'")
            continue

        tracking_url, raw_name = parts
        m3u8_url = decode_brightcove_url(tracking_url)
        if not m3u8_url:
            print(f"Line {i}: Skipping line with invalid URL: '{tracking_url}'")
            continue

        # Sanitize the name and append "感謝祭Voice"
        sanitized_name = sanitize_filename(raw_name)
        output_name = f"{sanitized_name}感謝祭Voice"

        print(f"\nLine {i}: Processing: {output_name} from {m3u8_url}")
        convert_m3u8_to_mp3(m3u8_url, output_name)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python script.py <text_file>")
        print("Example: python script.py links.txt")
        print("File format: <Brightcove_tracking_url> <name> per line")
        sys.exit(1)

    text_file = sys.argv[1]
    process_links_from_file(text_file)
