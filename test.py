import pandas as pd  # DataFrame / Excel handler
from bs4 import BeautifulSoup  # Web Scraper
import requests  # URL Requests to feed bs4

# Hask map of leagues
# Dictionary {'league' : 'URL'}

# Class instance will be created based on League
# SoccerScrap(self, league)

url = "https://www.soccerstats.com/timing.asp?league=japan"
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')

# Finding table of goals
table = soup.find('table', {'cellspacing': "1"})
table = table.findNext('table', {'cellspacing': '1'})
table = table.findNext('table', {'cellspacing': '1'})

# Headers
th_rows = table.find('tr', {'bgcolor': '#d0d0d0'}).find_all('td')
headers = [ele.text.strip() for ele in th_rows]


# Data
data = []
rows = table.find_all('tr', {'height': '22'})
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append(cols)

df = pd.DataFrame(data, columns=headers, dtype='string')
print(df)
