import requests
import os
import concurrent.futures
import imghdr  # Library to determine image file types
import time  # Import the time module
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


def main():
    # Input from the user

    # Create a directory to save the downloaded images
    DIR = input(
        "Enter the name of the directory to save images (leave blank for default): ") or "downloaded_images"
    create_directory(DIR)

    args = []
    a = [x + y + z for x in string.ascii_lowercase for y in string.ascii_lowercase for z in string.ascii_lowercase]
    counter = 0
    with open("urls.txt", "r") as f:
        urls = eval(f.read())
        for url in urls:
            args.append((url, DIR, a[counter]))
            counter += 1

    start_time = time.time()

    print(f"Total urls: {len(urls)}")

    # Download the images using threading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_image, args)

    end_time = time.time()

    total_time = end_time - start_time
    print(f"Total time taken: {total_time:.2f} seconds")
    print(f"Number of images available: {len([name for name in os.listdir(
        DIR) if os.path.isfile(os.path.join(DIR, name))]) - 1}")
    input()


if __name__ == "__main__":
    main()


''' DOM.js
let imgSrcArray = [];

function collectImages() {
    // Select the first div with class "o-justified-grid"
    let gridDiv = document.querySelector('.o-justified-grid');

    if (gridDiv) {
        let images = gridDiv.querySelectorAll('img');
        images.forEach(img => {
            // Check for lazy-loaded 'data-src' attribute or regular 'src'
            let src = img.getAttribute('data-src') || img.src;
            if (!imgSrcArray.includes(src)) {
                imgSrcArray.push(src);
            }
        });
    }
}

// Scroll and collect images from the specific div
function scrollAndCollect() {
    let scrollHeight = document.documentElement.scrollHeight;
    let currentPosition = 0;
    
    let interval = setInterval(() => {
        window.scrollTo(0, currentPosition);
        collectImages();
        currentPosition += window.innerHeight;

        if (currentPosition >= scrollHeight) {
            clearInterval(interval);
            console.log('All image sources:', imgSrcArray);
        }

        // Update scrollHeight in case more content gets loaded
        scrollHeight = document.documentElement.scrollHeight;
    }, 1000); // Adjust delay if necessary
}

// Start the scroll and collect process
scrollAndCollect();

'''

''' urls.txt
[
    'https://www.example.com/image1.jpg', 
    'https://www.example.com/image2.jpg', 
    'https://www.example.com/image3.jpg'
]
'''
