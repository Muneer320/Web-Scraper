import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import imghdr
import time
import hashlib


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def download_image(url, directory, image_number):
    try:
        filename = os.path.join(directory, f"{image_number}.jpg")
        with open(filename, 'wb') as file:
            response = requests.get(url)
            response.raise_for_status()
            file.write(response.content)
        print(f"Downloaded: {filename}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to download: {url} ({e})")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

#Input from the user
url = input("Enter the base URL: ")

if not url.endswith("/"):
    url += "/"


start_page = int(input("Enter the starting page number: "))
end_page = int(input("Enter the ending page number: "))

max_skip_count = 45

downloaded_images_directory = "downloaded_images"
create_directory(downloaded_images_directory)

start_time = time.time()
image_number = 1
image_urls = []

for page_number in range(start_page, end_page + 1):
    page_url = f"{url}page-{page_number}"
    response = requests.get(page_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img', class_='bbImage')
        for img_tag in img_tags:
            img_url = img_tag.get('src')
            if img_url:
                img_url = urljoin(page_url, img_url)
                image_urls.append((img_url, downloaded_images_directory, image_number))
                image_number += 1

    else:
        print(f"Failed to retrieve the web page: {page_url}")

# Download the images
for img_url, directory, img_num in image_urls:
    download_image(img_url, directory, img_num)

# Remove duplicate images after downloading all images
def file_hash(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as file:
        while True:
            data = file.read(65536)  # Read in 64k chunks
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()


# Remove duplicate files in a directory
def remove_duplicate_files(directory):
    seen = set()
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            filehash = file_hash(filepath)
            if filehash in seen:
                print(f"Removing duplicate: {filepath}")
                os.remove(filepath)
            else:
                seen.add(filehash)


remove_duplicate_files(downloaded_images_directory)

end_time = time.time()
total_time = end_time - start_time
print(f"Total time taken: {total_time:.2f} seconds")
DIR = "/content/downloaded_images"
print(f"Number of images available: {len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])}")
