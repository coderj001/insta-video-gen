# from src.instagram_downloader import download_instagram_videos_for_usernames
# from src.video_compiler import VideoCompilationMaker

# download_instagram_videos_for_usernames()


# vc = VideoCompilationMaker()
# vc.create_compilation()

# from src.utils import get_all_hashtags_in_str
# from src.youtube_uploader import YouTubeUploader
#
# ytupload = YouTubeUploader()
# ytupload.login()
# ytupload.upload_video(
#     video_path='merged_videos/final_video_2023-08-12 18:50:26.847226.mp4',
#     title="Test #1",
#     description="",
#     tags=get_all_hashtags_in_str()
# )

# import os
# from src.yt_uploader import get_authenticated_service, upload_video
# from src.settings import settings
#
# youtube = get_authenticated_service()
# video_path = os.path.join(settings.base_dir, 'l.mp4')
# title = input("Enter the video title: ")
# description = input("Enter the video description: ")
# tags = input("Enter the video tags (comma-separated): ")
# upload_video(youtube, video_path, title, description, tags)

# from src.settings import settings
#
# __import__('pprint').pprint(settings.model_dump_json())

from src.utils import get_upload_count, append_upload_entry, get_all_insta_usernames, get_credit_str
# print(append_upload_entry(
# 'Hi!', './merged_videos/final_video_2023-08-29 22:08:28.176477.mp4'))
# print(get_upload_count())

print(get_credit_str())
