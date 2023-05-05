from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import os
import wget
import time


# Credentials
print("Please enter your credentials:")
insta_id = input('Username/Email/Phone Number >>> ')
pswd = input("Password >>> ")


# Purpose
purpose = input("\nWhat do you want to do with Insta :\n1) Just Login and use it\n2) Search for a user or a Hashtag\n3) Download any user's uploaded pictures\n4) Send spam to a friend\n")

driver = webdriver.Chrome(executable_path=r'D:\\Driver\\chromedriver.exe')

def login(insta_id, pswd):
    driver.get('https://www.instagram.com')

    username = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    username.clear()
    password.clear()

    username.send_keys(insta_id)
    password.send_keys(pswd)

    login = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    not_now = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
    not_now2 = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()


def search(srch, insta_id, pswd):
    if (insta_id != '' and pswd != ''):
        login(insta_id,pswd)

    if '#' in srch:
        driver.get(f'https://www.instagram.com/explore/tags/{srch[1:]}')
    else:
        driver.get(f'https://www.instagram.com/{srch}')


def save(srch, insta_id, pswd):
    search(srch, insta_id, pswd)
    for i in range(15):
        driver.execute_script("window.scrollTo(0,40000);")
        time.sleep(2)

    images = driver.find_elements_by_tag_name('img')
    images = [image.get_attribute('src') for image in images]

    if '#' in srch:
        dirName = srch[1:]
    else:
        dirName = srch

    path = os.getcwd()
    path = os.path.join(path, dirName)

    if (not os.path.exists(path)):
        os.mkdir(path)

    counter = 1

    for image in images:
        save_as = os.path.join(path, dirName + "-" + str(counter) + '.jpeg')
        wget.download(image, save_as)
        counter += 1


def spam(srch, insta_id, pswd, message, times):
    search(srch, insta_id, pswd)
    message = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Message')]"))).click()
    # textBox = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/textarea[@placeholder='Message...']")))
    mBox = driver.find_element_by_class_name('Igw0E').click()
    textBox = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[@placeholder='Message...']")))
    
    for i in range(int(times)):
        textBox.send_keys(message)
        textBox.send_keys(Keys.ENTER)


if purpose == "1":
    if (insta_id == '' or pswd == ''):
        insta_id = input('Username/Email/Phone Number >>> ')
        pswd = input("Password >>> ")

    login(insta_id, pswd)

if purpose == "2":
    driver.minimize_window()

    if (insta_id == '' or pswd == ''):
        insta_id = input('Username/Email/Phone Number >>> ')
        pswd = input("Password >>> ")

    srch = input("Whom do you want to search for???\n")
    search(srch, insta_id, pswd)

if purpose == "3":
    driver.minimize_window()

    if (insta_id == '' or pswd == ''):
        insta_id = input('Username/Email/Phone Number >>> ')
        pswd = input("Password >>> ")

    srch = input("Whose pictures do you want (Give the username or the Hashtag)>>> ")
    save(srch, insta_id, pswd)
    print("\nSaved the pictures!!!")

if purpose == "4":
    driver.minimize_window()
    if (insta_id == '' or pswd == ''):
        insta_id = input('Username/Email/Phone Number >>> ')
        pswd = input("Password >>> ")

    srch = input('Enter the username of your friend here >>> ')

    message = input("What do you want to spam in yours friend's chat >>> ")

    times = input("How many times do you want to send this message >>> ")

    spam(srch, insta_id, pswd, message, times)

else:
    print("Please write a valid index number.")

print("\n\nHope you like that ;)\n")