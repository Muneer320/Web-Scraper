from bs4 import BeautifulSoup
import requests
import time
import os
import glob
import datetime

date = str(datetime.datetime.now())

familiar_skill = input("Put the skill that you are familiar with => ")
familiar_skill.replace(" ","+")

unfamiliar_skill = input("Put some skills that you are unfamiliar with (Write in one word) => ")
unfamiliar_skill.replace(" ","+")

print(f"Fetching in {familiar_skill} and filtering out {unfamiliar_skill}")

def find_jobs():
    url = "https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords="+ familiar_skill +"&txtLocation="
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li', class_ = "clearfix job-bx wht-shd-bx")


    if (not os.path.exists("posts")):
        os.mkdir('posts')
        
    try:
        os.mkdir(f'posts/{familiar_skill}')
    except:
        files = glob.glob(f'posts/{familiar_skill}/*')
        for f in files:
            os.remove(f)

    for index, job in enumerate(jobs):
        posted_date = job.find('span', class_ = "sim-posted").span.text

        if "few" in posted_date:
            company_name = job.find('h3' , class_ = "joblist-comp-name").text.replace(' ', '')
            skills = job.find('span', class_ = "srp-skills").text.replace(' ', '').replace(',', ', ')
            more_info = job.header.h2.a['href']
                    

            if unfamiliar_skill not in skills:
                with open(f'posts/{familiar_skill}/{index}.txt', 'w') as f:
                    f.write(f"Date: {date[:10]}\tTime: {date[10:19]}\n\n")
                    f.write(f'Company Name = {company_name.strip()}\nRequired Skills = {skills.strip()}\nMore Info = {more_info}')
                print(f'Files saved: {index}')
        
if __name__ == '__main__':
    while True:
        find_jobs()
        print('Waiting for 20 minutes...')
        time.sleep(1200)