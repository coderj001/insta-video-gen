import os
from src.settings import settings
from moviepy.editor import (
    VideoFileClip,
    concatenate_videoclips,
    AudioFileClip,
    CompositeAudioClip
)
from moviepy.audio.fx.all import audio_loop


class VidoeCompilationMaker:
    def __init__(self):
        self.temp_dir = os.path.join(settings.base_dir, settings.temp_dir)
        self.output_dir = os.path.join(settings.base_dir, "merged_videos")

    def create_output_dir(self) -> None:
        """Create output directory if it's dosn't exists."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def get_videos_files(self) -> list[str]:
        """Get all video files from the temp directory."""
        video_files = [f for f in os.listdir(
            self.temp_dir) if f.endswith(".mp4")]
        video_files.sort(key=lambda x: os.path.getmtime(
            os.path.join(self.temp_dir, x)))
        return video_files

    def get_extra_files(self) -> list[str]:
        """Get all extra files."""
        extra_files = [f for f in os.listdir(
            self.temp_dir) if not f.endswith(".mp4")]
        extra_files.sort(key=lambda x: os.path.getmtime(
            os.path.join(self.temp_dir, x)))
        return extra_files

    def create_video_clip_and_duration(self):
        """docstring for create_video_clip"""
        video_files = self.get_videos_files()
        video_clips = []
        durations = []
        for video_file in video_files:
            clip = VideoFileClip(os.path.join(self.temp_dir, video_file))
            video_clips.append(clip)
            durations.append(clip.duration)
        return video_clips, durations

    def calculate_video_duration(self, durations):
        """
        Calculate the total duration and individual durations
        of the video clips.
        """
        total_duration = sum(durations)
        return total_duration, durations

    def display_final_video_duration(self):
        _, durations = self.create_video_clip_and_duration()
        total_duration, individual_durations = self.calculate_video_duration(
            durations)
        print("Total Duration:", total_duration, "seconds")
        print("Individual Durations:", individual_durations, "seconds each")

    def video_compilation(self):
        """Create a video compilation from the video files."""
        self.create_output_dir()
        video_clips, _ = self.create_video_clip_and_duration()

        target_width, target_height = settings.target_resolution

        # Resize and pad all video clips to fit within the target resolution
        resized_clips = []
        for clip in video_clips:
            aspect_ratio = clip.w / clip.h
            new_height = target_height
            new_width = int(new_height * aspect_ratio)
            resized_clip = clip.resize(height=new_height)
            padding = (target_width - new_width) // 2
            padded_clip = resized_clip.margin(
                left=padding, right=padding, color=(0, 0, 0))
            resized_clips.append(padded_clip)

        # Combine all resized and padded video clips
        combined_videos = concatenate_videoclips(resized_clips)

        # Add asset_one at the end
        asset_one = VideoFileClip('media_assets/like_share_and_subscribe.mp4')
        asset_one_resized = asset_one.resize(
            newsize=(target_width, target_height))
        final_video = concatenate_videoclips(
            [combined_videos, asset_one_resized])

        background_music_path = 'media_assets/fluffing_a_duck.mp3'
        background_music = AudioFileClip(background_music_path)

        looped_background_music = audio_loop(
            background_music, duration=final_video.duration)

        final_audio = CompositeAudioClip(
            [final_video.audio, looped_background_music])
        final_video = final_video.set_audio(final_audio)

        final_video_path = os.path.join(self.output_dir, 'final_video.mp4')
        final_video.write_videofile(
            final_video_path, codec='libx264', audio_codec='aac')

        background_music.close()
        final_video.close()
        asset_one.close()
        asset_one_resized.close()
        for clip in video_clips:
            clip.reader.close()
