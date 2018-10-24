import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

base = pd.DataFrame.from_csv('2018 stats.csv')
score = base[0:12]
projected = base[12:24]
comp = base[24:]
change = score - projected


# points against
against = pd.DataFrame(index = score.index)

for j in range(len(score.columns)):
    temp = []
    title = 'week' + str(j + 1)
    for i in range(len(score)):
        opp = int(comp.iloc[i,j])
        temp.append(round(score.iloc[opp,j],2))
    against[title] = temp
        
pa = pd.Series()
pa = against.T.mean()
pa.sort_values(inplace = True)


# deviation from projected
less = pd.DataFrame(index = change.index)

for j in range(len(change.columns)):
    temp = []
    title = 'week' + str(j + 1)
    for i in range(len(change)):
        opp = int(comp.iloc[i,j])
        temp.append(round(change.iloc[opp,j],2))
    less[title] = temp
        
dp = pd.Series()
dp = less.T.mean()
dp.sort_values(inplace = True)



# deviation from mean
avgs = score.T.mean()
    
off = pd.DataFrame(index = score.index)

for j in range(len(score.columns)):
    temp = []
    title = 'week' + str(j + 1)
    for i in range(len(score)):
        opp = int(comp.iloc[i,j])
        temp.append(round(score.iloc[opp,j] - avgs.iloc[opp],2))
    off[title] = temp
        
dm = pd.Series()
dm = off.T.mean()
dm.sort_values(inplace = True)



fig, (axarr0, axarr1, axarr2) = plt.subplots(3, figsize = (12,10))


x0 = pa.index
y0 = pa.tolist()
sns.barplot(x0, y0, palette="rocket", ax=axarr0)
x1 = dp.index
y1 = dp.tolist()
sns.barplot(x1, y1, palette="rocket", ax=axarr1)
x2 = dm.index
y2 = dm.tolist()
sns.barplot(x2, y2, palette="rocket", ax=axarr2)

axarr0.set_title('Points against')
axarr1.set_title('Deviation from projected')
axarr2.set_title('Deviation from mean')

plt.show()