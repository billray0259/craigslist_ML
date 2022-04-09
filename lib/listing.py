from bs4 import BeautifulSoup
import json
import requests
import os
from tqdm import tqdm
from datetime import datetime
from PIL import Image
import io

class Listing:

    def __init__(self, post):
        self.post = post

        self.id = post["id"]
        self.repost_of = post["repost_of"]
        self.name = post["name"]
        self.url = post["url"]
        self.datetime = datetime.strptime(post["datetime"], "%Y-%m-%d %H:%M")
        self.last_updated = datetime.strptime(post["last_updated"], "%Y-%m-%d %H:%M")
        self.price = int(post["price"].replace(",", "")[1:])
        self.where = post["where"]
        self.has_image = post["has_image"]
        self.geotag = post["geotag"]
        self.deleted = post["deleted"]

        self.description = None
        self.image_url = None
        self.image = None
        

    def fetch_details(self):
        soup = BeautifulSoup(requests.get(self.url).text, 'xml')

        description = get_description(soup)
        self.description = description

        image_url = get_main_image_url(soup)
        self.image_url = image_url

        image_data = requests.get(image_url).content
        image = Image.open(io.BytesIO(image_data))
        self.image = image
    
    def to_dict(self):
        return {
            "id": self.id,
            "repost_of": self.repost_of,
            "name": self.name,
            "url": self.url,
            "datetime": self.datetime.strftime("%Y-%m-%d %H:%M"),
            "last_updated": self.last_updated.strftime("%Y-%m-%d %H:%M"),
            "price": self.price,
            "where": self.where,
            "has_image": self.has_image,
            "geotag": self.geotag,
            "deleted": self.deleted,
            "description": self.description,
            "image_url": self.image_url,
        }

    def save_image(self, image_dir):
        filename = os.path.join(image_dir, self.id + ".jpg")
        self.image.save(filename)

    def __str__(self):
        return f"{self.name} - {self.price} - {self.datetime}"


def get_soup(post):
    url = post['url']
    soup = BeautifulSoup(requests.get(url).text, 'xml')
    return soup

def get_thumbnail_urls(soup):
    # find the div with id="thumbs"
    thumbs = soup.find('div', id='thumbs')
    # find all the a tags with class="thumb"
    images = thumbs.find_all('a', class_='thumb')

    image_urls = list(map(lambda img: img["href"], images))
    return image_urls


def save_thumbnails(post, save_path):
    image_urls = get_thumbnail_urls(post)

    wrote_images = False
    # save the images to {images_dir}/{post_id}/{i}.jpg
    for i, url in enumerate(image_urls):
        filename = f"{i}.jpg"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            file_path = os.path.join(save_path, filename)
            with open(file_path, 'wb') as f:
                f.write(requests.get(url).content)
            wrote_images = True
    return wrote_images


def get_main_image_url(soup):
    # find the div with class="swipe"
    swipe = soup.find('div', class_='swipe')
    # find the img tag
    image = swipe.find('img')
    return image['src']


def save_main_image(image_url, save_path):
    # save the image to {images_dir}/{post_id}.jpg
    # filename = f"{post_id}.jpg"
    # file_path = os.path.join(save_dir, filename)
    wrote_image = False
    if not os.path.exists(save_path):
        with open(save_path, 'wb') as f:
            f.write(requests.get(image_url).content)
        wrote_image = True
    
    return wrote_image

def get_description(soup):
    # get section with id "postingbody"
    postingbody = soup.find('section', id='postingbody')
    # get the text
    description = postingbody.text
    return description