import os
import shutil
import sys
import time
import json
import requests

datapath = 'C:\\Users\\Administrator\\Desktop\\kdj基线策略组\\date\\'
kdjpath = 'C:\\Users\\Administrator\\Desktop\\kdj基线策略组\\kdj\\'
def removedir(filepath):
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)
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
print(tday())
if tday() == "1" :
    if dphq() == 1 :
        removedir(datapath)
        removedir(kdjpath)
        time.sleep(60)
        os.system("python.exe C:\\Users\\Administrator\\Desktop\\kdj基线策略组\\loaddate.py")
        time.sleep(60)
        os.system("python.exe C:\\Users\\Administrator\\Desktop\\kdj基线策略组\\kdjcer.py")
        time.sleep(60)
        fileName = 'C://Users//Administrator//Desktop//web//www//root//127.0.0.1//kdj.html'
        today = time.strftime("%Y-%m-%d")
        print(today)
        with open(fileName, 'a+') as file:
            file.write("<h2>"+today+"号指数命中策略，数据已更新</h2>")
            print(today)
    else :
        fileName = 'C://Users//Administrator//Desktop//web//www//root//127.0.0.1//kdj.html'
        today = time.strftime("%Y-%m-%d")
        with open(fileName, 'a+') as file:
            file.write("<h2>" + today + "号未触发策略</h2>")
else :
    fileName = 'C://Users//Administrator//Desktop//web//www//root//127.0.0.1//kdj.html'
    today = time.strftime("%Y-%m-%d")
    with open(fileName, 'a+') as file:
        file.write("<h2>" + today + "号非交易日</h2>")
