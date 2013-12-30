#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup

from collections import namedtuple


PLAYERSBYTEAM_URL = "http://stats.swehockey.se/Teams/Info/PlayersByTeam/{}"
ROSTER_URL = "http://stats.swehockey.se/Teams/Info/TeamRoster/{}"


LEAGUES = {
    'SHL' : 3905,
    'HOCKEYALLSVENSKAN' : 3906
}



def integer_or_str(v):
    try:
        return int(v)
    except:
        pass
    return v


def float_or_str(v):
    try: 
        return float(v)
    except:
        return None


def country_code(v):
    return v[0:3]


def strings(td):
    s = []
    for st in td.stripped_strings:
        s.append(st)
    return u"".join(s)




DATA_MAP = {
    'country' : country_code, 
    'sgperc' : float_or_str,
    'foperc' : float_or_str,
    'gaa' : float_or_str,
    'svsperc' : float_or_str
}
    

INTEGERS = ('rk', 'no','pos','gp','g', 'a','tp','pim','plus','minus','plusminus','gwg','ppg','shg','sog', 'foplus','fominus','fo', 'weight', 'height', 'gpt', 'gkd', 'gpi', 'ga', 'svs', 'sog', 'so', 'w', 'l')
for k in INTEGERS:
    DATA_MAP[k] = integer_or_str


def translate(name, value):
    fnc = DATA_MAP.get(name, None)
    if fnc:
        return fnc(value)
    return value


SKATERSSTATS_COLUMNS = ('team', 'rk', 'no','name','pos','gp','g', 'a','tp','pim','plus','minus','plusminus','gwg','ppg','shg','sog', 
'sgperc','foplus','fominus','fo','foperc')

GOALIESTATS_COLUMNS = ('team', 'rk','no','name','gpt', 'gkd','gpi', 'mip', 'ga', 'svs', 'sog', 'svsperc', 'gaa','so','w','l')

TEAMROSTER_COLUMNS = ('team', 'no', 'name','dob','pos', 'shoots', 'height','weight','country','youthclub')



class ShlTable:

    columns = ()

    def load(self):
        
        league_id = LEAGUES.get(self.league, None)

        if league_id is None:
            return

        url = self.url.format(league_id)
    
        html = urllib2.urlopen(url).read()

        self.soup = BeautifulSoup(html)

        return self


    def __init__(self, league):
        self.league = league.upper()


    def get_teamnames(self):
        return [a['href'].rsplit("#")[-1] for a in self.soup.find(id="headerLinks").find_all("a")] 


    def gettablerows(self, table):
        return table.find_all("tr")[3:]


    def gettable(self, team):
        return self.soup.find(id=team).next_sibling



    def readrows(self):

        for team in self.get_teamnames():
            
            team_table = self.gettable(team)
            table = team_table.find("table", class_="tblContent")

            for tr in self.gettablerows(table):
                
                data = [team] + [strings(td) for td in tr.find_all("td")]
                
                formatted_data =  [translate(k, v) for k,v in zip(self.columns,data)]

                yield self.rowdata._make(formatted_data)



    def __iter__(self):
        return self.readrows()

    def fetch(self):
        return list(self)



class SkatersStats(ShlTable):
    columns = SKATERSSTATS_COLUMNS
    url = PLAYERSBYTEAM_URL
    rowdata = namedtuple("Player", SKATERSSTATS_COLUMNS)


class GoalieStats(ShlTable):
    columns = GOALIESTATS_COLUMNS
    url = PLAYERSBYTEAM_URL
    rowdata = namedtuple("Player", GOALIESTATS_COLUMNS)

    def gettable(self, team):
        skaters_table = self.soup.find(id=team)
        goalie_table = skaters_table.find_next_siblings("table")[1]
        return goalie_table



class TeamRosters(ShlTable):
    columns = TEAMROSTER_COLUMNS
    url = ROSTER_URL
    rowdata = namedtuple("Player", TEAMROSTER_COLUMNS)

    def gettablerows(self, table):
        return table.find_all("tr")[3:-2]



def goalie_stats(league):
    return GoalieStats(league).load()


def skater_stats(league):
    return SkatersStats(league).load()


def all_players(league):
    return TeamRosters(league).load()


def main():
    for s in all_players('shl'):
        print s
    for s in goalie_stats('shl'):
        print s
    for s in skater_stats('shl'):
        print s
    


if __name__ == '__main__':
    main()