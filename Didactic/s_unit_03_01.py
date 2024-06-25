import requests
from bs4 import BeautifulSoup
import urllib.parse

url = 'https://www.boxofficemojo.com/intl/?ref_=bo_nb_hm_tab'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

release_links = []
for link in soup.find_all('td', ('class', 'a-text-left mojo-field-type-release mojo-cell-wide')):
    release_links.append(link.find('a').get('href'))

url_joined = []
for link in release_links:
  url_joined.append(urllib.parse.urljoin('https://www.boxofficemojo.com', link))

table = soup.find('table', {'class': 'a-bordered'})
headers = [header.text for header in table.find_all('th')]

data = []
for row in table.find_all('tr'):
    row_data = {}
    cells = row.find_all('td')
    if cells:
        row_data[headers[0]] = cells[0].find('a').text
        row_data[headers[1]] = cells[1].text
        row_data[headers[2]] = int(cells[2].text)
        row_data[headers[3]] = cells[3].find('a').text
        row_data[headers[4]] = cells[4].text.strip()
        row_data[headers[5]] = int(cells[5].text.replace('$', '').replace(',', ''))
        data.append(row_data)

import pandas as pd
df = pd.DataFrame(data)
print(df)