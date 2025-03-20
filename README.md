# Python Developer Test 2: FFmpeg and Pillow

## Objective
This script demonstrates how to:
1. Load an image using [Pillow](https://pillow.readthedocs.io/).  
2. Overlay text on the image and apply a basic transformation (grayscale, rotation, or resize).  
3. Convert the transformed image into a short video (at least 5 seconds) using [FFmpeg](https://ffmpeg.org/).  
4. Add background music and a voiceover narration.  
5. Embed captions into the final video.

## Requirements

### Image Processing
- **Pillow** is used to load the image.  
- Text is overlaid on the image.  
- A transformation is applied to the image (e.g., grayscale, rotation, and/or resize).

### Video Generation
- **FFmpeg** is used to create a short video (at least 5 seconds long).  
- Background music is added to the video.  
- Captions (subtitles) are applied to the final video.  
- A text-to-speech (TTS) engine generates a voiceover narration based on the provided captions.

### Additional Requirements
- The script can be easily customized (e.g., change text, font, background music file).  
- A README is provided (this document) describing installation and usage instructions.

---

## Installation

1. **Python 3.7+**  
   Make sure you have Python 3.7 or higher installed.  

2. **Pip Packages**  
   Install the following Python libraries (preferably in a virtual environment):
   ```bash
   pip install Pillow gTTS mutagen textwrap3

# FFmpeg and Pillow Video Processing Script

## FFmpeg Installation
Make sure FFmpeg is installed and available in your system’s `PATH`.

### On macOS (Homebrew)
```bash
brew install ffmpeg
```

### On Ubuntu/Debian
```bash
sudo apt-get update && sudo apt-get install ffmpeg
```

### On Windows
Download the FFmpeg binaries and ensure `ffmpeg.exe` is in your `PATH`.

## Fonts
The script uses `arial.ttf` by default. If you do not have `arial.ttf` available, either place it in the same directory or adjust the `font_path` parameter in the script to point to a valid TrueType font file.

## Usage

### Prepare Your Files
- **Input Image:** The default filename is `image.jpg`. Place this file in the same directory as `create_video.py`.
- **Text File:** Create a `text.txt` file containing the text you want to overlay on the image.
- **Captions File:** Create a `captions.txt` file containing the text you want spoken by the narrator and displayed as subtitles.
- **Background Music:** The default music file is `background_music.mp3`. Copy it to the same directory.

### Adjust Script Parameters (Optional)
In `create_video.py`, you can customize the following parameters if desired:

- `input_image` (default: `image.jpg`)
- `background_music` (default: `background_music.mp3`)
- Text transformation parameters (grayscale, rotation, resize, text location, font size, etc.)
- Video duration (`duration` in `create_video_from_image`)

### Run the Script
```bash
python create_video.py
```

## The Script Will:

1. Read the text from `text.txt` and overlay it on the image (`image.jpg`).
2. Apply transformations (grayscale, rotation, and resize) as specified.
3. Generate a short video using FFmpeg.
4. Generate the TTS narration from the `captions.txt` file.
5. Merge the background music and narration.
6. Add subtitles to the final video.

## Check the Output

You will see multiple files created, with suffixes like:

- `_text_image.jpg`
- `_video.mp4`
- `_tts.mp3`
- `_audio_merged.mp3`
- `_final_video.mp4`

The last file ending with `_final_video.mp4` is the complete video with background music, narration, and captions.

## Customization

### Image Transformations
Inside `transform_image()`, you can toggle grayscale, change rotation, or update the resize tuple.

### Text Overlay
Modify the `text`, `font_size`, `font_path`, and `text_location` in the function call to adjust how/where text appears on the image.

### Duration and FPS
In `create_video_from_image()`, you can change the duration (currently 10 seconds) and FPS (30).

### TTS Language
In `generate_tts()`, the default language is set to `"en"`. You can pass a different language code to `lang` if you want narration in another language (e.g., `"es"` for Spanish).

### Captions Appearance
In `add_subtitles()`, you can adjust the `drawtext` filter for font size, color, and positioning.

## Troubleshooting

### FFmpeg Not Found
Ensure FFmpeg is properly installed and added to your `PATH`. Run:

```bash
ffmpeg -version
```

to confirm.

### Font Errors
If you see errors loading `arial.ttf`, change the `font_path` argument to a path where a TrueType font is installed on your system.

### Missing Files
If `text.txt`, `captions.txt`, or `background_music.mp3` are missing, the script will either fail or use placeholder values.

## License
This project is provided *as is* for demonstration purposes. Feel free to modify and integrate it into your own projects.

---

