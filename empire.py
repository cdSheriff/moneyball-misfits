## SEE RESULTS BELOW




# METHOD:
# 1. make a DataFrame (empire) of the league members and their favorite team. If multiple members like the same team, they are RANDOMLY ASSIGNED a team for their empire foundation. ITS RANDOM. NO COLLUSION.
# 2. Import the stadium location CSV to get the team names
# 3. make two lists; one with the members needing a team, and another with the remaining teams
# 4. use random.choice (why random.choice? because it is easy. It is cryptographically secure or some shit like that? No. Kick rocks, fate stuck you with the Buffalo Bills) to align a league member with a team. Assign this team name to the league member in the empire DataFrame. Iterate through the league member list until they are all gone.
# 5. Reveal results to the league and face endless criticism

import pandas as pd
import numpy as np
import csv
import random

# 1. create the empire DataFrame with the league members and their favorite teams
name = ['Nesty', 'Sean', 'Uke', 'Blake', 'Aleck', 'Bryce', 'Jimbo', 'Kyle', 'Will', 'John', 'Sheriff', 'Jacob']
team = ['LAR', 'NE', 'NYJ', 'OAK', 'MIN', 'PIT', 'KC', 'CHI', 'WAS', 'MIA', 'PHI', 'LAC']
empire = pd.DataFrame(columns = ['name', 'team'], index = name)
empire['name'] = name
# empire.loc[0:len(team), 'team'] = team
empire['team'] = team

# # 2. get team list
# stadiums = pd.DataFrame.from_csv('STADIUMS.csv')
# stadiums['team'] = stadiums.index.values.tolist()

# # 3. make list of league members needing a randomly assigned team
# teamless = empire[empire['team'].isnull()].index.values.tolist()

# # 3. make list of teams to draw from
# taken = empire['team'].tolist()
# taken = [x for x in taken if isinstance(x, basestring) == True]
# leftovers = stadiums.index.values.tolist()
# leftovers = [x for x in leftovers if x not in taken]

# # 4. randomly draw teams and members to finish the empire DataFrame
# while len(teamless) > 0:
#     person = teamless.pop(teamless.index(random.choice(teamless)))
#     city = leftovers.pop(leftovers.index(random.choice(leftovers)))
#     empire.loc[person, 'team'] = city

# 5. Read it and weep
print empire