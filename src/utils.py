"""Utils"""
import glob
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


def get_all_insta_usernames():
    """docstring for get_all_insta_usernames"""
    # Read the CSV file
    with open('instagram_metadata.csv', 'r') as file:
        reader = csv.DictReader(file)
        rows = [row for row in reader]
    insta_usernames_list = []
    for row in rows:
        insta_username = row['Username']
        insta_usernames_list.append(insta_username)
    return set(insta_usernames_list)


def get_credit_str():
    credit_str = ""
    for i in get_all_insta_usernames():
        credit_str += f"\t{settings.instagram_url}/{i}\n"
    return credit_str


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


def append_upload_entry(video_name, video_id):
    """
    Append an entry to the CSV file for a video upload.

    Args:
    - csv_file (str): Path to the CSV file.
    - video_name (str): Name or title of the video.
    - video_id (str): Unique identifier or URL of the video.
    """
    csv_file = settings.videos_data
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


def get_upload_count() -> int:
    """
    Get the total count of videos uploaded.

    Args:
    - csv_file (str): Path to the CSV file.

    Returns:
    - int: Total count of videos uploaded.
    """
    csv_file = settings.videos_data
    if not os.path.exists(csv_file):
        return 0

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        # Subtract 1 for the header row
        return sum(1 for row in reader) - 1


def get_latest_video() -> str:
    # Getting all .mp4 files in the directory
    video_files = glob.glob(os.path.join(
        settings.output_dir, "final_video_*.mp4"))

    # Extracting the datetime from the filename and sorting based on it
    latest_video = max(video_files, key=lambda x: datetime.strptime(
        x.split('_')[-1].replace('.mp4', ''), '%Y-%m-%d %H:%M:%S.%f'))

    return latest_video
