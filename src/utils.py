"""Utils"""
from datetime import datetime
import csv
import os
import platform
import zipfile
from collections import Counter

import requests

from src.settings import settings


def get_all_tags() -> list[str]:
    # Read the CSV file
    with open('instagram_metadata.csv', 'r') as file:
        reader = csv.DictReader(file)
        rows = [row for row in reader]

    # Sort the rows based on Likes and Comments
    # (convert to integers for proper sorting)
    sorted_rows = sorted(rows, key=lambda x: (
        int(x['Likes']), int(x['Comments'])), reverse=True)

    # Extract hashtags from the sorted rows
    all_hashtags = []
    for row in sorted_rows:
        hashtags = row['Hashtags'].split()
        all_hashtags.extend(hashtags)

    # Get the 20 most common hashtags
    top_tags = [tag for tag, _ in Counter(
        all_hashtags).most_common(settings.limit_hashtags)]

    return settings.imp_hashtags + top_tags


def get_all_hashtags_in_str() -> str:
    return ','.join(get_all_tags())


def download_chromedriver(version=None) -> None:
    base_url = "https://chromedriver.storage.googleapis.com/"

    # Get the latest version if not specified
    if version is None:
        response = requests.get(base_url + "LATEST_RELEASE")
        version = response.text.strip()

    # Determine the correct file for the current OS
    system = platform.system().lower()
    if system == "windows":
        file_name = "chromedriver_win32.zip"
    elif system == "linux":
        file_name = "chromedriver_linux64.zip"
    elif system == "darwin":
        file_name = "chromedriver_mac64.zip"
    else:
        raise Exception("Unknown operating system")

    # Download the file
    url = base_url + version + "/" + file_name
    response = requests.get(url)
    zip_path = "chromedriver.zip"
    with open(zip_path, 'wb') as file:
        file.write(response.content)

    # Extract the file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall()

    # Remove the downloaded zip file
    os.remove(zip_path)

    # Move the chromedriver to a known location (optional)
    if system == "windows":
        os.rename("chromedriver.exe", f"{settings.base_dir}/chromedriver")
    else:
        os.rename("chromedriver", f"{settings.base_dir}/chromedriver")

    print("ChromeDriver downloaded successfully!")


def video_management_for_merged_videos_dir():
    """ Management Of Mergerd Videos Content """
    pass


def append_upload_entry(csv_file, video_name, video_id):
    """
    Append an entry to the CSV file for a video upload.

    Args:
    - csv_file (str): Path to the CSV file.
    - video_name (str): Name or title of the video.
    - video_id (str): Unique identifier or URL of the video.
    """
    # Check if CSV file exists. If not, create one with headers.
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Video Name", "Video ID", "Upload Date"])

    # Append the new entry to the CSV file.
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            video_name,
            video_id,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        ])


def get_upload_count(csv_file) -> int:
    """
    Get the total count of videos uploaded.

    Args:
    - csv_file (str): Path to the CSV file.

    Returns:
    - int: Total count of videos uploaded.
    """
    if not os.path.exists(csv_file):
        return 0

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        # Subtract 1 for the header row
        return sum(1 for row in reader) - 1
