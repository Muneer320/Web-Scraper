import os
import requests
import time
import concurrent.futures
import string
import imghdr


def get_reddit_posts(subreddit, post_type='top', time='all', num_posts=100):
    url = f"https://www.reddit.com/r/{subreddit}/{
        post_type}.json?t={time}&limit={num_posts}&raw_json=1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None


def extract_image_urls(post_data):
    if not post_data:
        return []

    urls = []

    posts = post_data['data']['children']

    for post in posts:
        post_info = post['data']

        if 'media_metadata' in post_info:
            media_metadata = post_info['media_metadata']
            for media_id, media_data in media_metadata.items():
                if 's' in media_data and 'u' in media_data['s']:
                    url = media_data['s']['u']
                    url = url.replace('preview', 'i').split(
                        '?')[0]  # Get the direct image URL
                    urls.append(url)
        elif 'url_overridden_by_dest' in post_info:
            urls.append(post_info['url_overridden_by_dest'])

    return urls


def download_images(args):
    url, directory, name = args

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404)

        temp_filename = os.path.join(directory, f"{name}")
        with open(temp_filename, 'wb') as temp_file:
            for chunk in response.iter_content(chunk_size=8192):
                temp_file.write(chunk)

        # Detect the image type
        image_format = imghdr.what(temp_filename)
        if not image_format:
            print(f"Failed to determine image format: {url}")
            os.remove(temp_filename)  # Clean up the temporary file
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


def main():
    subreddit = input("Enter subreddit: ")
    post_type = input("Enter post type [hot/top]: ").lower() or 'top'
    num_posts = int(input("Enter number of posts to scrape [default 100]: ") or 100)
    save_folder = input("Enter location to save images [default 'images']: ") or 'images'

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    args = []

    print(f"\nFetching posts from r/{subreddit}...")

    s1 = time.time()
    post_data = get_reddit_posts(subreddit, post_type, num_posts=num_posts)
    e1 = time.time()

    if post_data:
        image_urls = extract_image_urls(post_data)
        if image_urls:
            print(f"Found {len(image_urls)} images. Downloading...")
        else:
            print("No images found.")
    else:
        print("Failed to fetch data from the subreddit.")

    names = [x + y + z for x in string.ascii_lowercase for y in string.ascii_lowercase for z in string.ascii_lowercase]

    for url in image_urls:
        # check if image has valid extension
        if not url.endswith(('jpg', 'jpeg', 'png', 'gif')):
            image_urls.remove(url)

    args = [(url, save_folder, names[i]) for i, url in enumerate(image_urls)]

    s2 = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_images, args)
    e2 = time.time()

    time1 = e1 - s1
    time2 = e2 - s2

    print(f"\nTime taken to get urls: {time1:.2f} seconds")
    print(f"Time taken download images: {time2:.2f} seconds")
    print(f"Total time taken: {time1 + time2:.2f} seconds\n")
    print(f"Number of images available: {len([name for name in os.listdir(
        save_folder) if os.path.isfile(os.path.join(save_folder, name))]) - 1}")
    input()


if __name__ == "__main__":
    main()