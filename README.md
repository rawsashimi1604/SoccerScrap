# SoccerScrap

Soccer stats web scraper to get data from soccerstats.com

This is a webscraper that uses BS4, requests and pandas to get data from soccerstats.com.

Currently, we are able to extract data from various league tables. I might create an API soon to faciliate better data management.

## Installation
Use pip to install all required dependencies. Key in this line of code into your terminal, it will proceed to download all dependencies required.
```python
pip install -r requirements.txt # Use either cmd line
pip3 install -r requirements.txt
```

## Usage
Create a new python file. Then import the SoccerScrap class from soccerscrap.py
```python
from soccerscrap import SoccerScrap
```

Using the following dictionary as keys,
```python
{
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
```

Then proceed to get data using the following code.
```python
myObj = SoccerScrap.from_urlcode("england") # To get Premier League Data.
myObj.status() # Return current status of league.
```

#### Class Methods
@classmethod from_league(*cls, league: str) -> **SoccerScrap**:
```python
 # Class method constructor to create SoccerScrap object from League Name.
 # Example Usage:
 myObj = SoccerScrap.from_league("Premier League") # Creates soccerscrap object with premier league.
 print(myObj)
 # Output : League : Premier League, URLCODE : england
```

@classmethod from_urlcode(*cls, url: str) -> **SoccerScrap**:
```python
 # Class method constructor to create SoccerScrap object from UrlCode.
 # Example Usage:
 myObj = SoccerScrap.from_league("england") # Creates soccerscrap object with premier league.
 print(myObj)
 # Output : League : Premier League, URLCODE : england
```

@staticmethod dt_check() -> **None**:
```python
# Gets the current date and time.
# Output : July 12, 2021 14:13:47
```

method status(*self*) -> **None**:
```python
# Prints current status of league and time.
```

method fixtures(*self*) -> **pd.DataFrame**:
```python
# Returns upcoming fixtures of the league, raises NotInSeason error if season has not started.
# Output : pd.DataFrame of fixtures
```

method table(*self*) -> **pd.DataFrame**:
```python
# Returns current table of league.
# Output : pd.DataFrame of league table
```

method table_first(*self*) -> **pd.DataFrame**:
```python
# Returns current table of league based on first half scores. 
# Output : pd.DataFrame of league table based on first half.
```

method table_second(*self*) -> **pd.DataFrame**:
```python
# Returns current table of league based on second half scores. 
# Output : pd.DataFrame of league table based on second half.
```

method table_form(*self*) -> **pd.DataFrame**:
```python
# Returns current form table.
# Output : pd.DataFrame of form table.
```

method total_goals(*self, table_data: str*) -> **pd.DataFrame**:
```python
# Returns avg total goals per match table, raises WrongInput error if keyed in wrong input.
# table_data: "home", "away", "total"
# Output : pd.DataFrame of goals table.
```

method timing_goals(*self, table_data: str*) -> **pd.DataFrame**:
```python
# Returns avg total goals per match table, raises WrongInput error if keyed in wrong input.
# table_data: "home", "away", "total"
# Output : pd.DataFrame of goals table.
```
