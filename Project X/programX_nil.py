from bs4 import BeautifulSoup
import os
from deleteDuplicates import delete_duplicate_images


def extract_img_src(html):
    soup = BeautifulSoup(html, 'html.parser')
    img_tags = soup.find_all('img')
    srcs = [img.get('src') for img in img_tags if img.get('src')]
    return srcs

def purify_img_src(srcs):
    res = []
    for x in srcs:
        if not (x.startswith('data:') or x.startswith('https://desifakes.com')):
            res.append(x)
            # print(f"Removed: {x}")
    return res

def download_img(urls, folder):
    import requests
    
    count = 1
    for x in urls:
        print(f"Downloading: {x}")
        img_data = requests.get(x).content
        with open(f'{folder}/image_{count}.jpg', 'wb') as handler:
            handler.write(img_data)
        count += 1

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def main():
    # srcs = extract_img_src(input("Enter HTML: \n"))
    with open("srcs.txt", "r") as file:
        srcs = purify_img_src(eval(file.read()))

    directory =  input("Enter the name of the directory to save images (leave blank for default): ")
    DIR = "downloaded_images" if directory == "" else directory
    create_directory(DIR)
    
    download_img(srcs, DIR)
    print("Images downloaded!")
    delete_duplicate_images(DIR)
    print("Deleted dublicate images!")

if __name__ == "__main__":
    main()