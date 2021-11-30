# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 14:16:37 2021

@author: elced
"""

import matplotlib.pyplot as plt
import pandas as pd                        
from pytrends.request import TrendReq
pytrend = TrendReq()
pytrend.build_payload(kw_list=['bitcoin'], timeframe='2010-07-18 2021-01-01' )
df = pytrend.interest_over_time()
print(df)
plt.plot(df.index,df.bitcoin, label= 'Popularité du bitcoin')
plt.title('Recherche du terme bitcoin sur google trend')
plt.legend()
plt.show()