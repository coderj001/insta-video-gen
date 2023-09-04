import click
from src.instagram_downloader import download_instagram_videos_for_usernames
from src.video_compiler import VideoCompilationMaker
from src.yt_uploader import publish_video_to_youtube


@click.group()
def cli():
    """
    Main command group. This is the entry point of this CLI app
    """
    pass


@cli.command(name='download-videos')
def download_instagram_videos():
    """
    Download Instagram videos within a specified date range
    """
    print("Downloading Instagram videos...")
    download_instagram_videos_for_usernames()


@cli.command(name='create-compilation')
def compile_videos():
    """
    Compile downloaded Instagram videos into one video
    """
    print("Creating video compilation...")
    video_compiler = VideoCompilationMaker()
    video_compiler.create_compilation()


@cli.command(name='publish-to-youtube')
def upload_video():
    """
    Upload the compiled video to YouTube
    """
    print("Uploading to YouTube...")
    publish_video_to_youtube()


@cli.command(name='show-videos')
def list_videos():
    """
    List all the downloaded Instagram videos
    """
    video_compiler = VideoCompilationMaker()
    video_files = video_compiler.get_videos_files()
    for video in video_files:
        print(video)


if __name__ == '__main__':
    cli()
