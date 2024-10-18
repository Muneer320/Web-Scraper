# For checking the number of Images (with duplicates) availale in the webpages.

import requests
from bs4 import BeautifulSoup


url = input("Enter the base URL: ")
if not url.endswith("/"):
    url += "/"
start_page = int(input("Enter the starting page number: "))
end_page = int(input("Enter the ending page number: "))
total = 0

for page_number in range(start_page, end_page + 1):
    page_url = f"{url}page-{page_number}"
    response = requests.get(page_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img', class_='bbImage')
        total += len(img_tags)
        print(f"Page {page_number}: {len(img_tags)} images")

    else:
        print(f"Failed to retrieve the web page: {page_url}")

print("Total number of images: ",total)
input()