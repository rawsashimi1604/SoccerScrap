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


class Error(Exception):
    '''
        Base class for other exceptions.
    '''
    pass


class NotInSeason(Error):
    '''
        Raised when trying to get data from off season.
    '''
    pass


class SoccerScrap:

    url_league = ""

    def __init__(self):
        pass

    def set_league(self, league: str) -> None:
        '''
            Choose which league to find data in.
        '''
        self.url_league = leagues[league]

        return None

    def fixtures(self) -> pd.DataFrame:
        '''
            Find upcoming fixtures of the league.
        '''

        url = f"https://www.soccerstats.com/latest.asp?league={self.url_league}"
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')

        try:
            # Finding table of goals
            table = soup.find('div', {'class': 'eight columns'}).find(
                'table', {'id': 'btable'})

            # Headers
            headers = ['Date', 'Home Team', 'Away Team']

            # Data
            data = []
            rows = table.find_all('tr', {'class': 'odd'})
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append(cols)

            for sublist in data:
                del sublist[2]
                del sublist[-1]

            df = pd.DataFrame(data, columns=headers, dtype='string')

        except ValueError:
            raise NotInSeason(
                "Unable to retrive fixtures. Check season start date.")

        return df

    def table(self) -> pd.DataFrame:
        '''
            Retrieves current league table.
        '''
        url = f"https://www.soccerstats.com/latest.asp?league={self.url_league}"

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

        return df

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
test.set_league('Ligue 2')
result = test.table()
print(result)
