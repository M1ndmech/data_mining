import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime, time, timedelta
import time
import re
import json

url = 'https://www.boxofficemojo.com/intl/?ref_=bo_nb_hm_tab'
response = requests.get(url, headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'})

soup = BeautifulSoup(response.content, 'html.parser')

release_links = []
for link in soup.find_all('td', ('class', 'a-text-left mojo-field-type-release mojo-cell-wide')):
    release_links.append(link.find('a').get('href'))

url_joined = []
for link in release_links:
  url_joined.append(urllib.parse.urljoin('https://www.boxofficemojo.com', link))

data = []
for url in url_joined:
    response = requests.get(url, headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'})
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('div', {'class': 'a-section a-spacing-none mojo-summary-values mojo-hidden-from-mobile'})
    rows = table.find_all('div', {'class': 'a-section a-spacing-none'})

    row_data={}
    for row in rows:
        key = row.find('span').text.strip()
        value = row.find_all('span')[1].text.strip()
        if key == 'Opening':
            value = int(re.sub('[^0-9]', '', value))
        elif key == 'Release Date':
            value = value
        elif key == 'Running Time':
            time_delta = datetime.strptime(value, '%H hr %M min') - datetime(1900, 1, 1)
            value = time_delta.total_seconds()
        elif key == 'Genres':
            value = [genre.strip() for genre in value.split('\n') if genre.strip()]
        elif key == 'In Release':
            value = value.replace(' days/3 weeks', '').strip()
        elif key == 'Widest Release':
            value = int(re.sub('[^0-9]', '', value))
        
        row_data[key] = value
    
    data.append(row_data)
    time.sleep(10)

with open('box_office_data.json', 'w') as f:
    json.dump(data, f)