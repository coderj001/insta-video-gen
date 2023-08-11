""" Settings """
import os
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    your_insta_username: str = ""
    your_insta_password: str = ""
    instagram_usernames: list[str] = [
        "fuckjerry",
        "ladbible",
    ]  # added usernames in list
    base_dir: str = os.getcwd()
    temp_dir: str = "downloaded_videos"
    duration_str: str = os.getenv("DURATION", "2days")
    # Extract the numerical part from the string
    duration: int = int(duration_str[:-4])
    background_music: bool = True
    target_resolution: tuple[int, int] = (1920, 1080)

    # Extract the unit from the string ("hours", "days", "months", or "years")
    # to calculate the date range
    unit: str = duration_str[-4:]
    if unit == "hours":
        start_date_dt: datetime = datetime.now() - timedelta(hours=duration)
    elif unit == "days":
        start_date_dt: datetime = datetime.now() - timedelta(days=duration)
    elif unit == "months":
        start_date_dt: datetime = datetime.now() - relativedelta(months=duration)
    elif unit == "years":
        start_date_dt: datetime = datetime.now() - relativedelta(years=duration)
    else:
        raise ValueError(
            "Invalid duration unit. Use 'hours', 'days', 'months', or 'years'.")

    end_date_dt: datetime = datetime.now()

    # Declare start_date and end_date as class-level fields
    start_date: datetime = datetime.strptime(
        start_date_dt.strftime("%Y%m%d_%H%M%S"), "%Y%m%d_%H%M%S")
    end_date: datetime = datetime.strptime(
        end_date_dt.strftime("%Y%m%d_%H%M%S"), "%Y%m%d_%H%M%S")

    class Config:
        env_prefix = "ENV_"


settings = Settings()
