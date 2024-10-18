import requests
from bs4 import BeautifulSoup
import pprint
import uuid
	
def getdata(url):
	r = requests.get(url)
	return r.text

site = input("Enter the url of the website that you want to scrape: ")
htmldata = getdata(site)
soup = BeautifulSoup(htmldata, 'html.parser')
urls = []
for item in soup.find_all('img'):
	urls.append(item['src'])


pprint.pprint(urls)
print(f"Total number of image links scraped: {len(urls)}")
next = input("Press 's' to save all the links in a txt file OR '0' to exit >>> ").lower()

if next == 's':
    name = str(uuid.uuid4()) + ".txt"
    with open(name, 'w') as f:
        f.write(f"Links to all the images from {site}:\n\n")
        for item in urls:
            f.write(item + "\n")
    print("Links saved successfully!!")
else:
    exit