## based on the 'College football empire' map, can I do the same thing w/ fantasy football in our league?

"""
Challenges:
1. 6 members are fans of unique teams, 6 are repeats. So we need to randomly assign the remainders
1a. alternatively, everyone gets a random team that is based on equalizing starting area
2. importing FIPS data gives ascii issues, so I have to trim latitude (line 82). This caused issues with Alutian island county, because it is actually in the eastern hemisphere. manually trimmed data in the csv
3. This takes forever. Maximizing area means nCr of 6 people from 26 teams, or 260230 combinations. I got it down to fractions of a second, but that is still hours of thinky time for that many options
4. NO NESTED FOR LOOPS. The distlist takes a couple seconds to make, and makes a giant dataframe. But only has to happen once. Then the combination cruncher can do list comprehension on that instead of doing 32 teams vs 3142 for all 300K combinations
5. Can I reduce the loop time for lines 95-109? Or, reduce the number of iterations it performs? Something has to reduce to make the calculation managable
"""




import pandas as pd
import numpy as np
import csv
import random
import math
import time

def haversine(lat1,lat2,lon1,lon2):
    R = 6371.
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    phi = math.radians(lat2 - lat1)
    lamb = math.radians(lon2 - lon1)
    
    a = (math.sin(phi/2))**2 + math.cos(phi1) * math.cos(phi2) * (math.sin(lamb/2))**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1.-a));
    d = R*c
    return d


# name = ['Nesty', 'Sean', 'Uke', 'Blake', 'Aleck', 'Bryce']
# team = ['LAR', 'NE', 'NYJ', 'OAK', 'MIN', 'PIT']
# name = ['Nesty', 'Sean', 'Uke', 'Blake', 'Aleck', 'Bryce', 'Jimbo', 'Kyle', 'Will', 'John', 'Sheriff', 'Jacob']
# team = ['LAR', 'NE', 'NYJ', 'OAK', 'MIN', 'PIT', 'DEN', 'SEA', 'TB', 'DAL', 'NO', 'KC']
name = ['Nesty', 'Sean', 'Uke', 'Blake', 'Aleck', 'Bryce', 'Jimbo', 'Kyle', 'Will', 'John', 'Sheriff', 'Jacob']
team = ['LAR', 'NE', 'NYJ', 'OAK', 'MIN', 'PIT', 'SEA']

start1 = time.time()
empire = pd.DataFrame(columns = ['name', 'team', 'lat', 'lon', 'area', 'color'], index = team)
empire['name'] = name
empire['team'] = team
empire['area'] = 0
# print empire
stadiums = pd.DataFrame.from_csv('STADIUMS.csv')
stadiums['team'] = stadiums.index.values.tolist()

total = len(empire.index.values.tolist()) + 1.
i = 1
for index, row in empire.iterrows():
    empire.loc[index, 'lat'] = stadiums.loc[row['team'], 'LAT']
    empire.loc[index, 'lon'] = stadiums.loc[row['team'], 'LONG']
    empire.loc[index, 'color'] = stadiums.loc[row['team'], 'color']
    empire.loc[index, 'color_num'] = i
    i += 1
# print empire

landmass = pd.Series(0, index = empire.index.values.tolist())

countyinfo = pd.DataFrame.from_csv('county map.csv')
stadiums = pd.DataFrame.from_csv('STADIUMS.csv')
stadiums['team'] = stadiums.index.values.tolist()
countycondensed = countyinfo.set_index('FIPS')
countycondensed['adjusted'] = ''

for index, row in countycondensed.iterrows():
    area = row['total area mi']
    if ',' in area:
        area = area.replace(',', '')
    area = float(area)
    if row['State'] == 'AK':
        area = 0.15 * area
    countycondensed.loc[index, 'adjusted'] = round(area,0)

# make a big fucking dataframe of distances
coordinates = []
for row in countyinfo.itertuples():
    coordinates.append([float(row[8][1:-2]),-float(row[9][3:-2])])
distlist = pd.DataFrame(index = countyinfo['FIPS'])
for x in stadiums.index.values.tolist():
    lat = stadiums.loc[x,'LAT']
    lon = stadiums.loc[x,'LONG']
    temp = [haversine(lat,y[0],lon,y[1]) for y in coordinates]
    distlist[x] = temp
    
end1 = time.time()    

start2 = time.time()

# drop unused teams from distlist
missing = []
for column in distlist.columns:
    if column not in empire.index.values.tolist():
        missing.append(column)        
shortlist = distlist.drop(missing,1)


# add up land area
minlist = shortlist.idxmin(1)
temp = pd.DataFrame(index = minlist.index)
temp['closest'] = minlist
temp['area'] = countycondensed['adjusted']

for each in team:
    landmass[each] = temp.loc[temp['closest'] == each]['area'].sum()
end2 = time.time()

print(end1 - start1)
print(end2 - start2)
# print(end3 - start3)
# print(end4 - start4)
print landmass