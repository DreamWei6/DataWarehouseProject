import configparser
import requests
import json
import time
import csv

def SettingConfig():
	config = configparser.ConfigParser()
	config.read('config.ini')
	return config

def Write2File(csvfile, datalist):
	with open(csvfile, 'a') as output:
		temp = ','.join([str(data) for data in datalist])
		output.write(temp + '\n')
	
def CurrentTime():
	t = time.localtime()
	current_time = time.strftime("%H:%M:%S", t)
	print(current_time)

def main():
	config = SettingConfig();
	schedules = [item[1] for item in config.items('Schedule')]
	#print(schedules)

	Write2File(config['CSV']['output_path'], ['Date', 'GameType', 'AwayScore', 'AwayTeam', 'HomeScore', 'HomeTeam', 'VenueName', 'AwayHR', 'HomeHR'])

	for schedule in schedules:
		url = 'https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate=' + schedule.split(',')[0] + '&endDate=' + schedule.split(',')[1] + '&gameType=R&&gameType=D&&gameType=W&&gameType=L&hydrate=homeRuns'

		try:
			r = requests.get(url)
			data = json.loads(r.text)
		except:
			time.sleep(5)
			r = requests.get(url)
			data = json.loads(r.text)

		get_list = ['Date', 'GameType', 'AwayScore', 'AwayTeam', 'HomeScore', 'HomeTeam', 'VenueName', 'AwayHR', 'HomeHR']
		teamHomeRuns = [0,0]

		print(data['totalGames'])

		for date in data['dates']:
			#print(date['date'])
			get_list[0] = date['date']
			for game in date['games']:
				#print(game['seriesDescription'])
				get_list[1] = game['seriesDescription']
				if game['status']['codedGameState'] == 'F':
					#print(game['teams']['away']['score'],game['teams']['away']['team']['name'])
					#print(game['teams']['home']['score'],game['teams']['home']['team']['name'])
					#print(game['venue']['name'])
					get_list[2] = game['teams']['away']['score']
					get_list[3] = game['teams']['away']['team']['name']
					get_list[4] = game['teams']['home']['score']
					get_list[5] = game['teams']['home']['team']['name']
					get_list[6] = game['venue']['name']
					
					teamHomeRuns = [0,0]
					try:
						for homeRun in game['homeRuns']:
							if homeRun['about']['halfInning'] == 'top':
								teamHomeRuns[0] += 1
							elif homeRun['about']['halfInning'] == 'bottom':
								teamHomeRuns[1] += 1
					except KeyError:
						pass

					get_list[7] = teamHomeRuns[0]
					get_list[8] = teamHomeRuns[1]
					
					Write2File(config['CSV']['output_path'], get_list)

if __name__== "__main__":
	CurrentTime()
	main()
	CurrentTime()