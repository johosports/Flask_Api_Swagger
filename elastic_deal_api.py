#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import json
from pprint import pprint
from elasticsearch import Elasticsearch
import pandas as pd


# In[5]:


es = Elasticsearch()

es.indices.create(index='taipei',ignore=[400,404])

df = pd.read_csv('taipei.csv')
INDEX = "taipei"
TYPE = "house"
df = df.drop(columns=['Unnamed: 0']).fillna("NA")
df.head()

#這裡將dataframe匯入db
def rec_to_actions(df):
    i=0
    for rec in df.to_dict(orient="records"):
        i+=1
        yield('{"index":{"_index":"%s","_type":"%s","_id":"%d"}}'%(INDEX,TYPE,i))
        yield(json.dumps(rec,default=int))

if not es.indices.exists(INDEX):
    raise RuntimeError('Index does not exists')

r = es.bulk(rec_to_actions(df))


# In[6]:


es.search(index='taipei', filter_path=['hits.hits._id', 'hits.hits'])


# In[ ]:




