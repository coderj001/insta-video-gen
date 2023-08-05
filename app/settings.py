import os
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    instagram_usernames: list[str] = ["fuckjerry"]  # added usernames in list
    download_limits: int = 30
    base_dir: str = os.getcwd()
    temp_dir: str = "insta_downloads"
    duration_str: str = os.getenv("DURATION", "3days")
    duration: int = int(duration_str[:-4])  # Extract the numerical part from the string

    # Extract the unit from the string ("hours", "days", "months", or "years") to calculate the date range
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
        raise ValueError("Invalid duration unit. Use 'hours', 'days', 'months', or 'years'.")

    end_date_dt: datetime = datetime.now()

    # Declare start_date and end_date as class-level fields
    start_date: datetime = datetime.strptime(start_date_dt.strftime("%Y%m%d_%H%M%S"), "%Y%m%d_%H%M%S")
    end_date: datetime = datetime.strptime(end_date_dt.strftime("%Y%m%d_%H%M%S"), "%Y%m%d_%H%M%S")

    class Config:
        env_prefix = "ENV_"


settings = Settings()