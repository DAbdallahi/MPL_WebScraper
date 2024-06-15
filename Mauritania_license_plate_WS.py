import requests
from bs4 import BeautifulSoup
import os

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')

def download_image(img_url, img_name, directory, headers):
    img_response = requests.get(img_url, headers=headers, stream=True)
    img_path = os.path.join(directory, img_name)
    with open(img_path, 'wb') as file:
        file.write(img_response.content)
    print(f"Image saved as '{img_path}'")

def get_full_image_url(image_div):
    return image_div.find('a')['href']

def get_image_urls_from_tags(img_tags, base_url=None):
    img_urls = []
    for img in img_tags:
        img_url = img['src']
        if base_url and not img_url.startswith('http'):
            img_url = base_url.rsplit('/', 1)[0] + '/' + img_url
        img_urls.append(img_url)
    return img_urls

def scrape_and_save_images(url, img_tag_selector, img_name_prefix, directory, headers, base_url=None, limit=None):
    soup = get_soup(url)
    img_tags = soup.select(img_tag_selector)
    if limit:
        img_tags = img_tags[:limit]
    img_urls = get_image_urls_from_tags(img_tags, base_url)
    
    for i, img_url in enumerate(img_urls):
        img_name = f"{img_name_prefix}_{i + 1}.jpg"
        download_image(img_url, img_name, directory, headers)

# Directory for saving images
directory = "scr_images"
create_directory(directory)

# Headers for requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# URLs and configurations
scrape_configs = [
    {
        "url": "https://commons.wikimedia.org/wiki/File:Mauritanian_license_plate.jpg",
        "img_tag_selector": "div.fullImageLink a",
        "img_name_prefix": "web1_img1",
        "custom_processing": lambda soup: get_full_image_url(soup.find('div', class_='fullImageLink'))
    },
    {
        "url": "https://www.plateshack.com/y2k/Mauritania/mauritaniay2k.htm",
        "img_tag_selector": "img",
        "img_name_prefix": "web1_img2",
        "base_url": "https://www.plateshack.com/y2k/Mauritania/mauritaniay2k.htm"
    },
    {
        "url": "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=License++plates+of+MAURITANIA+&_sacat=0&_odkw=MAURITANIA+License++plates&_osacat=0",
        "img_tag_selector": "div.s-item__image img",
        "img_name_prefix": "web1_img3",
        "limit": 5
    },
    {
        "url": "https://commons.wikimedia.org/wiki/Category:License_plates_of_Mauritania",
        "img_tag_selector": "li.gallerybox img",
        "img_name_prefix": "web1_img4"
    },
    {
        "url": "http://www.worldlicenseplates.com/world/AF_MAUR.html",
        "img_tag_selector": "img[alt='Mauritanian License Plates']",
        "img_name_prefix": "web1_img5",
        "base_url": "http://www.worldlicenseplates.com/"
    }
]

# Scrape and save images based on configurations
for config in scrape_configs:
    if "custom_processing" in config:
        soup = get_soup(config["url"])
        img_url = config["custom_processing"](soup)
        download_image(img_url, config["img_name_prefix"], directory, headers)
    else:
        scrape_and_save_images(config["url"], config["img_tag_selector"], config["img_name_prefix"], directory, headers, config.get("base_url"), config.get("limit"))

print("All images have been scraped and saved.")
