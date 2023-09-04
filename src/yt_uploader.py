import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from src.settings import settings
from src.utils import (
    get_all_hashtags_in_str,
    get_yt_tags,
    get_credit_str,
    get_latest_video,
    get_upload_count,
)

# OAuth 2.0 setup
CLIENT_SECRETS_FILE = settings.client_secrets_file
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
VALID_PRIVACY_STATUSES = ("public", "private", "unlisted",)


def authenticate_with_youtube():
    """
    Authenticates the user using OAuth2.0 and returns an authenticated YouTube service object.
    """  # noqa: E501
    credentials = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    # If there are no valid credentials available, prompt the user to log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)

        # Save the credentials for future runs
        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)

    return build("youtube", "v3", credentials=credentials)


def upload_progress_callback(resumable_upload):
    """
    Callback function to display upload progress.
    """
    if resumable_upload.progress() is not None:
        print("\rUploading... {0:.1f}%".format(
            resumable_upload.progress() * 100), end="")


def initiate_video_upload(youtube, video_path, title, description, tags):
    """
    Uploads the video to YouTube.
    """
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': settings.yt_category
        },
        'status': {
            'privacyStatus': 'public'
        }
    }

    with open(video_path, "rb") as _:
        media_upload = MediaFileUpload(
            video_path,
            chunksize=-1,
            resumable=True
        )
        request = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=media_upload
        )
        response = None
        while response is None:
            status, response = request.next_chunk(num_retries=3)
            if status:
                upload_progress_callback(media_upload)

        print("\nUpload completed!")
        return response


def publish_video_to_youtube():
    """
    Prepares the video details and initiates the YouTube upload process.
    """
    youtube = authenticate_with_youtube()
    video_path = get_latest_video()
    video_count = get_upload_count() + 1
    if settings.yt_video_sub_title:
        title = f"{settings.yt_video_title} | {settings.yt_video_sub_title} | Challenge No. {video_count}"  # noqa: E501
    else:
        title = f"{settings.yt_video_title} | Challenge No. {video_count}"
    credit_str = get_credit_str()
    description = settings.yt_video_description.format(
        video_count,
        settings.your_youtube_username,
        credit_str,
        settings.your_youtube_username,
        get_all_hashtags_in_str()
    )
    tags = get_yt_tags()

    initiate_video_upload(youtube, video_path, title, description, tags)
