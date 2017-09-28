import requests
import eventlet
import json
from pprint import pprint
import operator
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

main_url = "https://fantasy.premierleague.com/drf/bootstrap-static"
proxy_check_url = "http://www.google.com"
proxy_required = False
all_detailed = {}
my_team = {}
dreamteam = {}

def proxyCheck():
    global proxy_required
    try:
        requests.get(proxy_check_url, verify=False, timeout=1)
    except IOError:
        print "Checking with proxy..."
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

def extractDataFromAllDetailed():
    global all_detailed
    global dreamteam
    for i in all_detailed['elements']:
        if (10 < float(i['influence'])):
            result = i['id']
            dreamteam[result] = [ i['ict_index'], i['influence'], i['creativity'], i['threat'], i['value_form'],
                                  i['web_name'].encode('ascii', 'ignore').decode('ascii'), i['now_cost'],
                                  i['minutes'], i['bps'], i['points_per_game'], i['chance_of_playing_this_round']]

def writeToCsv():
    global dreamteam
    top_row = ['Id', 'ict-index', 'influence', 'creativity', 'threat', 'value_form', 'web_name', 'now_cost', 'minutes', 'bps', 'points-per-game', 'playing-chance']
    timestr = time.strftime("%Y%m%d-%H%M%S")
    with open(timestr+'.csv', 'wb') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(top_row)
        for key, value in dreamteam.items():
            writer.writerow([key] + value)

def main():
    proxyCheck()
    getAllPlayersDetailedJson()
    #print(json.dumps(all_detailed, indent=2))
    extractDataFromAllDetailed()
    writeToCsv()

if __name__ == '__main__':
    main()
