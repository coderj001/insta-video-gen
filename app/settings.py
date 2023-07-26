from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    insta_usernames = [
        "daquan",
        "fuckjerry",
    ]

    download_limits: int = 10

