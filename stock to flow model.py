# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 23:36:41 2021

@author: elced
"""

import numpy as np
import matplotlib.pyplot as plt
import json
import requests
import pandas as pd

# insert your API key here
API_KEY = '20gFkluFUgs9UXSByHtdtGlbh5K'
# make API request
res = requests.get('https://api.glassnode.com/v1/metrics/market/price_usd_close',
    params={'a': 'BTC','s':'1279411200', 'api_key': API_KEY})
res2 = requests.get('https://api.glassnode.com/v1/metrics/transactions/transfers_volume_within_exchanges_sum',
    params={'a': 'BTC','s':'1279411200','c':'NATIVE', 'api_key': API_KEY})
res3 = requests.get('https://api.glassnode.com/v1/metrics/transactions/transfers_volume_sum',
    params={'a': 'BTC','s':'1279411200','c':'NATIVE', 'api_key': API_KEY})
#res4 = requests.get('https://api.glassnode.com/v1/metrics/transactions/transfers_volume_from_miners_sum',
   # params={'a': 'BTC','s':'1279411200','c':'NATIVE', 'api_key': API_KEY})
res5 = requests.get('https://api.glassnode.com/v1/metrics/supply/sth_lth_realized_value_ratio',
    params={'a': 'BTC','s':'1279411200', 'api_key': API_KEY})
res6 = requests.get('https://api.glassnode.com/v1/metrics/addresses/active_count',
    params={'a': 'BTC','s':'1279411200', 'api_key': API_KEY})
#res7 = requests.get('https://api.glassnode.com/v1/metrics/derivatives/futures_liquidated_volume_short_mean',
    #params={'a': 'BTC','s':'1279411200', 'api_key': API_KEY})
res8 = requests.get('https://api.glassnode.com/v1/metrics/indicators/rhodl_ratio',
    params={'a': 'BTC','s':'1279411200', 'api_key': API_KEY})
res9 = requests.get('https://api.glassnode.com/v1/metrics/indicators/stock_to_flow_ratio',
    params={'a': 'BTC','s':'1279411200', 'api_key': API_KEY})
res10 = requests.get('https://api.glassnode.com/v1/metrics/lightning/network_capacity_sum',
    params={'a': 'BTC','s':'1279411200', 'api_key': API_KEY})
# convert to pandas dataframe
prix = pd.read_json(res.text, convert_dates=['t'])
exchangeout = pd.read_json(res2.text, convert_dates=['t'])
volume = pd.read_json(res3.text, convert_dates=['t'])
#minerout = pd.read_json(res4.text, convert_dates=['t'])
slrv = pd.read_json(res5.text, convert_dates=['t'])
addresses = pd.read_json(res6.text, convert_dates=['t'])
#liquidations = pd.read_json(res7.text, convert_dates=['t'])
rhodl = pd.read_json(res8.text, convert_dates=['t'])
stocktoflow = pd.read_json(res9.text, convert_dates=['t'])
lightning = pd.read_json(res10.text, convert_dates=['t'])


print(res)
print(slrv)
print(stocktoflow)
#Pour changer le nom des colonnes
prix.columns = ['Date', 'prix du BTC']
slrv.columns = ['Date', 'slrv']
exchangeout.columns = ['Date', 'exchanges outflow']
volume.columns = ['Date', 'volume']
#minerout.columns = ['Date', 'miners outflow']
addresses.columns = ['Date', 'active addresses']
#liquidations.columns = ['Date', 'liquidations short']
rhodl.columns = ['Date', 'rhodl']
stocktoflow.columns = ['Date', 'stock to flow']
lightning.columns = ['Date', 'lightning network capacity']

#Pour scinder les colonnes du stock to flow
b = stocktoflow.update('"' + stocktoflow['stock to flow'].astype(str) + '"')
print (stocktoflow)  

stocktoflow['stock to flow'] = stocktoflow['stock to flow'].str.replace(r"[\"\'\{\},]", "")
print (stocktoflow)

stocktoflow= stocktoflow.join(stocktoflow['stock to flow'].str.split(':', expand=True))
stocktoflow.pop('stock to flow')
stocktoflow.pop(1)
stocktoflow.pop(0)
stocktoflow.columns = ['Date', 'stock to flow']
print(stocktoflow)

stocktoflow['stock to flow']=stocktoflow['stock to flow'].astype('float64')
print(stocktoflow)
#Pour fusionner les differente base en fonction de la date de la premier base
new=pd.merge(stocktoflow, prix,how='left', on="Date")
print(new)

#Pour faire les graphiques
x1=np.array(prix['Date'])
x5=np.array(stocktoflow['Date'])
y1=np.array(prix['prix du BTC'])
y5=np.array(stocktoflow['stock to flow'])


plt.plot(x5,y5, label='stock to flow model')
plt.plot(x1,y1,label='prix du btc')
plt.yscale("log")
plt.title('Cours du Bitcoin depuis 2015')
plt.legend()
plt.show()


#pour exporter les données sur excel
#excel11= 'stocktoflow.xlsx'
#stocktoflow.to_excel(excel11) 