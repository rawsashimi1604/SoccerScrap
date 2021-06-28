import pandas as pd  # DataFrame / Excel handler
from bs4 import BeautifulSoup  # Web Scraper
import requests  # URL Requests to feed bs4

# Hask map of leagues
# Dictionary {'league' : 'URL'}

# Class instance will be created based on League
# SoccerScrap(self, league)

url = "https://www.soccerstats.com/latest.asp?league=japan"
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')

# Finding table of goals
table = soup.find('table', {'id': 'btable', 'cellpadding': "2"})

# Headers
th_rows = table.find('tr', {'class': 'trow2'}).find_all('th')
headers = [ele.text.strip() for ele in th_rows]
headers[0] = 'Pos'
headers[1] = 'Team'
headers = headers[0:10]


# Data
data = []
rows = table.find_all('tr', {'class': 'odd'})
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append(cols)

data = [sublist[0:10] for sublist in data]


df = pd.DataFrame(data, columns=headers, dtype='string')
print(df)
