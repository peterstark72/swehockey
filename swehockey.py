#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import datetime
from collections import namedtuple

from bs4 import BeautifulSoup


PLAYERSBYTEAM_URL = "http://stats.swehockey.se/Teams/Info/PlayersByTeam/{}"
ROSTER_URL = "http://stats.swehockey.se/Teams/Info/TeamRoster/{}"

SKATERSSTATS_COLUMNS = ('team', 'rk', 'no','name','pos','gp','g', 'a','tp','pim','plus','minus','plusminus','gwg','ppg','shg','sog', 
'sgperc','foplus','fominus','fo','foperc')
GOALIESTATS_COLUMNS = ('team', 'rk','no','name','gpt', 'gkd','gpi', 'mip', 'ga', 'svs', 'sog', 'svsperc', 'gaa','so','w','l')
TEAMROSTER_COLUMNS = ('team', 'no', 'name','dob','pos', 'shoots', 'height','weight','country','youthclub')


LEAGUE_MAP = {
    3905 : (u'SHL', '20132014', 'regular'),
    3906 : (u'Hockeyallsvenskan', '20132014', 'regular'),
    3928 : (u'Allettan Mellan', '20132014', 'regular'),
    3929 : (u'Allettan Södra', '20132014', 'regular'),
    3882 : (u'Division 1 Norra', '20132014', 'regular'),
    3878 : (u'Division 1 C', '20132014', 'regular'),
    3930 : (u'Division 1 C Forts.', '20132014', 'regular'),
    2892 : (u'Elitserien', '20122013', 'regular'),
    3810 : (u'SM-slutspel', '20122013', 'playoff'),
    3811 : (u'Kval till Elitserien', '20122013', 'qualification'),
}



class SweHockeyException(Exception):
    pass




def integer_or_none(v):
    try:
        return int(v)
    except ValueError:
        pass

def float_or_none(v):
    try: 
        return float(v)
    except ValueError:
        pass



INTEGERS = 'rk','no','gp','g','a','tp','pim','plus','minus','plusminus','gwg','ppg','shg','sog','foplus','fominus','fo','weight','height','gpt','gkd','gpi','ga','svs','sog','so','w','l'
FLOATS= 'sgperc','foperc','gaa','svsperc'

DATA_MAP = {}
for i in INTEGERS:
    DATA_MAP[i] = integer_or_none
for f in FLOATS:
    DATA_MAP[f] = float_or_none




class RowDataMixin:
    __slots__ = ()

    @property
    def splitname(self):
        '''Returns a tuple of lastame, firstname for a given player'''
        lastname, firstname = map(lambda x:x.strip().replace("*",""), self.name.split(","))
        return (lastname, firstname)  

    @property
    def playerid(self):
        name = u":".join(self.name).lower()
        s = u":".join((str(self.no), name))
        return hash(s)


 

class SkaterStatsRow(RowDataMixin, namedtuple("SkaterStatsRow", SKATERSSTATS_COLUMNS)):
    __slots__ = ()


class GoalieStatsRow(RowDataMixin, namedtuple("GoalieStatsRow", GOALIESTATS_COLUMNS)):
    __slots__ = ()

    @property
    def minutes_in_play(self):
        if ':' in self.mip:
            minutes, seconds = self.mip.split(':')
            return datetime.timedelta(minutes=int(minutes), seconds=int(seconds))


class TeamRosterRow(RowDataMixin,namedtuple("TeamRosterRow", TEAMROSTER_COLUMNS)):
    __slots__ = ()  
    
    @property
    def countrycode(self):
        c = self.country
        if len(c) >= 3:
            return c[0:3]  

    @property            
    def dateofbirth(self):
        dt = datetime.datetime.strptime(self.dob, "%Y-%m-%d")
        return datetime.date(dt.year, dt.month, dt.day)



"""

TABLES


"""
class AbstractShlTable:

    rowdata = None

    def __init__(self, soup):
        self.soup = soup


    def get_teamnames(self):
        '''Returns tuple of team ID and team NAME from the navigation menu above the tables'''
        all_anchors = self.soup.find(id="headerLinks").find_all("a")
        return [(a['href'][1:], a.string) for a in all_anchors ]

    def gettablerows(self, table):
        '''Returns table rows, skipping headers'''
        return table.find_all("tr")[3:]

    def gettable(self, team):
        '''Returns team table'''
        return self.soup.find(id=team).next_sibling

    def read(self):

        for team_id, team_name in self.get_teamnames():
            
            team_table = self.gettable(team_id)
            table = team_table.find("table", class_="tblContent")

            for tr in self.gettablerows(table):
                
                s = [team_name] + [u"".join(td.stripped_strings) for td in tr.find_all("td")]                

                data = [DATA_MAP.get(k,unicode)(v) for k,v in zip(self.colnames,s)]
                    
                yield self.rowdata._make(data)


    def __iter__(self):
        return self.read()

    def fetch(self):
        return list(self)

    @property
    def colnames(self):
        return self.rowdata._fields



class SkatersStatsTable(AbstractShlTable):
    rowdata = SkaterStatsRow


class GoalieStatsTable(AbstractShlTable):
    rowdata = GoalieStatsRow

    def gettable(self, team):
        skaters_table = self.soup.find(id=team)
        goalie_table = skaters_table.find_next_siblings("table")[1]
        return goalie_table

    def gettablerows(self, table):
        '''Returns table rows, skipping headers'''
        return table.find_all("tr")[2:]


class TeamRostersTable(AbstractShlTable):
    rowdata = TeamRosterRow

    def gettablerows(self, table):
        return table.find_all("tr")[3:-2]




def default_loader(url):
    '''Loads HTML from the given URL'''
    try:
        response = urllib2.urlopen(url)
        content = response.read()
        return content
    except:
        raise SweHockeyException("Could not load {}".format(url))



class SHLPageReader(object):
    def __init__(self, league_id, loader=default_loader):
        url = self.url.format(league_id)
        html = loader(url)
        self.soup = BeautifulSoup(html)


class TeamStatsReader(SHLPageReader):
    url = PLAYERSBYTEAM_URL

    @property
    def skaters(self):
        return SkatersStatsTable(self.soup)
    
    @property
    def goalies(self):
        return GoalieStatsTable(self.soup)


class RostersReader(SHLPageReader):
    url = ROSTER_URL

    @property
    def players(self):
        return TeamRostersTable(self.soup)




def main():

    import sys
    import csv
    import itertools
    
    if len(sys.argv) < 2:
        raise SystemExit("Expected one or many swehockey league ids, e.g. 3905 3906")

    leagues = sys.argv[1:]        
    writer = csv.writer(sys.stdout)

    def asutf8(v): return unicode(v).encode('utf-8')
    
    for league in leagues:

        swe_reader = TeamStatsReader(league)

        skaters = swe_reader.skaters
        goalies = swe_reader.goalies

                
        for p in itertools.chain(skaters, goalies):
            writer.writerow([asutf8(v) for v in list(p)])



if __name__ == '__main__':
    main()