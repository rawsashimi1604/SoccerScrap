import pandas as pd
from bs4 import BeautifulSoup
import requests

'''
    Information: 
    Soccerscrap scraps data from soccerstats.com and stores it in a usable JSON format, or excel file.
    Made by Gavin Loo / rawsashimi1604
'''

'''
    List of leagues available for scrapping, use these as your class instance variables
'''
leagues = {
    # ---- English Leagues ----
    'Premier League': 'england',
    'Championship': 'england2',
    'League One': 'england3',
    'League Two': 'england4',

    # ---- German Leagues ----
    'Bundesliga': 'germany',
    '2. Bundesliga': 'germany2',

    # ---- Italian Leagues ----
    'Serie A': 'italy',
    'Seria B': 'italy2',

    # ---- Spanish Leagues ----
    'La Liga': 'spain',
    'La Liga 2': 'spain2',

    # ---- French Leagues ----
    'Ligue 1': 'france',
    'Ligue 2': 'france2',

    # ---- Japanese Leagues ----
    'J1 League': 'japan'
}


class SoccerScrap:

    url_league = ""

    def __init__(self):
        pass

    def set_league(self, league: str):
        '''
            Choose which league to find data in.
        '''
        self.url_league = leagues[league]

    def total_goals(self, table_data: str) -> pd.DataFrame:
        '''
            Find avg total goals per match of each team.
            table_data = total, home, away
        '''
        URL = f"https://www.soccerstats.com/trends.asp?league={self.url_league}"
        req = requests.get(URL)
        soup = BeautifulSoup(req.content, 'html.parser')

        total = soup.find('table', {'class': 'sortable'})
        home = total.find_next('table')
        away = home.find_next('table')

        if table_data == 'total':
            th_row = total.find('thead').find('tr').find_all('th')
            headers = [ele.text.strip() for ele in th_row]

            # Data
            data = []
            rows = total.find_all('tr', {'class': 'odd'})
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append(cols)

            df = pd.DataFrame(data, columns=headers, dtype='string')

        if table_data == 'home':
            th_row = home.find('thead').find('tr').find_all('th')
            headers = [ele.text.strip() for ele in th_row]

            # Data
            data = []
            rows = home.find_all('tr', {'class': 'odd'})
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append(cols)

            df = pd.DataFrame(data, columns=headers, dtype='string')

        if table_data == 'away':
            th_row = away.find('thead').find('tr').find_all('th')
            headers = [ele.text.strip() for ele in th_row]

            # Data
            data = []
            rows = away.find_all('tr', {'class': 'odd'})
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append(cols)

            df = pd.DataFrame(data, columns=headers, dtype='string')

        return df


test = SoccerScrap()
test.set_league('J1 League')
result = test.total_goals('away')
print(result)
