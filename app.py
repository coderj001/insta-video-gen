import click
from src.instagram_downloader import download_instagram_videos_for_usernames
from src.video_compiler import VideoCompilationMaker
from src.yt_uploader import upload_to_youtube as upload_to_yt


@click.group()
def main():
    """
    Main command group. This is the entry point of this CLI app
    """
    pass


@main.command()
def fetch():
    """
    To Fetch Insta Videos
    """
    print("Fetching...")
    download_instagram_videos_for_usernames()


@main.command()
def compile():
    """
    compilation of insta videos
    """
    print("Compilating...")
    vc = VideoCompilationMaker()
    vc.create_compilation()


@main.command()
def upload():
    """
    upload to youtube
    """
    print("Uploading...")
    upload_to_yt()


if __name__ == '__main__':
    main()
