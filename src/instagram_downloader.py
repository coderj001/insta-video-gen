""" Instagram Downloader """
from datetime import datetime
from itertools import dropwhile, takewhile
import os
import csv
import shutil

import instaloader

from .settings import settings

L = instaloader.Instaloader(download_video_thumbnails=False)


def download_instagram_videos_in_date_range(username: str)->None:
    profile = instaloader.Profile.from_username(L.context, username)
    posts = profile.get_posts()
    results = takewhile(lambda p: p.date > (settings.start_date), dropwhile(lambda p:p.date > (settings.end_date), posts))
    
    with open('instagram_metadata.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["Username", "Post ID", "Date", "Likes", "Comments"])

        for post in results:
            print(post.date)
            if post.is_video:
                L.download_post(post, target=settings.temp_dir)
                writer.writerow([username, post.shortcode, post.date, post.likes, post.comments])
                original_file_path = os.path.join(settings.temp_dir, f'{post.date_utc}_UTC.mp4')
                new_file_path = os.path.join(settings.temp_dir, f'{post.shortcode}.mp4')
                if os.path.exists(original_file_path):
                    shutil.move(original_file_path, new_file_path)


def download_instagram_videos_for_usernames()->None:
    for username in settings.instagram_usernames:
        print("Username: ", username)
        download_instagram_videos_in_date_range(username=username)