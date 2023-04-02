#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import numpy as np
import pandas as pd
import pandas_ta as ta

from config import *


def addShiftedColumns(df: pd.DataFrame, xf: pd.DataFrame, columns: list, shift_list=[0, 1, 2, 3, 4]):
    shifted_column_names = []
    for column in columns:
        for i in shift_list:
            colname = f"{column}-{i}"
            shifted_column_names.append(colname)
            xf[colname] = df[column].shift(i)
    return shifted_column_names

def addFutureHighLow5(df: pd.DataFrame, xf: pd.DataFrame):
    N = df.shape[0]
    high5 = np.empty(N)
    low5 = np.empty(N)
    highArg = np.empty(N)
    lowArg = np.empty(N)
    high = df.high.values
    low = df.low.values
    for i in range(N - 5):
        highs = high[i + 1:i + 6]
        lows = low[i + 1:i + 6]
        high5[i] = np.max(highs)
        low5[i] = np.min(lows)
    high5[N - 5:] = np.nan
    low5[N - 5:] = np.nan    
    xf['high+5'] = high5
    xf['low+5'] = low5
    added_columns = ['high+5', 'low+5']
    return added_columns


def createXY(df: pd.DataFrame):
    xf = pd.DataFrame()
    xf["hwap"] = ta.hma(df.wap)
    shifted_hlc_columns = addShiftedColumns(df, xf, ['high', 'low', 'close'] ) 
    
#     df['ao'] = ta.adosc(df.high, df.low, df.close, df.volume)
#     shifted_indicator_cols = addShiftedColumns(df,xf,['ao'])
    
    # z = ta.adx(df.high, df.low, df.close)
    # xf['ex1'] = z['ADX_14']
    # xf['ex2'] = z['DMP_14']
    # xf['ex3'] = z['DMN_14']
    # xf['ao'] = ta.ao(df.high, df.low)
    # xf['chop'] = ta.chop(df.high, df.low, df.close)
    
    # xf['apo'] = ta.apo(df.close)
    
    # m = ta.macd(df.close)
    # xf['macd'] = m['MACDh_12_26_9']
    
    # xf['adosc'] = ta.adosc(df.high, df.low, df.close, df.volume)

    high_low_columns = addFutureHighLow5(df,xf)
    
    for col in shifted_hlc_columns:
        xf[col+'h'] = 1000*(xf[col]/xf['hwap']-1)
        
        
    for col in high_low_columns:
        xf[col+'c'] = 1000*(xf[col]/df['close']-1)
        
    xf.drop(shifted_hlc_columns, axis=1, inplace=True)
    xf.drop(high_low_columns, axis=1, inplace=True)
    return xf





# In[3]:


BARS1_DIRECTORY = getBarsDirectory()
ALL_FILE_DIRECTORY = getAllFileDirectory()
first_file = True
filelist = os.listdir(BARS1_DIRECTORY)
filelist.sort(reverse=True)

firstfile = True
for f in filelist[:20]:
    df = pd.read_csv(f'{BARS1_DIRECTORY}/{f}')
    xyf = createXY(df)

    xyf.dropna(inplace=True)
    all_file = f'{ALL_FILE_DIRECTORY}/all.csv'
    if first_file:
        xyf.to_csv(all_file, mode='w', index=False, header=True)
        first_file = False
    else:
        xyf.to_csv(all_file, mode='a', index=False, header=False)
        

for x in xyf.columns: print(x)
print('DONE')


# In[ ]:




