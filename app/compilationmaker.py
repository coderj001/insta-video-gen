from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, CompositeAudioClip

import os
from app.settings import settings

def video_compilation() -> None:
    temp_dir = os.path.join(settings.base_dir, settings.temp_dir)
    output_dir = os.path.join(settings.base_dir, "merged_videos")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    video_files = [f for f in os.listdir(temp_dir) if f.endswith(".mp4")]

    video_files.sort(key=lambda x: os.path.getmtime(os.path.join(temp_dir, x)))

    video_clips = [VideoFileClip(os.path.join(temp_dir, video_file)) for video_file in video_files]
    combined_video = concatenate_videoclips(video_clips)

    like_and_share = VideoFileClip('assets/like_share_and_subscribe.mp4')

    total_duration = combined_video.duration
    middle_time = total_duration / 2

    # Add 'like_share_and_subscribe.mp4' in the middle of the video
    middle_position = (combined_video.w // 2 - like_and_share.w // 2, combined_video.h // 2 - like_and_share.h // 2)
    combined_video = CompositeVideoClip([combined_video, like_and_share.set_position(middle_position)],
                                        size=(combined_video.w, combined_video.h)).set_duration(total_duration)

    # Add 'like_share_and_subscribe.mp4' a few seconds before the end of the video
    end_time = total_duration - 5  # Add 5 seconds before the end
    end_position = (combined_video.w // 2 - like_and_share.w // 2, combined_video.h // 2 - like_and_share.h // 2)
    combined_video = CompositeVideoClip([combined_video.subclip(0, end_time),
                                         like_and_share.set_position(end_position).set_start(end_time)],
                                        size=(combined_video.w, combined_video.h)).set_duration(total_duration)

    audio_clips = [video.audio for video in video_clips]

    # Load the background music 'fluffing_a_duck.mp3'
    background_music = AudioFileClip('assets/fluffing_a_duck.mp3')

    # Combine the audio from each video clip with the background music
    final_audio = CompositeAudioClip([background_music] + audio_clips)

    # Set the audio of the final video
    final_video = combined_video.set_audio(final_audio)

    final_video_path = os.path.join(output_dir, 'final_video.mp4')
    final_video.write_videofile(final_video_path, codec='libx264', audio_codec='aac')

    combined_video.close()
    for video_clip in video_clips:
        video_clip.reader.close()
    like_and_share.close()
    background_music.close()
