import numpy as np
import pandas as pd
import plotly as py
import plotly.graph_objs as go
import json, ConfigParser
from scipy import stats


config = ConfigParser.ConfigParser()
config.read('{0}/.python_keys.conf'.format(os.path.expanduser("~")))
py.tools.set_credentials_file(username=config.get('plotly','un'), api_key=config.get('plotly','pw'))

#  helpful: http://www.danielforsyth.me/exploring_nba_data_in_python/

# get lineups
with open('/home/jason/nba_lineup/raw/nba_lineup_2016_17.json') as data_file:    
    data = json.load(data_file)
headers = data['resultSets'][0]['headers']
lineupdata = data['resultSets'][0]['rowSet']
lineup_df = pd.DataFrame(lineupdata,columns=headers) 

# get individual
with open('/home/jason/nba_lineup/raw/nba_general_2015_16.json') as data_file:    
    data = json.load(data_file)
headers = data['resultSets'][0]['headers']
inddata = data['resultSets'][0]['rowSet']
ind_df = pd.DataFrame(inddata,columns=headers) 

lineup_df[['p1','p2','p3','p4','p5']] = lineup_df['GROUP_ID'].apply(lambda x:pd.Series(x.split(' - ')))
lineup_df[['p1','p2','p3','p4','p5']] = lineup_df[['p1','p2','p3','p4','p5']].apply(pd.to_numeric)


# starts with 250 lineups.
lineup_df = lineup_df.merge(ind_df[['PLAYER_ID','PIE']],left_on='p1',right_on='PLAYER_ID',suffixes=('', '_a'))
lineup_df = lineup_df.merge(ind_df[['PLAYER_ID','PIE']],left_on='p2',right_on='PLAYER_ID',suffixes=('', '_b'))
lineup_df = lineup_df.merge(ind_df[['PLAYER_ID','PIE']],left_on='p3',right_on='PLAYER_ID',suffixes=('', '_c'))
lineup_df = lineup_df.merge(ind_df[['PLAYER_ID','PIE']],left_on='p4',right_on='PLAYER_ID',suffixes=('', '_d'))
lineup_df = lineup_df.merge(ind_df[['PLAYER_ID','PIE']],left_on='p5',right_on='PLAYER_ID',suffixes=('', '_e'))
# finish with only 179.
lineup_df['AVG_PIE'] = (lineup_df['PIE_a']+lineup_df['PIE_b']+lineup_df['PIE_c']+lineup_df['PIE_d']+lineup_df['PIE_e'])/5



### scatterplot
slope, intercept, r_value, p_value, std_err = stats.linregress(lineup_df['AVG_PIE'],lineup_df['OFF_RATING'])
line = slope*lineup_df['AVG_PIE']+intercept

trace1 = go.Scatter(y=lineup_df['OFF_RATING'],
    x=lineup_df['AVG_PIE'],
    text=lineup_df['GROUP_NAME'], 
    mode='markers',
    marker = dict(size=np.log(lineup_df['MIN']*2),
        #colorbar = dict(title = "Previous Wins"),
        color=lineup_df['MIN'],colorscale='Viridis',showscale=True),name='Minutes')
trace2 = go.Scatter(
                  x=lineup_df['AVG_PIE'], 
                  y=line, 
                  mode='lines',
                  marker=go.Marker(color='rgb(31, 119, 180)'),
                  name='Fit',
                  showlegend=False
                  )
data = [trace1,trace2]
        
layout = go.Layout(title='Individual and Lineup Offensive Performance',yaxis=dict(title='Lineup Offensive Rating',zeroline=False),xaxis=dict(title='Individual Avg PIE'))
fig = go.Figure(data=data, layout=layout)
plot_url = py.plotly.plot(fig, filename='nba_lineup',sharing='public')    
    









