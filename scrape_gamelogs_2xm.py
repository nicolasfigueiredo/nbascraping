import requests
from urllib.request import urlopen
import pandas as pd

fourfactors_df = pd.read_csv('fourfactors_14_15_2xm.csv')
gameID_list = [i + 21400000 for i in range(249, 1210)]

url_template = 'http://stats.nba.com/stats/boxscoresummaryv2?GameID=00{gameID}'

team_index = {'1610612737': 0, '1610612738': 1, '1610612751': 2, 
				'1610612766': 3, '1610612741': 4, '1610612739': 5,
				'1610612742': 6, '1610612743': 7, '1610612765': 8,
				'1610612744': 9, '1610612745': 10, '1610612754': 11,
				'1610612746': 12, '1610612747': 13, '1610612763': 14,
				'1610612748': 15, '1610612749': 16, '1610612750': 17,
				'1610612740': 18, '1610612752': 19, '1610612760': 20,
				'1610612753': 21, '1610612755': 22, '1610612756': 23,
				'1610612757': 24, '1610612758': 25, '1610612759': 26,
				'1610612761': 27, '1610612762': 28, '1610612764': 29}

month_index = {'12': 3, '01': 4, '02': 5, '03': 6, '04': 7}

main_df = pd.DataFrame()

for game in gameID_list:

	url = url_template.format(gameID = str(game))
	response = requests.get(url)
	headers = response.json()['resultSets'][5]['headers']
	data = response.json()['resultSets'][5]['rowSet']

	game_df = pd.DataFrame(data, columns = headers)
	game_df = game_df.drop(game_df.columns[[1,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]], axis=1)

	away_team = str(game_df.TEAM_ID[1])
	home_team = str(game_df.TEAM_ID[0])
	away_pts = str(game_df.PTS[1])
	home_pts = str(game_df.PTS[0])
	date = str(game_df.GAME_DATE_EST[0])

	month = date[5:7]
	day = date[8:10]

	if int(day) > 14:
		multiplier = 1
	else:
		multiplier = 0

	away_index = 60 + team_index[away_team] + 30 * (2*month_index[month] - 6 + multiplier)
	home_index = 60 + team_index[home_team] + 30 * (2*month_index[month] - 6 + multiplier)

	away_series = fourfactors_df.loc[away_index]
	home_series = fourfactors_df.loc[home_index]

	away_series = away_series.rename(index = {'EFG_PCT': 'A_EFG_PCT', 'FTA_RATE': 'A_FTA_RATE',
											'TM_TOV_PCT':'A_TM_TOV_PCT', 'OREB_PCT':'A_OREB_PCT',
											'OPP_EFG_PCT': 'A_OPP_EFG_PCT', 'OPP_FTA_RATE': 'A_OPP_FTA_RATE',
											'OPP_TOV_PCT':'A_OPP_TOV_PCT', 'OPP_OREB_PCT':'A_OPP_OREB_PCT',
											'PACE':'A_PACE', 'OFF_RATING':'A_OFF_RATING', 'DEF_RATING':'A_DEF_RATING'})

	home_series = home_series.rename(index = {'EFG_PCT': 'H_EFG_PCT', 'FTA_RATE': 'H_FTA_RATE',
											'TM_TOV_PCT':'H_TM_TOV_PCT', 'OREB_PCT':'H_OREB_PCT',
											'OPP_EFG_PCT': 'H_OPP_EFG_PCT', 'OPP_FTA_RATE': 'H_OPP_FTA_RATE',
											'OPP_TOV_PCT':'H_OPP_TOV_PCT', 'OPP_OREB_PCT':'H_OPP_OREB_PCT',
											'PACE':'H_PACE','OFF_RATING':'H_OFF_RATING', 'DEF_RATING':'H_DEF_RATING'})

	game_series = away_series.append(home_series)
	game_series = game_series.drop(['W', 'L', 'Unnamed: 0', 'GP', 'W_PCT', 'MIN', 'CFID', 'CFPARAMS'])

	game_score = {'A_PTS': away_pts, 'H_PTS': home_pts, 'DATE': date}
	game_score = pd.Series(game_score)

	game_series = game_series.append(game_score)

	final_df = pd.DataFrame(game_series)
	final_df = final_df.T

	main_df = main_df.append(final_df, ignore_index = True)

	loading = 'Done game ' + str(game-21400248) + ' of 984.'
	print(loading)

main_df.to_csv('final_data_2xm_14_15.csv')
print('Done.')