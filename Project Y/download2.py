import requests
import os
import concurrent.futures
import imghdr
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import string


# Function to create a directory if it doesn't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def download_image(args):
    url, directory, image_number = args

    try:
        # Download the image
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404)

        # Create a temporary file to save the image content
        temp_filename = os.path.join(directory, f"{image_number}")
        with open(temp_filename, 'wb') as temp_file:
            for chunk in response.iter_content(chunk_size=8192):
                temp_file.write(chunk)

        # Detect the image type
        image_format = imghdr.what(temp_filename)
        if not image_format:
            print(f"Failed to determine image format: {url}")
            return False

        # Rename the temporary file to the correct format
        final_filename = f"{temp_filename}.{image_format}"
        os.rename(temp_filename, final_filename)
        print(f"Downloaded: {final_filename}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Failed to download: {url} ({e})")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def collect_image_urls(driver, div_class_name):
    imgSrcArray = []

    # Scroll and collect images
    scroll_height = driver.execute_script("return document.documentElement.scrollHeight")
    current_position = 0

    while current_position < scroll_height:
        # Scroll down
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(1.5)  # Pause to allow lazy-loading

        # Collect image URLs
        images = driver.find_elements(By.CSS_SELECTOR, f'div.{div_class_name} img')
        for img in images:
            src = img.get_attribute('data-src') or img.get_attribute('src')
            if src and src not in imgSrcArray:
                imgSrcArray.append(src)

        # Update the scroll position and scroll height
        current_position += driver.execute_script("return window.innerHeight;")
        scroll_height = driver.execute_script("return document.documentElement.scrollHeight")

    return imgSrcArray


def main():
    # Input from the user
    webpage_url = input("Enter the webpage URL: ")

    # Create a directory to save the downloaded images
    DIR = input("Enter the name of the directory to save images (leave blank for default): ") or "downloaded_images"
    create_directory(DIR)

    # Selenium setup (using Chrome as an example)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless (without opening browser window)
    chrome_service = Service(executable_path="D:\Driver\chromedriver-win64\chromedriver.exe")

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    start_time1 = time.time()
    try:
        # Open the webpage
        driver.get(webpage_url)

        # Collect image URLs from the specific div
        image_urls = collect_image_urls(driver, "o-justified-grid")  # Assuming the class is "o-justified-grid"

    finally:
        driver.quit()
    end_time1 = time.time()
    time1 = end_time1 - start_time1

    # Download images from the collected URLs
    args = []
    a = [x + y + z for x in string.ascii_lowercase for y in string.ascii_lowercase for z in string.ascii_lowercase]
    for counter, url in enumerate(image_urls):
        args.append((url, DIR, a[counter]))


    print(f"Total URLs: {len(image_urls)}")

    start_time2 = time.time()
    # Download the images using threading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_image, args)

    end_time2 = time.time()

    time2 = end_time2 - start_time2
    print(f"\nTime taken to get urls: {time1:.2f} seconds")
    print(f"Time taken download images: {time2:.2f} seconds")
    print(f"Total time taken: {time1 + time2:.2f} seconds\n")
    print(f"Number of images available: {len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]) - 1}")
    input()


if __name__ == "__main__":
    main()
