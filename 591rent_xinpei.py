#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import urllib3
import json
import re
from pprint import pprint
from elasticsearch import Elasticsearch
import sys


# In[5]:


#換頁用
xin_api = 'https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region=3&firstRow='

#將需求欄位存成list
linkman =[]
nick_name = []
house_attr =[]
house_phone = []
house_now = []
house_gender =[]


#Cookie 與 X-CSRF-TOKEN 每次都要更換
for i in range(285):
    print("第{}筆".format(i))
    i = i*30
    headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': 'webp=1; PHPSESSID=18gpf6tnp8vtphricesv8m5cq1; urlJumpIp=1; urlJumpIpByTxt=%E5%8F%B0%E5%8C%97%E5%B8%82; T591_TOKEN=18gpf6tnp8vtphricesv8m5cq1; c10f3143a018a0513ebe1e8d27b5391c=1; _ga=GA1.3.693502838.1572961606; _gid=GA1.3.492385046.1572961606; _gat=1; _ga=GA1.4.693502838.1572961606; _gid=GA1.4.492385046.1572961606; _dc_gtm_UA-97423186-1=1; _gat_UA-97423186-1=1; XSRF-TOKEN=eyJpdiI6InFTZ25EeVwvTm42ZVNSRGw5YnJOUlwvQT09IiwidmFsdWUiOiJyM3NHOG85XC9SVlNlVVFDMjA0bHdwazZDRnJYV3hRR2tmTnFLR09Ob1NVU2pMdnVJdzA4NStiWGQ4ZGI3UFdVaThybzJ0NUVQa2c2dDI1MzdISjhQblE9PSIsIm1hYyI6IjNhNDZmYTNmMTI4ZGY3NDM3MDJmMDMyNDM3NWU5MTNjOWRhNDkyMTBkM2M4MmJjZmE5ZDJkYTFlYjRkNDRkY2MifQ%3D%3D; _fbp=fb.2.1572961609675.2041252944; new_rent_list_kind_test=0; 591_new_session=eyJpdiI6IkxnNlY3U0gzVHdWS0J2Y1pYK1d2bEE9PSIsInZhbHVlIjoiWHBranNhUEN1Q2hjYTVZV3pwak1lZ041UTZVSHdcL1ExdFlMQkhJU2JrV2VScDQ3SEphQVpoenJuclF6VHZQZjVvbG9CdzMzNU1BSlNnSm5MbGdEV0dRPT0iLCJtYWMiOiIwODc0MzE1ZmQ2NTk2ZGU2NDczOTg5ZDllOTEwNTgwNGI3MjdlOGRiYWY3NDc0ZDY5ZTU0N2U4NmQyNjkwMjY5In0%3D',
        'Host': 'rent.591.com.tw',
        'Referer': 'https://rent.591.com.tw/?kind=0&region=1',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'X-CSRF-TOKEN': 'QyF5MFL5nvC6zXeObDV1ljX4RUrayVsycb1PTAmk',
        'X-Requested-With': 'XMLHttpRequest'}
    url = xin_api +str(i)
    req = requests.get(url, headers=headers)
    task = BeautifulSoup(req.text,'html.parser')

    try:
        goods_url = json.loads(task.text)
        #物件url
        goods_urls = []

        for j in range(30):
            try:
                good_url = goods_url['data']['data'][j]['id']
                goods_urls.append(good_url)   
            except:
                pass
    except:
        pass

    
    for g in range(len(goods_urls)):
        under_url = 'https://rent.591.com.tw/rent-detail-'+ str(goods_urls[g]) +'.html'
        under_req = requests.get(under_url, headers=headers)
        u_task = BeautifulSoup(under_req.text,'html.parser')
        print(under_url)

        try:
            nick = u_task.select('div[class="avatarRight"]')[0].find('div').get_text()
#             print(nick)
            #出租者姓名
            linkmans = nick[:3]
            linkman.append(linkmans)     
            #出租者身份
            nicks = nick[3:].replace(r'(',"").replace(' ',"").replace(r')',"")
            nick_name.append(nicks)
    #         print(nick)
        except:
            pass
        
        #型態+現況 
        try:
            h_attr = u_task.select('ul[class="attr"]')[0].find_all('li')
            h_len = len(h_attr)
            for h in range(h_len):       
                h_attr[h]=h_attr[h].get_text()
                if  "型態" in h_attr[h]:               
                    house_attr.append(h_attr[h].replace("型態 :","").replace(" ","").replace("\xa0\xa0",""))
                else:
                    pass   
                
                if "現況" in h_attr[h]: 
                    house_now.append(h_attr[h].replace("現況 :","").replace(" ",""))
                else:
                    pass
        except:
            pass

        #電話
        try:
            h_phone = u_task.select('span[class="dialPhoneNum"]')[0].get('data-value')
            house_phone.append(h_phone)
        except:
            pass
        
        #性別要求
        try:
            h_id = u_task.select('ul[class="clearfix labelList labelList-1"]')[0].find_all('li')[1].get_text()
#             print(h_id)
            nus_h = h_id.find('性別要求')
#             print(nus_h)
            try:
                if nus_h != -1:
                    house_gender.append(h_id[nus_h:nus_h+10].replace("性別要求：",""))
                else:
                    house_gender.append("None")
            except:
                pass
        except:
            pass
#比對資料長度
print(len(linkman),len(nick_name),len(house_attr),len(house_now),len(house_phone),len(house_gender))   

#將DF合併
data = pd.concat([pd.DataFrame({'linkman': linkman}), pd.DataFrame({'nick_name':nick_name}), pd.DataFrame({'house_attr':house_attr}), 
                  pd.DataFrame({'house_now':house_now}), pd.DataFrame({'house_phone':house_phone}), pd.DataFrame({'house_gender':house_gender})], axis=1)


# In[2]:


#Elasticsearch 套件
es = Elasticsearch()

es.indices.create(index='xinpei001',ignore=[400,404])

INDEX = "xinpei001"
TYPE = "house"

#這裡將dataframe匯入db
def rec_to_actions(df):
    i=0
    for rec in df.to_dict(orient="records"):
        i+=1
        yield('{"index":{"_index":"%s","_type":"%s","_id":"%d"}}'%(INDEX,TYPE,i))
        yield(json.dumps(rec,default=int))

    if not es.indices.exists(INDEX):
        raise RuntimeError('Index does not exists')
        
#匯入Data
r = es.bulk(rec_to_actions(data))


# In[ ]:





# In[11]:





# In[ ]:





# In[ ]:




