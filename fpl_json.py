import requests
import json
import csv
import time

http_proxy = "http://proxy-jf.intel.com:911"
https_proxy = "https://proxy-jf.intel.com:911"
ftp_proxy = "ftp://proxy-jf.intel.com:911"

proxyDict = {
             "http"  : http_proxy,
             "https" : https_proxy,
             "ftp"   : ftp_proxy
            }

main_url = "https://fantasy.premierleague.com/api/bootstrap-static"
player_url = "https://fantasy.premierleague.com/api/element-summary/"
proxy_check_url = "http://www.google.com"
proxy_required = False
all_detailed = {}
my_team = {}
dreamteam = {}

positions = {1:'GKP', 2:'DEF', 3:'MID', 4:'FWD'}
team = {1:'MUN',
        3:'ARS',
        4:'NEW',
        6:'TOT',
        7:'AVL',
        8:'CHE',
        11:'EVE',
        13:'LEI',
        14:'LIV',
        20:'SOU',
        21:'WHU',
        31:'CRY',
        35:'WBA',
        36:'BHA',
        38:'HUD',
        39:'WOL',
        43:'MCI',
        45:'NOR',
        49:'SHU',
        54:'FUL',
        57:'WAT',
        80:'SWA',
        90:'BUR',
        91:'BOU',
        97:'CAR',
        110:'STK'
        }

def proxyCheck():
    global proxy_required
    try:
        requests.get(proxy_check_url, verify=False, timeout=1)
    except IOError:
        print("Checking with proxy...")
        requests.get(proxy_check_url, proxies=proxyDict, verify=False, timeout=1)
        proxy_required = True

def getAllPlayersDetailedJson():
    global all_detailed
    if proxy_required:
        all_detailed = requests.get(main_url, proxies=proxyDict).json()
    else:
        all_detailed = requests.get(main_url).json()
    with open('AllPlayersDetailed.json', 'w') as f:
        json.dump(all_detailed, f)

def getPlayerJson(p_id):
    if proxy_required:
        return requests.get(player_url+str(p_id), proxies=proxyDict).json()
    else:
        return requests.get(player_url+str(p_id)).json()

def extractDataFromAllDetailed():
    global dreamteam
    print("Processing...")
    for i in all_detailed['elements']:
        if (10 < float(i['influence'])):
            key = i['id']
            p = getPlayerJson(key)['history'][-1]
            print(json.dumps(p, indent=2))
            dreamteam[key] = [i['ict_index'], i['influence'], i['creativity'], i['threat'], i['value_form'],
                              i['web_name'].encode('ascii', 'ignore').decode('ascii'), i['now_cost'],
                              positions.get(i['element_type'], 'default'), team.get(i['team_code'], 'default'),
                              i['minutes'], i['bps'], i['points_per_game'], i['event_points'], i['chance_of_playing_this_round'],
                              p['was_home'], i['clean_sheets'], i['assists']]

def writeToCsv():
    top_row = ['Id', 'ict-index', 'influence', 'creativity', 'threat', 'value_form', 'web_name', 'now_cost',
               'position', 'team', 'minutes', 'bps', 'points-per-game', 'points-last-game', 'playing-chance',
               'was_home', 'clean_sheets', 'assists']
    timestr = time.strftime("%Y%m%d-%H%M%S")
    with open(timestr+'.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(top_row)
        for key, value in dreamteam.items():
            writer.writerow([key] + value)

def main():
    proxyCheck()
    getAllPlayersDetailedJson()
    print(json.dumps(all_detailed, indent=2))
    extractDataFromAllDetailed()
    writeToCsv()

if __name__ == '__main__':
    main()
