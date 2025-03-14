# Audio Downloader m3u8

A tool specifically designed to download and convert Brightcove audio files to MP3 format.

## Description

This tool helps you download audio content from Brightcove media streams. It converts m3u8 streams to MP3 audio files, particularly optimized for downloadin content.

## Prerequisites

- Modern web browser with Developer Tools (Chrome, Firefox, etc.)
- FFmpeg installed and available in your PATH
- Python 3.6 or higher

## Usage

### Step 1: Find the Audio Links

1. Visit the Sakurazaka46 website or other Brightcove-based audio source
2. Open the browser Developer Tools by pressing `F12` or right-clicking and selecting "Inspect"
3. Navigate to the "Network" tab in the Developer Tools
4. Play the audio you want to download
5. In the Network tab, filter for "tracking" or look for Brightcove tracking URLs
6. Right-click on the appropriate request and select "Copy link address" or "Copy URL"

### Step 2: Prepare the Download List

1. Create a text file in this directory (e.g., `links.txt`)
2. For each audio file, add a line with the format: `<Brightcove_tracking_url> <member_name>`
   Example:
   ```
   https://example.brightcove.com/tracking?media_url=https://example.com/file.m3u8 MemberName
   https://example.brightcove.com/tracking?media_url=https://example.com/file2.m3u8 AnotherName
   ```

### Step 3: Download the Audio

1. Run the download script:
   ```
   python m3u8.py links.txt
   ```
2. The script will:
   - Extract the m3u8 URL from each Brightcove tracking link
   - Download and convert each audio file to MP3 format
   - Name each file with the member name and "感謝祭Voice" suffix
   - Save all files to the current directory

## Output

Files will be saved in the format: `<MemberName>感謝祭Voice.mp3`

