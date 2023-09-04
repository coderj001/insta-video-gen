""" Settings """
import os
from datetime import datetime, timedelta
from typing import Optional

from dateutil.relativedelta import relativedelta
from pydantic import validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuration and settings for the application.

    Attributes:
    - base_dir: Directory where the application is running.
    - temp_dir: Directory for storing temporary files, such as downloaded videos.
    - your_insta_username: Instagram username for authentication.
    - your_insta_password: Instagram password for authentication.
    - instagram_usernames: List of Instagram usernames whose videos are to be downloaded.
    - start_date: Starting date for downloading Instagram videos.
    - end_date: Ending date for downloading Instagram videos.
    - background_music: Flag indicating whether to add background music to the compiled video.
    - background_music_path: Path to background_music_file.
    - outro_video_path: Path to outro video.
    - target_resolution: Target resolution for the compiled video.
    - your_youtube_username: YouTube username for authentication.
    - your_youtube_password: YouTube password for authentication.
    - limit_hashtags: Maximum number of hashtags to be used while uploading to YouTube.
    - imp_hashtags: List of important hashtags to be included while uploading to YouTube.

    Usage:
    To access any setting, simply use: settings.<attribute_name>.
    For example, to get the base directory, use settings.base_dir.
    """  # noqa: E501

    base_dir: str = os.getcwd()
    temp_dir: str = os.path.join(base_dir,  "downloaded_videos")
    output_dir: str = os.path.join(base_dir,  "merged_videos")
    instagram_url: str = "https://www.instagram.com"
    #####################
    # Instagram related #
    #####################
    your_insta_username: Optional[str] = None
    your_insta_password: Optional[str] = None
    instagram_usernames: list[str]  # added usernames in list

    @validator("instagram_usernames", each_item=True)
    def check_instagram_usernames(cls, username):
        if not username:
            raise ValueError("Instagram usernames must not be empty.")
        return username
    duration_str: str = "1days"
    # Extract the numerical part from the string
    duration: int = int(duration_str[:-4])

    # Extract the unit from the string ("hours", "days", "months", or "years")
    # to calculate the date range
    unit: str = duration_str[-4:]
    if unit == "hours":
        start_date_dt: datetime = datetime.now() - timedelta(hours=duration)
    elif unit == "days":
        start_date_dt: datetime = datetime.now() - timedelta(days=duration)
    elif unit == "months":
        start_date_dt: datetime = datetime.now() - relativedelta(
            months=duration
        )
    elif unit == "years":
        start_date_dt: datetime = datetime.now() - relativedelta(
            years=duration
        )
    else:
        raise ValueError(
            "Invalid duration unit. Use 'hours', 'days', 'months', or 'years'."
        )

    end_date_dt: datetime = datetime.now()

    # Declare start_date and end_date as class-level fields
    start_date: datetime = datetime.strptime(
        start_date_dt.strftime("%Y%m%d_%H%M%S"), "%Y%m%d_%H%M%S")
    end_date: datetime = datetime.strptime(
        end_date_dt.strftime("%Y%m%d_%H%M%S"), "%Y%m%d_%H%M%S")

    #############################
    # Video Compilation Related #
    #############################
    background_music: bool = False
    background_music_path: str = os.path.join(
        base_dir,
        'media_assets/fluffing_a_duck.mp3'
    )
    target_resolution: tuple[int, int] = (1930, 1080)
    outro_video_path: str = os.path.join(
        base_dir,
        'media_assets/like_share_and_subscribe.mp4'
    )
    videos_data: str = os.path.join(base_dir, 'videos.csv')

    ##########################
    # Youtube Upload Related #
    ##########################
    yt_category: int = 32
    your_youtube_username: Optional[str] = None
    your_youtube_password: Optional[str] = None
    client_secrets_file: str = os.path.join(base_dir, 'client_secrets.json')
    limit_hashtags: int = 5
    imp_hashtags: list[str] = [
        "videoedit",
        "funney",
        "compilation",
        "compilationedit",
        "best memes compilation",
        "memes",
        "bruh sound",
        "effect meme",
        "fluffing_a_duck"
    ]
    yt_video_title: str = "TRY NOT TO LAUGH 😆"
    yt_video_sub_title: Optional[str] = None
    yt_video_description: str = (
        "If you accepted this challange\n"
        "Thanks for watching this video. I hope you liked it.\n"
        "Don't forget to subscribe!\n\n"
        "meme compilation v{}"  # Placeholder for meme compilation version
        "\n\n"
        "For business and queries contact {}"  # Placeholder for contact details # noqa: E501
        "\n\n"
        "𝘾𝙍𝙀𝘿𝙄𝙏𝙎\n"
        "=====================================================\n\n"
        "𝙁𝙤𝙡𝙡𝙤𝙬 𝙩𝙝𝙚𝙨𝙚 𝙖𝙬𝙚𝙨𝙤𝙢𝙚 𝙘𝙧𝙚𝙖𝙩𝙤𝙧𝙨\n"
        "{}"  # Placeholder for creators
        "\n\n"
        "---------------------------------------------------------------------------------------------------------------\n"  # noqa: E501

        "All clips are used for entertainment purposes only! If there are any problems with the videos or songs featured send me an email at: {} and we'll resolve the issue!\n"  # email  # noqa: E501
        "-----------------------------------------------------------------------------------------------------------------\n\n"  # noqa: E501

        "{}"  # Placeholder for any additional information
    )

    class Config:
        env_prefix = "env_"


settings = Settings(_env_file='.env')
