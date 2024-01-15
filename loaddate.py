#!/usr/bin/env python
# coding: utf-8


import requests
import json
import sys
import easyquotation


# 获取正向比的股票

# In[1]:


url ='https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=999999999&po=1&np=1&fltt=2&invt=2&fid0=f4001&fid=f62&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,m:1+t:3+f:!2&stat=1&fields=f184,f12'


# In[6]:


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'
headers = {'User-Agent': user_agent} 


# In[7]:


res = requests.get(url,headers=headers)


# In[14]:


json_obj = json.loads(res.text)


# 如果按照每个股票的历史数据单独输出为一个文件，而正向比的股票大概有1500左右，所以为了减少文件的输出，这里暂定设置为5

# In[49]:


stock_num_lst =[(u['f12'],u['f184'] )for u  in json_obj['data']['diff'] if u['f184'] !='-'and float(u['f184'])>0][:5000]


# 获取股票的历史数据

# In[42]:


import pandas as pd
import time
from datetime import datetime,timedelta



def mix(code,file) :
    quotation = easyquotation.use('sina') # 新浪 ['sina'] 腾讯 ['tencent', 'qq']
    #获取所有股票行情
    quotation.market_snapshot(prefix=True) # prefix 参数指定返回的行情字典中的股票代码 key 是否带 sz/sh 前缀
    #单只股票
    a = quotation.real(code)# 支持直接指定前缀，如 'sh000001'
    name = a[code]["name"]
    high = a[code]["high"]
    low = a[code]["low"]
    now = a[code]["now"]

    fp = open(file)
    lines = []
    for line in fp:
        lines.append(line)
    fp.close()
    today = time.strftime("%Y-%m-%d")
    nr = f" ,{today},2,{now},3,4,{low},{high},7,8,9\n"
    lines.insert(1, nr)  # 在第二行插入
    s = ''.join(lines)
    fp = open(file, 'w')
    fp.write(s)
    fp.close()
# In[51]:

endday = time.strftime("%Y-%m-%d")
print(endday)
startday = time.strftime("%Y-%m-%d")
startday = datetime.strptime(startday, "%Y-%m-%d").date()
# 前推120天 就是 - timedelta(days=120)
target = startday - timedelta(days=120)
a = str(target)
b = a.replace(r'-', '')
today = endday.replace(r'-','')
hist_url=f"https://q.stock.sohu.com/hisHq?code=cn_%s&start={b}&end={today}"

#hist_url='https://q.stock.sohu.com/hisHq?code=cn_%s&start=20230101&end=20230203'


# In[67]:


for stock_dict in stock_num_lst:
    code = stock_dict[0]
    rate = stock_dict[1]
    url = hist_url%(code)
    hist_data_str = requests.get(url,headers=headers).text
    hist_data_json = json.loads(hist_data_str)
    #if hist_data_json[0].findall('hq') :
    if 'hq' in hist_data_json[0]:
        name = str(rate) + "-" + code + '.csv'
        file = "C:\\Users\\Administrator\\Desktop\\kdj基线策略组\\date\\" + name  # date 文件必须要提前建好
        pd.DataFrame(hist_data_json[0]['hq']).to_csv(file)
        mix(code, file)

