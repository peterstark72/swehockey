#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''swehockey.py



Example usage:



'''


__author__  = "Peter N Stark"


from lxml import etree
import datetime

from collections import namedtuple


PLAYERSBYTEAM_URL = "http://stats.swehockey.se/Teams/Info/PlayersByTeam/{}"
ROSTER_URL = "http://stats.swehockey.se/Teams/Info/TeamRoster/{}"



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

def minutes_in_play(v):
    if ':' in v:
        minutes, seconds = v.split(':')
        return datetime.timedelta(minutes=int(minutes), seconds=int(seconds))

def countrycode(v):
    if len(v) >= 3:
        return v[0:3]  

def dateofbirth(v):
    dt = datetime.datetime.strptime(v, "%Y-%m-%d")
    return datetime.date(dt.year, dt.month, dt.day)


INTEGERS = 'rk','no','gp','g','a','tp','pim','plus','minus','plusminus','gwg','ppg','shg','sog','foplus','fominus','fo','weight','height','gpt','gkd','gpi','ga','svs','sog','so','w','l'
FLOATS = 'sgperc','foperc','gaa','svsperc'


DATA_MAP = {}
for i in INTEGERS:
    DATA_MAP[i] = integer_or_none
for f in FLOATS:
    DATA_MAP[f] = float_or_none

DATA_MAP['mip'] = minutes_in_play
DATA_MAP['birthdate'] = dateofbirth
DATA_MAP['nationalityclub'] = countrycode


def textmapper(rowdata):
    return tuple([unicode(v) for k,v in rowdata])

def datamapper(rowdata):
    return tuple([DATA_MAP.get(k,unicode)(v) for k,v in rowdata])


mapper = datamapper


tables = {
    'playingstatistics' : (2,None),
    'goalkeepingstatistics' : (1,None),
    'teamroster' : (2,-2),
    'teamofficials' : (1,None)
}



def cleanup_column_name(element):

    return stringify(element).strip().replace("\n", "").replace("+","plus").replace("-","minus").replace("/","").replace("%","perc").replace(" ", "").lower()


def stringify(element):
    return u"".join([x for x in element.itertext()])


def get_tabletype(element):
    subtitle = element.find(".//th[@class='tdSubTitle']")
    return subtitle.text.strip().replace(" ","").lower()



def readstats(doc):

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
        start = tables[table_type][0]
        end  = tables[table_type][1]
        
        #Column names
        colnames = []
        colnames.append('team')
        colnames.extend(map(cleanup_column_name, rows[start].findall(".//th[@class='tdHeader']"))) 

                
        RowdataTuple = namedtuple(table_type.capitalize(), colnames)

        #Ahh...data
        for row in rows[start+1:end]:  
            s = []
            s.append(team)      
            s.extend(map(stringify, row.findall(".//td")))

            data = mapper(zip(colnames, s)) 
            
            yield RowdataTuple(*data)



def read(url):
    parser = etree.HTMLParser()
    doc = etree.parse(url, parser)    
    return readstats(doc)


def teamstats(league_id):
    url = PLAYERSBYTEAM_URL.format(league_id)
    return read(url)


def rosters(league_id):
    url = ROSTER_URL.format(league_id)
    return read(url)



def main():

    for r in teamstats(3905):
        print r

    for r in rosters(3905):
        print r





if __name__ == '__main__':
    main()