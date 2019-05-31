import pandas as pd
from datetime import datetime, timedelta
import requests

page_url = 'https://www.soccervista.com/soccer_games.php?date='
page_live = 'https://www.livescore.cz/live-soccer.php'
today = datetime.now().strftime('%Y-%m-%d')
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

class Scrape:

    def __init__(self, page, t, y, tom, live):
        self.page = page
        self.t = t
        self.y = y
        self.tom = tom
        self.live = live

    def yesterday(self):
        return self.page + self.y

    def today(self):
        return self.page + self.t

    def tomorrow(self):
        return self.page + self.tom

    def live_score(self):
        return self.live

    @staticmethod
    def soup(date, path):
        if date == 'today':
            r = requests.get(path)
            df = pd.read_html(r.content, attrs={'class':'main'})[0]
            df = df[2:]
        elif date == 'yesterday':
            r = requests.get(path)
            df = pd.read_html(r.content, attrs={'class':'main'})[0]
            df = df[2:]
        elif date == 'live':
            try:
                r = requests.get(path)
                df = pd.read_html(r.content, attrs={'class': 'tab main-live'})[0]
            except ValueError as e:
                print(e)
                return "No live games on right now!"
        else:
            r = requests.get(path)
            df = pd.read_html(r.content, attrs={'class': 'main'})[0]
            df = df[2:]
        return df

    @staticmethod
    def col_drop(df):
        cols = df.columns
        return [x for x in cols if type(x) == str]

    @staticmethod
    def change_data(df, date):
        if date == 'live':
            return df.rename(columns={0: 'Game Start', 1: 'Country / Live Time', 2: 'Home Team',
                                      3: 'Score', 4: 'Away Team'})
        else:

            return df.rename(columns={0: 'Game Start', 1: 'Country', 2: 'Home Team',
                                      3: 'Score', 4: 'Away Team'})