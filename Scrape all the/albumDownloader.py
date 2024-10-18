import requests
import os
import concurrent.futures
import time
import string


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def generate_codes(n):
    codes = []
    i = 0
    # Start with 3 characters by default
    while len(codes) < n:
        code = ""
        num = i
        # Generate base-26 code starting with 'aaa'
        while True:
            code = string.ascii_lowercase[num % 26] + code
            num = num // 26 - 1
            if num < 0:
                break
        # Only accept codes with a length of 3 or more
        if len(code) >= 3:
            codes.append(code)
        i += 1
    return codes



def download_image(url, img_num, file):
    try:
        response = requests.get(f"{url}{img_num}.png", stream=True)
        response.raise_for_status() 

        with open(file, 'wb') as temp_file:
            for chunk in response.iter_content(chunk_size=8192):
                temp_file.write(chunk)

        print(f"Downloaded: {file}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Failed to download: {url} ({e})")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    url = input("Enter the URL: ")
    url = url[:url.find("Page")+4]
    # print(url)
    
    dir = input("Enter the directory name to save images (leave blank for default): ") or "downloaded_images"
    create_directory(dir)

    num_images = int(input("Enter the number of images: "))
    names = generate_codes(num_images)


    # Download the images
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(num_images):
            executor.submit(download_image, url, str(i+1).zfill(2), f"{dir}/{names[i]}.png")

    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    print(f"Number of images available: {len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))])}")
    input()



if __name__ == "__main__":
    main()