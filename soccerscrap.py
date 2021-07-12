from __future__ import annotations
from datetime import datetime
from typing import Dict
import pandas as pd
from bs4 import BeautifulSoup
import requests

# Information
'''
    Information: 
    Soccerscrap scraps data from soccerstats.com. All data belongs to them.
    Made by Gavin Loo / rawsashimi1604
'''

# Dictionary
'''
    List of leagues available for scrapping, use these as your class instance variables
    format: league : urlcode
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


class LeagueNotAvailable(Error):
    '''
        Raised when trying to get data from an unavailable league.
    '''
    pass


class TeamNotAvailable(Error):
    '''
        Raised when team cannot be found.
    '''
    pass


class WrongInput(Error):
    '''
        Raised when inputing wrong input into function parameter.
    '''
    pass


class SoccerScrap:
    def __init__(self, url_league, league_name) -> None:
        self.url_league = url_league
        self.league_name = league_name

    def __repr__(self) -> str:
        return f"League : {self.league_name}, URLCODE : {self.url_league}"

    @classmethod
    def from_league(cls, league: str) -> SoccerScrap:
        '''
            class method (alternative constructor) to create soccerscrap object from league
        '''
        try:
            url_league = leagues[league]

        except KeyError:
            raise LeagueNotAvailable(
                f"Data not available for league : {league}.")

        return cls(url_league, league)

    @classmethod
    def from_urlcode(cls, url: str) -> SoccerScrap:
        '''
            class method (alternative constructor) to create soccerscrap object from urlcode
        '''
        league_name = ""

        found_flag = False
        for key, value in leagues.items():
            if url == value:
                league_name = key
                found_flag = True

        if found_flag:
            return cls(url, league_name)

        else:
            raise LeagueNotAvailable(
                f"Data not available for urlcode : {url}.")

    @staticmethod
    def dt_check() -> None:
        '''
            Gets the date and time for info printing
        '''
        result = datetime.now().strftime("%B %d, %Y %H:%M:%S")
        return result

    def status(self) -> None:
        '''
            Gets current status of class
        '''

        print(f'''

        ** Welcome to SoccerScrap made by Gavin Loo / rawsashimi1604. **
        -----------------------------------------------------------------------
        SoccerScrap scraps data from soccerstats.com. All data belongs to them.
        -----------------------------------------------------------------------

        It is currently {self.dt_check()}.
        You are currently using urlcode : {self.url_league}
        You are currently using league : {self.league_name}
        Enjoy and have a nice day!

        Here is the current league table ....
        ''')

        print(self.table())
        print("\n\n\n")
        return None

    def get_team_urls(self) -> dict:
        '''
            Gets a list of dicts for URLS for each team's specific page.
        '''
        url = url = f"https://www.soccerstats.com/latest.asp?league={self.url_league}"

        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')

        links = []
        rows = soup.find('table', {'id': 'btable', 'cellpadding': "2"}).find_all('tr' , {'class' : "odd"})
        for row in rows:
            team = row.find('td', {'align' : 'left'}).find('a').text
            link = "https://www.soccerstats.com/" + row.find('td', {'align' : 'left'}).find('a')['href']
            links.append({"team" : team, "url" : link})

        return links

    def team_players(self, team: str) -> pd.DataFrame:
        '''
            Find team players for specific team
        '''
        list_teams = self.get_team_urls()

        def team_url(n_team):
            counter = 0
            for dicts in list_teams:
                if dicts['team'] == n_team:
                    return list_teams[counter]

                counter += 1
            raise TeamNotAvailable("Team cannot be found.")
        
        result = team_url(team)
        url = result['url']
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')

        table = soup.find('table', {'id' : 'btable', 'width' : '100%', 'cellspacing' : '0', 'cellpadding' : '2', 'border' : '0'})

        t_headers = table.find('tr', {'class' : 'trow1'}).find_all('th')
        headers = [ele.text.strip() for ele in t_headers]
        headers.pop(0)
        headers[0] = "Kit Number"

        data = []
        t_rows = table.find_all('tr', {'class' : 'odd'})
        for row in t_rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            cols.pop(1)
            data.append(cols)

        df = pd.DataFrame(data, columns=headers, dtype='string')

        return df

    def team_results(self, team: str) -> pd.DataFrame:
        '''
            Find team results for specific team
        '''
        list_teams = self.get_team_urls()

        def team_url(n_team):
            counter = 0
            for dicts in list_teams:
                if dicts['team'] == n_team:
                    return list_teams[counter]

                counter += 1
            raise TeamNotAvailable("Team cannot be found.")

        result = team_url(team)
        url = result['url']
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')

        table = soup.find('table', {'cellspacing' : '0', 'cellpadding' : '0', 'bgcolor' : '#cccccc', 'width': '100%'})
        headers = ["Date", "Home", "Score", "Away"]
        data = []
        selector = [0, 1, 2, -6]
        t_rows = table.find_all('tr', {'height' : '28'})
        for row in t_rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            cols[2] = cols[2].split('\n')[0]
            cols = [cols[x] for x in selector]
            data.append(cols)

        data.pop(0)

        df = pd.DataFrame(data, columns=headers, dtype="string")

        return df

    def team_goals(self, team: str) -> pd.DataFrame:
        '''
            Find team goals for specific team

        '''
        list_teams = self.get_team_urls()

        def team_url(n_team):
            counter = 0
            for dicts in list_teams:
                if dicts['team'] == n_team:
                    return list_teams[counter]

                counter += 1
            raise TeamNotAvailable("Team cannot be found.")

        result = team_url(team)
        url = result['url']
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')

        table = soup.find('table', {'cellspacing' : '0', 'cellpadding' : '0', 'bgcolor' : '#cccccc', 'width': '99%'})
        t_headers = table.find('tr', {'bgcolor' : '#666666'}).find_all('td')

        headers = [ele.text.strip() for ele in t_headers]

        data = []
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append(cols)

        data.pop(0)
        data.pop(0)
        data.pop(-1)

        df = pd.DataFrame(data, columns=headers, dtype="string")
        return df

    def team_total_goals(self, team: str) -> pd.DataFrame:
        '''
            Find team total goals for specific team

        '''
        list_teams = self.get_team_urls()

        def team_url(n_team):
            counter = 0
            for dicts in list_teams:
                if dicts['team'] == n_team:
                    return list_teams[counter]

                counter += 1
            raise TeamNotAvailable("Team cannot be found.")

        result = team_url(team)
        url = result['url']
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')

        table = soup.find('table', {'cellspacing' : '0', 'cellpadding' : '0', 'bgcolor' : '#cccccc', 'width': '99%'}).findNext('table').findNext('table')
        t_headers = table.find('tr', {'bgcolor' : '#666666'}).find_all('td')

        headers = [ele.text.strip() for ele in t_headers]

        data = []
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append(cols)

        data.pop(0)
        data.pop(0)
        data.pop(-1)

        df = pd.DataFrame(data, columns=headers, dtype="string")
        return df

    def team_patterns(self, team: str) -> pd.DataFrame:
        '''
            Find goal scoring patterns for specific team

        '''
        list_teams = self.get_team_urls()

        def team_url(n_team):
            counter = 0
            for dicts in list_teams:
                if dicts['team'] == n_team:
                    return list_teams[counter]

                counter += 1
            raise TeamNotAvailable("Team cannot be found.")

        result = team_url(team)
        url = result['url']
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')

        table = soup.find('table', {'cellspacing' : '0', 'cellpadding' : '0', 'bgcolor' : '#cccccc', 'width': '99%'}).findNext('table')
        t_headers = table.find('tr', {'bgcolor' : '#666666'}).find_all('td')

        headers = [ele.text.strip() for ele in t_headers]

        data = []
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append(cols)

        data.pop(0)
        data.pop(0)
        data.pop(-1)

        df = pd.DataFrame(data, columns=headers, dtype="string")
        return df
    
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

        # Finding table
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

    def table_first(self) -> pd.DataFrame:
        '''
            Gets league table based on first half scores.
        '''
        url = f"https://www.soccerstats.com/halftime.asp?league={self.url_league}"

        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')

        # Finding table of goals
        table = soup.find('table', {'id': 'btable', 'cellpadding': "0"})

        # Headers
        th_rows = table.find('tr', {'class': 'trow2'}).find_all('th')
        headers = [ele.text.strip() for ele in th_rows]

        # Data
        data = []
        rows = table.find_all('tr', {'class': 'odd'})
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append(cols)

        df = pd.DataFrame(data, columns=headers, dtype='string')
        return df

    def table_second(self) -> pd.DataFrame:
        '''
            Gets league table based on second half scores.
        '''
        url = f"https://www.soccerstats.com/halftime.asp?league={self.url_league}"

        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')

        # Finding table of goals
        table = soup.find(
            'table', {'id': 'btable', 'cellpadding': "0"}).findNext('table')

        # Headers
        th_rows = table.find('tr', {'class': 'trow2'}).find_all('th')
        headers = [ele.text.strip() for ele in th_rows]

        # Data
        data = []
        rows = table.find_all('tr', {'class': 'odd'})
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append(cols)

        df = pd.DataFrame(data, columns=headers, dtype='string')
        return df

    def table_form(self) -> pd.DataFrame:
        '''
            Gets form table of the last 6 matches played.
        '''
        url = f"https://www.soccerstats.com/formtable.asp?league={self.url_league}"

        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')

        # Finding table of goals
        table = soup.find(
            'table', {'id': 'btable', 'cellpadding': "0"}).findNext('table')

        # Headers
        th_rows = table.find('tr', {'class': 'trow2'}).find_all('th')
        headers = [ele.text.strip() for ele in th_rows]

        # Data
        data = []
        rows = table.find_all('tr', {'class': 'odd'})
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append(cols)

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

        elif table_data == 'home':
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

        elif table_data == 'away':
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

        else:
            raise WrongInput("Please check your input and only use ('total', 'home' or 'away').")


        return df

    def timing_goals(self, table_data: str) -> pd.DataFrame:
        '''
            Find time of goals.
            Format : goals scored - goals conceded
            table_data = both, home, away
        '''
        url = f"https://www.soccerstats.com/timing.asp?league={self.url_league}"

        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')

        if table_data == 'both':
            # Finding table of goals
            table = soup.find('table', {'cellspacing': "1"})

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

        elif table_data == 'home':
            # Finding table of goals
            table = soup.find('table', {'cellspacing': "1"})
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

        elif table_data == 'away':
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

        else:
            raise WrongInput("Please check your input and only use ('both', 'home' or 'away').")
            
        return df


'''
    Testing Hub
'''
# test = SoccerScrap.from_urlcode('england')
# result = test.timing_goals("both")
# print(result)
