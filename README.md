The Swehockey Python module
===========================

A Python module for reading player-statistics and rosters from swehockey.se, the official site for swedish hockey statistics. 

The module can be used as a commmand-line tool or as an integrated module in some other program. 



# Command Line Tool
```
usage: swehockey.py [-h] [-l LEAGUE] [-p {skaters,goalies}] [--header]
                    output [output ...]

Get player stats from swehockey.se and write CSV file

positional arguments:
  output                The list of attributes to write, e.g. name, gp, gaa

optional arguments:
  -h, --help            show this help message and exit
  -l LEAGUE, --league LEAGUE
                        The league ID from swehockey.se
  -p {skaters,goalies}, --players {skaters,goalies}
                        Skaters or Goalies
  --header              Write header row
```

For example, to print the team, name and games played (gp) for all players in SHL, you write:

```
$ python swehockey.py -l 3905 -p skaters team name gp
```

Gives the following output:

```
AIK,"Janmark-Nylén, Mattias",36
AIK,"Pirnes, Esa",42
AIK,"Ramstedt, Teemu",36
AIK,"Melin, Björn",25
AIK,"Steen, Oscar",42
AIK,"Liwing, Jonas",43
AIK,"Hurtubise, Mark",45
AIK,"Joslin, Derek",44
AIK,"Ahlström, Oscar",45
```


# Basic Usage 

```python
import swehockey

for row in swehockey.teamstats(3905):
    print row

for row in swehockey.rosters(3905):
    print row

```

Gives the following output:

```
Playingstatistics(team=u'AIK', rk=1, no=26, name=u'Janmark-Nyl\xe9n, Mattias', pos=u'CE', gp=32, g=16, a=9, tp=25, pim=50, plus=18, minus=22, plusminus=-4, gwg=3, ppg=5, shg=1, sog=85, sgperc=18.82, foplus=11, fominus=30, fo=41, foperc=26.83)
Playingstatistics(team=u'AIK', rk=2, no=10, name=u'Pirnes, Esa', pos=u'LW', gp=34, g=9, a=11, tp=20, pim=14, plus=17, minus=25, plusminus=-8, gwg=2, ppg=2, shg=1, sog=54, sgperc=16.67, foplus=198, fominus=223, fo=421, foperc=47.03)
Playingstatistics(team=u'AIK', rk=3, no=46, name=u'Ramstedt, Teemu', pos=u'CE', gp=34, g=6, a=14, tp=20, pim=46, plus=17, minus=26, plusminus=-9, gwg=1, ppg=2, shg=0, sog=47, sgperc=12.77, foplus=288, fominus=364, fo=652, foperc=44.17)
Playingstatistics(team=u'AIK', rk=4, no=91, name=u'Melin, Bj\xf6rn', pos=u'LW', gp=25, g=6, a=13, tp=19, pim=24, plus=12, minus=20, plusminus=-8, gwg=0, ppg=2, shg=0, sog=49, sgperc=12.24, foplus=0, fominus=1, fo=1, foperc=0.0)
Playingstatistics(team=u'AIK', rk=5, no=45, name=u'Steen, Oscar', pos=u'CE', gp=36, g=4, a=13, tp=17, pim=20, plus=16, minus=27, plusminus=-11, gwg=1, ppg=0, shg=0, sog=50, sgperc=8.0, foplus=272, fominus=283, fo=555, foperc=49.01)
Playingstatistics(team=u'AIK', rk=6, no=23, name=u'Liwing, Jonas', pos=u'RD', gp=35, g=3, a=13, tp=16, pim=6, plus=25, minus=33, plusminus=-8, gwg=0, ppg=2, shg=1, sog=46, sgperc=6.52, foplus=0, fominus=0, fo=0, foperc=None)
Playingstatistics(team=u'AIK', rk=7, no=14, name=u'Hurtubise, Mark', pos=u'RW', gp=37, g=11, a=3, tp=14, pim=22, plus=16, minus=26, plusminus=-10, gwg=0, ppg=1, shg=1, sog=76, sgperc=14.47, foplus=142, fominus=163, fo=305, foperc=46.56)
Playingstatistics(team=u'AIK', rk=8, no=25, name=u'Joslin, Derek', pos=u'LD', gp=36, g=4, a=10, tp=14, pim=24, plus=23, minus=32, plusminus=-9, gwg=0, ppg=3, shg=1, sog=82, sgperc=4.88, foplus=0, fominus=0, fo=0, foperc=None)
Pl
```

# Installation

Using PIP:

```
pip install swehockey
```  
