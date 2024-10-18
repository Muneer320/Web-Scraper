import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import concurrent.futures
import filetype
import time
import hashlib
import string

# Global variables to track failed downloads
failed = 0
failed_urls = []

# Default user-agent and referer headers
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

# Function to create a directory if it doesn't exist


def create_directory(directory, log_function):
    if not os.path.exists(directory):
        os.makedirs(directory)
        log_function(f"Created directory: {directory}")

# Function to download an image from a URL


def download_image(args):
    page_url, url, directory, image_name, log_function = args
    try:
        headers = DEFAULT_HEADERS.copy()
        headers['Referer'] = page_url

        # Download the image
        try:
            response = requests.get(url, headers=headers, stream=True)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            error_message = f"Error: Failed to download from URL: {
                url}\nDetails: {str(e)}"
            log_function(error_message)
            return

        # Create a temporary file to save the image content
        temp_filename = os.path.join(directory, f"{image_name}")
        with open(temp_filename, 'wb') as temp_file:
            for chunk in response.iter_content(chunk_size=8192):
                temp_file.write(chunk)

        log_function(f"Downloaded: {url}")

        # Detect the image type
        image_format = filetype.guess_extension(temp_filename)
        if not image_format:
            # log_function(f"Failed to determine image format: {url}")
            return False

        # Rename the temporary file to the correct format
        final_filename = f"{temp_filename}.{image_format}"
        os.rename(temp_filename, final_filename)
        return True

    except requests.exceptions.RequestException as e:
        global failed, failed_urls
        log_function(f"Failed to download: {url} ({e})")
        failed += 1
        failed_urls.append(url)
        return False
    except Exception as e:
        log_function(f"Error: {e}")
        return False

# Function to calculate file hash for duplicate checking


def file_hash(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as file:
        while chunk := file.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

# Remove duplicate files in a directory


def remove_duplicate_files(directory, log_function):
    seen = set()
    num = 0
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            filehash = file_hash(filepath)
            if filehash in seen:
                num += 1
                log_function(f"Removing duplicate: {filepath}")
                os.remove(filepath)
            else:
                seen.add(filehash)

# Add appropriate file extensions if saved without one


def add_extn(directory, log_function):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path) and '.' not in filename:
            image_format = filetype.guess_extension(file_path)
            if image_format:
                new_filename = f"{file_path}.{image_format}"
                os.rename(file_path, new_filename)
                log_function(f"Added extension {
                             image_format} to file: {file_path}")

# Main function for GUI and script interaction


def main_function(url, start_page, end_page, DIR, log_function=print):
    start_time = time.time()

    names = [x + y + z for x in string.ascii_lowercase for y in string.ascii_lowercase for z in string.ascii_lowercase]
    image_number = 1
    image_urls = []
    arg = []

    create_directory(DIR, log_function)

    for page_number in range(start_page, end_page + 1):
        page_url = f"{url}/page-{page_number}"
        log_function(f"Retrieving page: {page_url}")
        try:
            response = requests.get(page_url)
        except requests.exceptions.RequestException as e:
            error_message = f"Error: Failed to download from URL: {
                url}\nDetails: {str(e)}"
            log_function(error_message)
            return

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tags = soup.find_all('img', class_='bbImage')
            for img_tag in img_tags:
                img_url = img_tag.get('src')
                if img_url:
                    img_url = urljoin(page_url, img_url)
                    image_urls.append(img_url)
        else:
            log_function(f"Failed to retrieve the web page: {page_url}")

    log_function(f"Number of image urls found: {len(image_urls)}")
    image_urls = list(dict.fromkeys(image_urls))
    log_function(f"Number of unique image urls found: {len(image_urls)}")

    for x in image_urls:
        arg.append((page_url, x, DIR, names[image_number], log_function))
        image_number += 1

    with open(f"{DIR}/info.txt", "w") as f:
        f.write(f"URL: {url}\n")
        f.write(f"Start page: {start_page}\n")
        f.write(f"End page: {end_page}\n")
        f.write("\n\nUrls:\n")
        for i, y in enumerate(image_urls):
            f.write(f"{i+1}. {y}\n")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_image, arg)

    add_extn(DIR, log_function)
    remove_duplicate_files(DIR, log_function)

    end_time = time.time()
    total_time = end_time - start_time
    log_function(f"\nTotal time taken: {total_time:.2f} seconds")

    if failed:
        log_function(f"Number of failed attempts: {failed}")
        with open(f"{DIR}/failed_urls.txt", "w") as f:
            f.write(f"Total failed attempts: {failed}\n\nFailed URLs:\n")
            for url in failed_urls:
                f.write(f"{url}\n")

    log_function("Process completed.")
