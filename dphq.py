# -- coding: utf-8 --**
import requests
import json
def dphq() :
    url = f'https://push2.eastmoney.com/api/qt/ulist/get?fltt=1&invt=2&fields=f3,f14&secids=1.000001,0.399001,1.000300,0.399006,1.000688&pn=1&np=1'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'
    headers = {'User-Agent': user_agent}

    res = requests.get(url,headers=headers)
    jsonobj = json.loads(res.text)
    actpath=0
    for a in jsonobj['data']['diff']:
        if a['f3'] > 0 :
            actpath=actpath+1
    if actpath > 3 :
       ads = 1
    else :
       ads = 0
    return ads ;
print(dphq())