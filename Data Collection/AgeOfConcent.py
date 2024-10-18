from bs4 import BeautifulSoup
import requests


def get_age_of_consent():
    url = "https://www.ageofconsent.net/world"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    data_table = soup.find("table")

    countries = []
    ages = []

    for row in data_table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) > 0:
            countries.append(cells[1].text)
            ages.append(cells[3].text)

    age_dict = dict(sorted(zip(countries, ages), key=lambda x: (not x[1].isdigit(), int(x[1]) if x[1].isdigit() else float('inf'))))
    
    return age_dict



print(get_age_of_consent())