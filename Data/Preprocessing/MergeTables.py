import numpy as np
import pandas as pd

# import data
posic = pd.read_csv("Positions.csv", usecols=['Player','PosicAbbrev'])
NBA =pd.read_csv("nba-2015-2016-regular-season.csv")


## Joining NBA X posic only to get the conflits
# Join dataSets according to Player
df = NBA.set_index('Player').join(posic.set_index('Player')).reset_index()

# looking for conflicts
conflits2 = df.loc[~df.loc[:,'PosicAbbrev'].isin((' PG',' SG',' PF',' C',' SF')),('Player')]
conflits2.sort_values(inplace=True)
conflits2 = conflits2.reset_index()['Player']


## Joining posic X NBA only to get the conflits
df = posic.set_index('Player').join(NBA.set_index('Player')).reset_index()
df.head()
conflits = df.loc[~(df.loc[:,'AGE'] >= 0),('Player')]
conflits.sort_values(inplace=True)
conflits = conflits.reset_index()['Player']

# Creating a aka table
aka = pd.DataFrame()
aka['NBA'] = conflits
aka['Pos'] = conflits2

aux = aka.loc[6,'Pos']
aka.loc[6,'Pos'] = aka.loc[8,'Pos']
aka.loc[8,'Pos'] = aka.loc[7,'Pos']
aka.loc[7,'Pos'] = aux
df = NBA

# Correcting conflicts based on the AKA table
for i in aka.index:
    df.loc[df['Player'] == aka.loc[i,'Pos'],'Player'] = aka.loc[i,'NBA']

# Finally... do the join
df = df.set_index('Player').join(posic.set_index('Player')).reset_index()

# Export data 
df.to_csv("../NBA-data-With-Positions.csv")