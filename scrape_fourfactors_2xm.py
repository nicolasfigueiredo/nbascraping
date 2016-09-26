import requests
from urllib.request import urlopen
import pandas as pd

url_template =  'http://stats.nba.com/stats/leaguedashteamstats?Conference=&Date'\
				'From={date}&Division=&GameScope=&GameSegment=&LastNGames=0&'\
				'LeagueID=00&Location=&MeasureType=Advanced&Month=0&Oppone'\
				'ntTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Per'\
				'iod=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Se'\
				'ason=2012-13&SeasonSegment=&SeasonType=Regular+Season&ShotClo'\
				'ckRange=&StarterBench=&TeamID=0&VsConference=&VsDivision='

month_list = range(1,4)
input_list = ['11%2F01%2F2012&DateTo=11%2F14%2F2012',
			  '11%2F15%2F2012&DateTo=11%2F28%2F2012',
			  '12%2F01%2F2012&DateTo=12%2F14%2F2012',			  
			  '12%2F15%2F2012&DateTo=12%2F28%2F2012',]

for month in month_list:

	new_input = '0' + str(month) + '%2F01%2F2013&DateTo=0' + str(month) + '%2F14%2F2013'
	input_list.append(new_input)
	new_input = '0' + str(month) + '%2F15%2F2013&DateTo=0' + str(month) + '%2F28%2F2013'
	input_list.append(new_input)

url = url_template.format(date = input_list[1])
response = requests.get(url)
headers = response.json()['resultSets'][0]['headers']
data = response.json()['resultSets'][0]['rowSet']

fourfactors_df = pd.DataFrame(data, columns = headers)

for date in input_list:

	url = url_template.format(date = date)
	response = requests.get(url)
	data = response.json()['resultSets'][0]['rowSet']
	temp_df = pd.DataFrame(data, columns = headers)
	fourfactors_df = fourfactors_df.append(temp_df, ignore_index = True)

print(fourfactors_df.head())

fourfactors_df.to_csv("advanced_12_13_2xm.csv")

print('Done.')