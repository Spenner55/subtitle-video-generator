import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS

def transform_image(
        input_path: str,
        output_path: str,
        text: str = None,
        grayscale: bool = True,
        rotation: int = 0,
        resize: int = (800, 600)
):
    
    if text is None:
        print("Please provide some text to overlay on the image")
        return

    image = Image.open(input_path)

    if grayscale:
        image = image.convert("L")

    if rotation != 0:
        image = image.rotate(rotation)

    if resize != (800, 600):
        image = image.resize(resize)

    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    text_width, text_height = draw.textsize(text, font=font)

    x = (image.width - text_width) // 2
    y = (image.height - text_height) // 2

    outline_color = (0, 0, 0)

    for offset in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        draw.text((x + offset[0], y + offset[1]), text, font=font, fill=outline_color)

    draw.text((x - y), text, font=font, fill = "white")


    image.save(output_path)
    print(f"Image saved to {output_path}")

    return output_path


def generate_tts (text: str, tts_path: str, lang: str = "en"):
    tts = gTTS(text=text, lang=lang)
    tts.save(tts_path)
    print(f"TTS saved to {tts_path}")

    return tts_path


def create_video_from_image (
        image_path: str,
        video_output_path: str,
        duration: int = 5,
        fps: int = 30
):
    cmd = [
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-i", image_path,
        "-t", str(duration),
        "-c:v", "libx264",
        "-r", str(fps),
        "-pix_fmt", "yuv420p",
        video_output_path
    ]

    subprocess.run(cmd, check=True)
    print(f"Video saved to {video_output_path}")

    return video_output_path


def merge_audio (
    video_path: str, 
    background_music_path: str, 
    tts_path: str, 
    output_path: str
):
    if not video_path or not background_music_path or not tts_path:
        print ("All file paths must be provided")
        return

    if os.path.exists(video_path) and os.path.exists(background_music_path) and os.path.exists(tts_path):
        audio_filter = "[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=2"
        
        cmd = [
            "ffmpeg",
            "-y",
            "-i", video_path,
            "-i", background_music_path,
            "-i", tts_path,
            "-filter_complex", audio_filter,
            "-c:v", "copy",
            "-c:a", "aac",
            output_path

        ]

        subprocess.run(cmd, check=True)
        print(f"Merged audio saved to {output_path}")

        return output_path
    
    else:
        print ("Missing one or more files from the provided paths")
        return
    

def add_subtitles (input_path: str, output_path: str, text_path: str):

    drawtext_filter = (
        f"drawtext=fontsize=40:fontcolor=white:"
        f"fontfile='arial.ttf':"
        f"text='{text_path}"
        f"x=(w-text_w)/2:y=h-th-50:shadowcolor=black:shadowx=2:shadowy=2"
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-vf", drawtext_filter,
        "-c:a", "copy",
        output_path
    ]

    subprocess.run(cmd, check=True)
    print(f"Subtitles added to {output_path}")

    return output_path


def main():
    input_image = 'test.jpg'
    text = "this is test text to experiment with the functionality of this script"
    background_music = "background_music.mp3"

    