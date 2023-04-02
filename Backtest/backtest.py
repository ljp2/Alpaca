#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import pandas_ta as ta

# In[2]:


class Status():
    def __init__(self):
        self.position = 0


# In[3]:


def checkPosition() -> int:
    """
    This will check position:
    Will return negative, 0, or positive inicating position in number of shares
    """
    return 0

def checkOrders() -> list:
    """
    This will check for outstanding Orders
    """
    return []



# In[4]:


def createFeatures(df : pd.DataFrame) -> pd.Series:
    """
    Creates the features which are input to the model
    """
    return pd.Series()


# In[5]:


def predictHighLow(features: pd.Series) -> dict:
    """
    Predicts the High and Low values from the features
    """
    return {'high': 0, 'low': 0}


# In[6]:


def createEvaluationFeatures(df: pd.DataFrame):
    pass


# In[7]:


def evaluatePosition(position: int):
    pass


# In[8]:
def addShiftedColumns(df: pd.DataFrame, xf: pd.DataFrame, columns: list, shift_list=[0, 1, 2, 3, 4]):
    shifted_column_names = []
    for column in columns:
        for i in shift_list:
            colname = f"{column}-{i}"
            shifted_column_names.append(colname)
            xf[colname] = df[column].shift(i)
    return shifted_column_names



def evaluateBarForTrade(df: pd.DataFrame):
    xf = pd.DataFrame()
    xf["hwap"] = ta.hma(df.wap)
    shifted_hlc_columns = addShiftedColumns(df, xf, ['high', 'low', 'close'] ) 
    for col in shifted_hlc_columns:
        xf[col+'h'] = 1000*(xf[col]/xf['hwap']-1)
    xf.drop(shifted_hlc_columns, axis=1, inplace=True)
    return xf.iloc[-1]


# In[9]:


def main():
    status = Status()
    for index,row in pd.read_csv("/Users/ljp2/ALLNEW/Data/bars1/20211008.csv").iterrows():
        if index == 0: 
            df = row.to_frame().T
        else:
            df.loc[len(df)] = row
            
        if index < 45: continue
            
        if status.position == 0:
            xf = evaluateBarForTrade(df)
            
        else:
            evaluatePosition(status.position)
            


# In[10]:


main()
