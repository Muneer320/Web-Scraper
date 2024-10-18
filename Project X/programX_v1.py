import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import imghdr  # Library to determine image file types
import time  # Import the time module
import hashlib  # Library to calculate file hashes

# Function to create a directory if it doesn't exist


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to download an image from a URL


def download_image(url, directory, image_number):
    try:
        # Check if the URL ends with ".jpg", ".jpeg", ".png", or ".gif"
        supported_extensions = [".jpg", ".jpeg", ".png", ".gif"]
        if any(url.lower().endswith(extension) for extension in supported_extensions):
            # Extract the filename from the URL
            filename = os.path.join(directory, f"{image_number}.jpg")
            with open(filename, 'wb') as file:
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404)
                file.write(response.content)
            print(f"Downloaded: {filename}")
            return True
        else:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404)

            # Determine the image file type
            image_type = imghdr.what(None, response.content)
            if image_type in ["jpeg", "jpg", "png", "gif"]:
                # Extract the filename from the URL
                filename = os.path.join(directory, f"{image_number}.jpg")
                with open(filename, 'wb') as file:
                    file.write(response.content)
                print(f"Downloaded: {filename}")
                return True
            else:
                print(f"Skipped: {url} (Not a supported image file)")
                return False
    except requests.exceptions.RequestException as e:
        print(f"Failed to download: {url} ({e})")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


# Input from the user
url = input("Enter the base URL: ")
if not url.endswith("/"):
    url += "/"  # Ensure the URL ends with a trailing slash
start_page = int(input("Enter the starting page number: "))
end_page = int(input("Enter the ending page number: "))
max_skip_count = 45  # Maximum number of skip/failure attempts allowed

# Create a directory to save the downloaded images
downloaded_images_directory = "downloaded_images"
create_directory(downloaded_images_directory)

# Start the timer
start_time = time.time()

# Initialize a counter for image numbering
image_number = 1

# Create a list to store image URLs
image_urls = []

# Iterate through the specified pages
for page_number in range(start_page, end_page + 1):
    page_url = f"{url}page-{page_number}"

    # Send an HTTP GET request to the page
    response = requests.get(page_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all image tags (img)
        img_tags = soup.find_all('img')

        # Find all links (a) that might contain images and extract image URLs
        a_tags = soup.find_all('a', href=True)
        for a_tag in a_tags:
            # Look for img tags within the <a> tag
            img_in_a = a_tag.find_all('img')
            for img_tag in img_in_a:
                img_url = img_tag.get('src')
                if img_url:
                    img_url = urljoin(page_url, img_url)
                    image_urls.append(
                        (img_url, downloaded_images_directory, image_number))
                    image_number += 1

    else:
        print(f"Failed to retrieve the web page: {page_url}")

# Download the images
for img_url, directory, img_num in image_urls:
    download_image(img_url, directory, img_num)

# Remove duplicate images after downloading all images


def file_hash(filepath):
    # Calculate and return the hash of a file
    hasher = hashlib.md5()
    with open(filepath, 'rb') as file:
        while True:
            data = file.read(65536)  # Read in 64k chunks
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()


def remove_duplicate_files(directory):
    # Remove duplicate files in a directory
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

# Stop the timer and calculate the total time taken
end_time = time.time()
total_time = end_time - start_time
print(f"Total time taken: {total_time:.2f} seconds")
