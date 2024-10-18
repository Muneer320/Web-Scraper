import requests
from bs4 import BeautifulSoup
import pprint
import uuid

def scrape(site):
    reqs = requests.get(site)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    urls = []
    # for link in soup.find_all('a'):
    #     urls.append(link.get('href'))

    for link in soup.find_all('img'):
        urls.append(link.get('src'))

    return urls


if __name__ == "__main__":
    site = input("Enter the url of the website that you want to scrape: ")
    urls = scrape(site)

    for link in urls:
        link = str(link)
        if link.startswith("/"):
            urls.remove(link)
            urls.append(f"{site}/{link}")

    pprint.pprint(urls)
    print(f"Total number of image links scraped: {len(urls)}")
    next = input("Press 's' to save all the links in a txt file OR '0' to exit >>> ").lower()

    if next == 's':
        name = str(uuid.uuid4()) + ".txt"
        with open(name, 'w') as f:
            f.write(f"All links from {site}:\n\n")
            for item in urls:
                f.write(str(item) + "\n")
        print("Links saved successfully!!")
    else:
        exit
