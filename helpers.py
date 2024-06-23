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
