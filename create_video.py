import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from mutagen.mp3 import MP3
import textwrap


def transform_image(
        input_path: str,
        output_path: str,
        text: str = None,
        grayscale: bool = True,
        rotation: int = 0,
        resize: int = (800, 600),
        text_location: int = (0, -200),
        font_size: int = 20,
        font_path: str = "arial.ttf"
):
    
    if text is None:
        print("Please provide some text to overlay on the image")
        return
    
    output_path = '_'.join([output_path, 'text_image.jpg'])

    image = Image.open(input_path)

    if grayscale:
        image = image.convert("L")

    if rotation != 0:
        image = image.rotate(rotation)

    image = image.resize(resize)

    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(font_path, font_size)

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    x = ((image.width - text_width) // 2) + text_location[0]
    y = ((image.height - text_height) // 2) + text_location[1]

    outline_colour = 0
    fill_colour = 255
    
    for offset in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        draw.text((x + offset[0], y + offset[1]), text, font=font, fill=outline_colour)

    draw.text((x, y), text, font=font, fill=fill_colour)


    image.save(output_path)
    print(f"Image saved to {output_path}")

    return output_path


def generate_tts (text: str, tts_path: str, lang: str = "en"):
 
    tts_path = '_'.join([tts_path, 'tts.mp3'])

    tts = gTTS(text=text, lang=lang)
    tts.save(tts_path)
    print(f"TTS saved to {tts_path}")

    return tts_path



def create_video_from_image (
        image_path: str,
        video_output_path: str,
        duration: int = 10,
        fps: int = 30
):
    
    video_output_path = '_'.join([video_output_path, 'video.mp4'])
    
    cmd = [
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-i", image_path,
        "-t", str(duration),
        "-c:v", "libx264",
        "-r", str(fps),
        "-pix_fmt", "yuv420p",
        "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
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
    
    audio_merged_path = '_'.join([output_path, 'audio_merged.mp3'])
    output_path = '_'.join([output_path, 'audio_merged_video.mp4'])
    
    if not video_path or not background_music_path or not tts_path:
        print ("All file paths must be provided")
        return

    if os.path.exists(video_path) and os.path.exists(background_music_path) and os.path.exists(tts_path):
        audio_filter = "[0:a][1:a]amix=inputs=2:duration=shortest:dropout_transition=2"
        
        audio_cmd = [
            "ffmpeg",
            "-y",
            "-i", background_music_path,
            "-i", tts_path,
            "-filter_complex", audio_filter,
            "-c:a", "mp3",
            audio_merged_path
        ]

        subprocess.run(audio_cmd, check=True)
        print(f"Merged audio saved to {output_path}")

        video_cmd = [
            "ffmpeg",
            "-y",
            "-i", video_path,
            "-i", audio_merged_path,
            "-c:v", "copy",
            "-c:a", "copy",
            output_path
        ]

        subprocess.run(video_cmd, check=True)
        print(f"Final video saved to {output_path}")

        return output_path
    
    else:
        print ("Missing one or more files from the provided paths")
        return
    

def add_subtitles (input_path: str, output_path: str, captions: str):

    output_path = '_'.join([output_path, 'final_video.mp4'])

    wrapped_text = textwrap.fill(captions, width=60)

    drawtext_filter = (
        f"drawtext=fontsize=20:"
        f"fontcolor=white:"
        f"fontfile='arial.ttf':"
        f"text='{wrapped_text}':"
        f"x=(w-text_w)/2:"
        f"y=h-th-100:"
        f"shadowcolor=black:shadowx=2:shadowy=2:"
        f"box=1:boxcolor=black@0.5:boxborderw=5"
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

    input_image = 'image.jpg'
    text = "Placeholder text"
    captions = "Placeholder captions"
    background_music = "background_music.mp3"

    try:
        with open('text.txt', 'r', encoding='utf-8') as text_file, \
             open('captions.txt', 'r', encoding='utf-8') as caption_file:
            text = text_file.read()
            print("text: " + text)
            captions = caption_file.read()
            print("captions: " +captions)
    except FileNotFoundError:
        print("The specified file was not found.")



    output_path_name = './sample'

    image_path = transform_image(input_image, output_path_name, text)

    video_path =create_video_from_image(image_path, output_path_name)

    tts_path = generate_tts(captions, output_path_name)

    merged_audio_path = merge_audio(video_path=video_path, background_music_path=background_music, tts_path=tts_path, output_path=output_path_name)

    add_subtitles(input_path=merged_audio_path, output_path=output_path_name, captions=captions)


if __name__ == "__main__":
    main()