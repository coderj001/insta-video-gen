# from src.instagram_downloader import download_instagram_videos_for_usernames
# from src.video_compiler import VidoeCompilationMaker
#
# download_instagram_videos_for_usernames()
#
#
# vc = VidoeCompilationMaker()
# vc.create_compilation()

from src.utils import get_all_hashtags_in_str
from src.youtube_uploader import YouTubeUploader

ytupload = YouTubeUploader()
ytupload.login()
ytupload.upload_video(
    video_path='merged_videos/final_video_2023-08-12 18:50:26.847226.mp4',
    title="Test #1",
    description="",
    tags=get_all_hashtags_in_str()
)
ytupload.close()
