import requests
from bs4 import BeautifulSoup
from pprint import pprint
import concurrent.futures
from tqdm import tqdm


def scrape(site):
    reqs = requests.get(site)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    urls = []
    prev = ""

    for link in soup.find_all('a'):
        url = link.get('href')

        try:
            if url == prev:
                continue
            if "HPMoR_Chap" in url:
                urls.append(url)
                prev = url

        except:
            pass

    with open("hpmor.txt", "w") as f:
        for item in urls:
            f.write(str(item) + "\n")
# pprint(scrape("https://hpmorpodcast.com/?page_id=56"))


def download1():
    with open("hpmor_modified.txt", "r") as f:
        urls = f.readlines()

    for url in urls:
        with open(f"HPMoR/{url[url.strip().rfind("/")+1:-1]}", "wb") as f:
            f.write(requests.get(url).content)


def download_mp3(url, filename):
    try:
        response = requests.get(url.strip(), stream=True)
        response.raise_for_status()  # Check for HTTP errors

        total_size = int(response.headers.get('Content-Length', 0))
        downloaded_size = 0

        with open(filename, 'wb') as file, tqdm(
            desc=filename[filename.find("_")+1:filename.find(".")],
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    progress_bar.update(len(chunk))

        if downloaded_size < total_size:
            print(f"Warning: {filename} may be incomplete. Downloaded {
                  downloaded_size} of {total_size} bytes.")
        else:
            print(f"Downloaded {filename} successfully.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}\nFile: {filename}\n")


def download2():
    with open("hpmor_modified.txt", "r") as f:
        urls = f.readlines()

    urls = [url.strip() for url in urls]
    filenames = ["HPMoR/" + url[url.rfind("/")+1:] for url in urls]

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(download_mp3, url, filename)
                   for url, filename in zip(urls, filenames)]

        for future in concurrent.futures.as_completed(futures):
            future.result()  # Wait for all futures to complete


download2()
