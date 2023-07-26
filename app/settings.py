import os
from datetime import datetime, timedelta

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    instagram_usernames: list[str] = ["daquan", "fuckjerry"]
    download_limits: int = 30
    base_dir: str = os.getcwd()
    temp_dir: str = "insta_downloads"
    duration_str: str = os.getenv("DURATION", "10days")
    duration: int = int(duration_str[:-4])  # Extract the numerical part from the string
    unit: str = duration_str[-4:]
    if unit == "days":
        start_date_dt: str = (datetime.now() - timedelta(days=duration)).strftime("%Y%m%d_%H%M%S")
    elif unit == "hour":
        start_date_dt: str = (datetime.now() - timedelta(hours=duration)).strftime("%Y%m%d_%H%M%S")
    else:
        raise ValueError("Invalid duration unit. Use 'days' or 'hours'.")
    end_date_dt: str = datetime.now().strftime("%Y%m%d_%H%M%S")

    start_date: datetime = datetime.strptime(start_date_dt, "%Y%m%d_%H%M%S")
    end_date: datetime = datetime.strptime(end_date_dt, "%Y%m%d_%H%M%S")


    
    class Config:
        env_prefix = "ENV_"


settings = Settings()