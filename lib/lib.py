from datetime import datetime
import os
from PIL import Image

def get_search_filename(search_type, limit, category):
    filename = f"{search_type}_{limit}_{category}_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.json"
    return filename

def get_titles(search):
    titles = []
    for post_id, post in search.items():
        titles.append(post["name"])
    return titles

def get_ids(search):
    ids = []
    for post_id in search:
        ids.append(post_id)
    return ids

def get_images(search, image_dir):
    images = []
    for post_id in search:
        filename = os.path.join(image_dir, post_id + ".jpg")
        if os.path.exists(filename):
            # read image with PIL
            image = Image.open(filename)
            images.append(image)
    return images