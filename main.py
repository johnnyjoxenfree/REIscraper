from bs4 import BeautifulSoup
import requests
import json
import csv
from tqdm import tqdm

def getsite (url):
    return requests.get(url)

page = getsite('https://www.rei.com/stores/map')
soup = BeautifulSoup(page.content, 'html.parser')
url = 'https://www.rei.com'
file = 'stores.csv'

locations = soup.findAll('div', class_='store-directory__state')

for div in tqdm(locations):
    for h in tqdm(div.findAll('a')):
        extension = h['href']
        location = url + extension
        site = getsite(location)
        consomme = BeautifulSoup(site.content, 'html.parser')

        content = consomme.find("script", id="store-schema")
        store = "REI " + json.loads(content.text)['name']
        baseadd = json.loads(content.text)['address']
        address = baseadd["streetAddress"] + " " + baseadd["addressLocality"] + " " + baseadd["addressRegion"] + " " + baseadd["postalCode"]
        address = address.replace(',','')

        row = [store,address]

        with open(file, 'a', newline='') as fileobj:
            writer = csv.writer(fileobj)
            writer.writerow([store, address])
        

# ~iosj 2022