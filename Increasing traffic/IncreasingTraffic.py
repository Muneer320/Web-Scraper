from selenium import webdriver
import time


start = 0.00

def generateURL(site):
    if 'https://' or 'http://' in site:
        url = site
    elif 'https://' not in site:
        if '.blogspot.com' in site:
            url = 'http://' + site
        else:
            url = 'https://' + site
    return url

def crawl(url, num):

    print(f'Opening {url}')

    
    driver = webdriver.Chrome(executable_path=r'D:\\Driver\\chromedriver.exe')

    start = time.time()

    for i in range(num):
        driver.get(url)
        print(f'Opened {i + 1} times.')
    
    end = time.time()
    timeTaken = (end - start)

    if timeTaken <= 100 :
        print(f'It took me {timeTaken} seconds successfully opened {url} {num} times.')
    elif timeTaken > 100 :
        print(f'It took me about {round(timeTaken / 60)} minutes to successfully open {url} {num} times.')


url = generateURL(input('Enter the URL of the site you want to open: '))
num = int(input("How many times would you like to open the site: "))
wish = input(f'Are you sure you want to open {url} (Y/N) >>> ').capitalize()


if wish == 'Y' or wish == 'YES':
    crawl(url, num)

elif wish == 'N' or wish == "NO":
    print('\nAbourting...')

else:
    print("Please write either 'Y' or 'N' only!")

print('\nHope you liked our services ;)\nMeet you soon.')