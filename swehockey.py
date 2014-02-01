#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''swehockey.py

Python module for readings stats tables from swehockey.se

Every league is identifies with a league ID, which is found at the stats.swehockey.se web site. 
For example, 3905 is SHL, the Swedish Hockey League. 


Example usage:

for r in rosters(3905):
    print r


for r in playersbyteam(3905):
    print r



'''

__author__  = "Peter N Stark"


from collections import namedtuple
from urllib2 import urlopen
from lxml import etree
import itertools
import hashlib



PLAYERSBYTEAM_URL = "http://stats.swehockey.se/Teams/Info/PlayersByTeam/{}"
ROSTER_URL = "http://stats.swehockey.se/Teams/Info/TeamRoster/{}"


def get_html_page(url):
    '''Returns the HTML page at the URL as a unicode string''' 
    response = urlopen(url)
    content = response.read()
    return content.decode('utf-8')#We use Unicode internally 


'''Data


'''

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


def countrycode(v):
    '''Returns the 3-letter country code'''
    if len(v) >= 3:
        return v[0:3]  



INTEGERS = 'rk','no','gp','g','a','tp','pim','plus','minus','plusminus','gwg','ppg','shg','sog','foplus','fominus','fo','weight','height','gpt','gkd','gpi','ga','svs','sog','so','w','l'
FLOATS = 'sgperc','foperc','gaa','svsperc'


DATA_MAP = {}
for i in INTEGERS:
    DATA_MAP[i] = integer_or_none
for f in FLOATS:
    DATA_MAP[f] = float_or_none
DATA_MAP['nationalityclub'] = countrycode


def datamapper(rowdata):
    return tuple([DATA_MAP.get(k,unicode)(v) for k,v in rowdata])



TABLES = {
    'playingstatistics' : (2,None),
    'goalkeepingstatistics' : (1,None),
    'teamroster' : (2,-2),
    'teamofficials' : (1,None)
}


def get_columnname(element):
    return stringify(element).strip().replace("\n", "").replace("+","plus").replace("-","minus").replace("/","").replace("%","perc").replace(" ", "").lower()


def stringify(element):
    '''Concatenates all text in the subelements into one string'''
    return u"".join([x for x in element.itertext()])


def get_tabletype(element):
    '''Retrieves the table's subtitle as the name of the table type'''
    subtitle = element.find(".//th[@class='tdSubTitle']")
    return subtitle.text.strip().replace(" ","").lower()


def readrows(doc):

    for table in doc.findall(".//table[@class='tblContent']"):
    
        #Team name
        title = table.find(".//th[@class='tdTitle']")
        if title is not None:
            team = title.text

        #Rows    
        rows = list(table.findall(".//tr")) 


        #Detect table table
        table_type = get_tabletype(table)        
        
        #Where data rows starts, ends
        start = TABLES[table_type][0]
        end  = TABLES[table_type][1]
        
        #Column names
        colnames = []
        colnames.append('team')
        colnames.extend(map(get_columnname, rows[start].findall(".//th[@class='tdHeader']"))) 

                
        RowdataTuple = namedtuple(table_type.capitalize(), colnames)

        #Ahh...data
        for row in rows[start+1:end]:  
            s = []
            s.append(team)      
            s.extend(map(stringify, row.findall(".//td")))

            data = datamapper(zip(colnames, s)) 
            
            yield RowdataTuple(*data)




def parse(content):
    '''Parses the content into an etree and return a readrows iterator'''
    parser = etree.HTMLParser()
    doc = etree.fromstring(content, parser)        
    return readrows(doc)


def playersbyteam(league_id, loader=get_html_page):
    content = loader(PLAYERSBYTEAM_URL.format(league_id))
    return parse(content)


def rosters(league_id, loader=get_html_page):
    content = loader(ROSTER_URL.format(league_id))
    return parse(content)



def skaterstats(league_id):
    '''Iterates over all skaters and returns the following value as a tuple:
    team, name, gp, g, a, tp, pim, plusminues'''

    for player in playersbyteam(league_id):
        if type(player).__name__ == "Playingstatistics":
            yield player


def goaliestats(league_id):
    '''Iterates over all goalies and returns the following value as a tuple:
    team, name, gp, gaa'''

    for player in playersbyteam(league_id):
        if type(player).__name__ == "Goalkeepingstatistics":
            yield player



class Rosters:
    def __init__(self, league_id):
        self.players = {p.name : p for p in rosters(league_id)}

    def find_players(self, name):
        '''Returns list of players with matching name. Can be empty''' 
        return [self.players[p] for p in self.players if name==p]



if __name__ == '__main__':
    import argparse
    import csv
    import sys

    STATS_READERS = {'skaters' : skaterstats,'goalies' : goaliestats}

    parser = argparse.ArgumentParser(description='Get player stats from swehockey.se and write CSV file') 
    parser.add_argument("-l", "--league", help="The league ID from swehockey.se", action="store", dest="league")
    parser.add_argument("-p", "--players", action="store", choices={'skaters', 'goalies'}, help="Skaters or Goalies")
    parser.add_argument(dest="output", nargs="+", help="The list of attributes to write, e.g. name, gp, gaa")
    parser.add_argument("--header", action="store_true", help="Write header row")
    args = parser.parse_args()

    writer = csv.writer(sys.stdout)

    if args.header:
        writer.writerow(args.output)

    for player in STATS_READERS[args.players](args.league):
        attribs = player._asdict()
        try:
            row = [unicode(attribs[attrib]).encode('utf-8') for attrib in args.output]
        except KeyError as e:
            raise SystemExit("Unknown key : {}".format(e))
        writer.writerow(row)



