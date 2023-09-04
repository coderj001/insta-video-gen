""" Instagram Downloader """
import csv
import os
import re
import shutil
from itertools import dropwhile, takewhile

import instaloader

from .settings import settings

L = instaloader.Instaloader(download_video_thumbnails=False)

# Load existing session or create a new session
# session_file = f"{settings.your_insta_username}.session"
# if os.path.exists(session_file):
#     L.load_session_from_file(settings.your_insta_username)
# else:
#     # Login before saving session
#     L.context.login(settings.your_insta_username,
#                     settings.your_insta_password)
#     L.save_session_to_file(settings.your_insta_username)


def download_instagram_videos_in_date_range(username: str) -> None:
    profile = instaloader.Profile.from_username(L.context, username)
    posts = profile.get_posts()
    results = takewhile(lambda p: p.date > (settings.start_date), dropwhile(
        lambda p: p.date > (settings.end_date), posts))

    with open('instagram_metadata.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(
                [
                    "Username",
                    "Post ID",
                    "Date",
                    "Likes",
                    "Comments",
                    "Hashtags",
                    "Caption Hashtags",
                    "Caption",   # Add this line
                ]

            )

        for post in results:
            print(f"Downloading: {post.date}")
            if post.is_video:
                L.download_post(
                    post, target=settings.temp_dir.split('/').pop())
                # Extract hashtags from caption
                hashtags = " ".join(re.findall(r"#(\w+)", post.caption))

                writer.writerow([
                    username,
                    post.shortcode,
                    post.date,
                    post.likes,
                    post.comments,
                    hashtags,
                    post.caption_hashtags,
                    post.caption if post.caption else "N/A"  # Add this line
                ])
                original_file_path = os.path.join(
                    settings.temp_dir,
                    f'{post.date_utc}_UTC.mp4'
                )
                new_file_name = f"{username}_{post.shortcode}_{post.date_utc.strftime('%Y%m%d_%H%M%S')}.mp4"  # noqa: E501
                new_file_path = os.path.join(settings.temp_dir, new_file_name)
                original_file_path = original_file_path.replace(
                    ' ', '_').replace(':', '-')
                if os.path.exists(original_file_path):
                    shutil.move(original_file_path, new_file_path)


def download_instagram_videos_for_usernames() -> None:
    for username in settings.instagram_usernames:
        print(f"Username: {username}")
        download_instagram_videos_in_date_range(username=username)
