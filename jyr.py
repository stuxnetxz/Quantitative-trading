import requests
import json
import pandas as pd
import time
from datetime import datetime,timedelta
from pandas import DataFrame
def tday() :
    thism = time.strftime("%Y-%m")
    today = time.strftime("%Y-%m-%d")
    url = f'http://www.szse.cn/api/report/exchange/onepersistenthour/monthList?month={thism}'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'
    headers = {'User-Agent': user_agent}
    res = requests.get(url,headers=headers)
    jsonobj = json.loads(res.text)
    for a in jsonobj['data']:
         if a['jyrq'] == today :
            istheday = a['jybz']
    return istheday ;

print(tday())