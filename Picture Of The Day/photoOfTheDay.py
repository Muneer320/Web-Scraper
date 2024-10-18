from bs4 import BeautifulSoup
import requests
import wget
from datetime import datetime
import pprint
import time


date = str(datetime.today())[:10]
print("WELCOME TO 'PICTURE OF THE DAY' DOWNLOADER")


def main():
    down = input("\n\nDownload PICTURE OF THE DAY from (Enter 1\\2\\3):\n1: NASA\n2: ASTRONOMY.COM\n3: BOTH\n")


    if down == '1':
        NASA_APOD()

    elif down == '2':
        ASTRONOMY_COM_APOD()
    
    elif down == '3':
        NASA_APOD()
        ASTRONOMY_COM_APOD()

    else:
        print("\nPlease enter a valid option.")
        main()

    print("\n\nHope you liked it.")
    time.sleep(3)

def NASA_APOD():
    url = 'https://apod.nasa.gov/apod/'
    try:
        img = BeautifulSoup(requests.get(url).text, 'lxml').find('img')['src']
        print(img)  
        src = url + img
        print(src)

        wget.download(src, f'NASA_APOD_{date}.jpg')
    except:
        print("\nNASA PICTURE OF THE DAY is not available today.")

def ASTRONOMY_COM_APOD():
    url = 'https://astronomy.com/photos/picture-of-day'
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    img = soup.find_all('div', class_ = "hero")[0].find('a').find('img')['src']
    src = url + img
    print(src)

    wget.download(src, f'ASTRONOMY_COM_APOD_{date}.jpg')



if __name__ == '__main__':
    main()