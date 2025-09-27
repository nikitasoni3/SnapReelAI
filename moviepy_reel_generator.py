import os
from moviepy import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip


def create_reel(folder: str):
    folder_path = os.path.join("user_uploads", folder)
    input_txt = os.path.join(folder_path, "input.txt")
    audio_path = os.path.join(folder_path, "audio.mp3")
    output_file = os.path.join(folder_path, "reel.mp4")

    clips = []
    with open(input_txt, "r") as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("file"):
            img_file = line.split("'")[1]
            img_path = os.path.join(folder_path, img_file)

            # Default duration
            duration = 3

            # Check if next line is duration
            if i + 1 < len(lines) and lines[i + 1].startswith("duration"):
                try:
                    duration = float(lines[i + 1].replace("duration", "").strip())
                except:
                    pass

            # ✅ Use new MoviePy API
            clip = (
                ImageClip(img_path)
                .with_duration(duration)
                .resized(height=1920)
                .with_position("center")
            )
            clips.append(clip)
        i += 1

    # Concatenate all image clips
    final_video = concatenate_videoclips(clips, method="compose")

    # Add audio
    if os.path.exists(audio_path):
        audio = AudioFileClip(audio_path)
        final_video = final_video.with_audio(audio)

    # Export video
    final_video.write_videofile(output_file, fps=30, codec="libx264", audio_codec="aac")
    print(f"Reel created: {output_file}")

    return output_file
