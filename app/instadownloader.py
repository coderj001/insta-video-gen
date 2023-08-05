""" Instagram Downloader """
from datetime import datetime
from itertools import dropwhile, takewhile

import instaloader

from .settings import settings

L = instaloader.Instaloader(download_pictures=False, download_video_thumbnails=False, user_agent="Instagram 146.0.0.27.125 (iPhone12,1; iOS 13_3; en_US; en-US;scale=2.00; 1656x3584; 190542906)")

def download_instagram_videos_in_date_range(username: str)->None:
    posts = instaloader.Profile.from_username(L.context, username).get_posts()
    results = takewhile(lambda p: p.date > (settings.start_date), dropwhile(lambda p:p.date > (settings.end_date), posts))
    
    for post in results:
        print(post.date)
        if post.is_video:
            L.download_post(post, target=settings.temp_dir)
            

def download_instagram_videos_for_usernames()->None:
    for username in settings.instagram_usernames:
        print("Username: ", username)
        download_instagram_videos_in_date_range(username=username)