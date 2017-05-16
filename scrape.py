import requests
from urllib import urlencode
import json
import sys
import os
import time

API_KEY="6951CC04045EEBA78C54D9855DD26EBB"

HISTORY_URI="https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?"
DETAILS_URI="https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?"

ROOT = os.path.dirname(os.path.realpath(__file__))
OUT_DIR = os.path.join(ROOT, 'matches')

PLAYERSFILE = os.path.join(ROOT, 'players.txt')
MAX_DOS = 3

players = []
with open(PLAYERSFILE) as pf:
    for line in pf:
        line = line.strip()
        if line:
            players.append(line)

acc_id, dos = players.pop(0).split(',')

r = requests.get(HISTORY_URI + urlencode({'key': API_KEY, 'account_id':acc_id})).text
history = json.loads(r)
if 'result' not in history:
    sys.exit(0)
if 'matches' in history['result']:
    for m in history['result']['matches']:
        if len(m['players']) == 10:
            time.sleep(1)
            data = requests.get(DETAILS_URI + urlencode({'key': API_KEY, 'match_id': m['match_id']})).text
            with open(os.path.join(OUT_DIR, str(m['match_id']) + '.json'), 'w') as f:
                f.write(data)

            try:
                next_dos = int(dos) + 1
                if next_dos <= MAX_DOS:
                    jsondata = json.loads(data)
                    for pl in [p['account_id'] for p in jsondata['result']['players']]:
                        if pl not in players:
                            players.append(','.join([str(pl), str(next_dos)]))
            except:
                print("Error scraping match:", m['match_id'])
                continue

players.append(','.join([acc_id, dos]))

with open(PLAYERSFILE, 'w+') as pf:
    for pl in players:
        pl = pl.strip()
        if pl:
            pf.write(pl + '\n')
