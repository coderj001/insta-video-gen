import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from src.settings import settings

# OAuth 2.0 setup
CLIENT_SECRETS_FILE = settings.client_secrets_file
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
VALID_PRIVACY_STATUSES = (
    "public",
    "private",
    "unlisted",
)


def get_authenticated_service():
    credentials = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    # If there are no valid credentials, authenticate
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)

    return build("youtube", "v3", credentials=credentials)


def progress_callback(resumable_upload):
    if resumable_upload.progress() is not None:
        print("\rUploading... {0:.1f}%".format(
            resumable_upload.progress() * 100), end="")


def upload_video(youtube, video_path, title, description, tags):
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': settings.yt_category  # "People & Blogs" category
        },
        'status': {
            'privacyStatus': 'public'
        }
    }

    # Call the API to upload the video
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
                progress_callback(media_upload)

        print("\nUpload completed!")
        return response
