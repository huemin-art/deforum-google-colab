import requests
from PIL import Image
from io import BytesIO
import os

def load_image(source):
    """
    Load an image from a local file path or HTTP link and return a PIL Image object.
    
    :param source: str, either a local file path or an HTTP/HTTPS URL
    :return: PIL.Image.Image object
    """
    try:
        if source.startswith(('http://', 'https://')):
            # Load image from URL
            response = requests.get(source)
            response.raise_for_status()  # Raise an exception for bad status codes
            image = Image.open(BytesIO(response.content))
        else:
            # Load image from local file
            if not os.path.exists(source):
                raise FileNotFoundError(f"The file {source} does not exist.")
            image = Image.open(source)
        
        return image
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image from URL: {e}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except IOError as e:
        print(f"Error opening the image: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return None

import subprocess
import tempfile
import os
from PIL import Image

def create_animation_from_pil_images(images, output_file, fps=30, loop=0, crf=17):
    """
    Create an animation from a list of PIL images using FFmpeg.

    :param images: List of PIL Image objects
    :param output_file: Path to the output animation file (e.g., 'output.gif' or 'output.mp4')
    :param fps: Frames per second (default: 30)
    :param loop: Number of times to loop the animation (0 means infinite loop, default: 0)
    :param crf: Constant Rate Factor for video quality (0-51, lower is better quality, default: 17)
    """
    # Create a temporary directory to store individual frames
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save each PIL image as a temporary file
        for i, img in enumerate(images):
            img.save(os.path.join(temp_dir, f"frame_{i:04d}.png"))

        # Determine the output format based on the file extension
        _, ext = os.path.splitext(output_file)
        if ext.lower() == '.gif':
            # FFmpeg command for GIF output
            cmd = [
                'ffmpeg',
                '-y',  # Overwrite output file if it exists
                '-framerate', str(fps),
                '-i', os.path.join(temp_dir, 'frame_%04d.png'),
                '-filter_complex', f'[0:v]split[a][b];[a]palettegen[p];[b][p]paletteuse',
                '-loop', str(loop),
                output_file
            ]
        else:
            # FFmpeg command for video output (e.g., MP4)
            cmd = [
                'ffmpeg',
                '-y',  # Overwrite output file if it exists
                '-framerate', str(fps),
                '-i', os.path.join(temp_dir, 'frame_%04d.png'),
                '-c:v', 'libx264',
                '-preset', 'slow',  # Use 'slow' preset for better compression
                '-crf', str(crf),
                '-pix_fmt', 'yuv420p',
                output_file
            ]

        # Run FFmpeg command
        subprocess.run(cmd, check=True)

    print(f"Animation saved as {output_file}")
