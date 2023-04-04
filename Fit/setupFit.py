import os
import numpy as np
import pandas as pd

def getAllFileDirectory():
    if os.name == "nt":
        ALL_FILE_DIRECTORY = "C:/Alpaca/Data/"
    else:
        ALL_FILE_DIRECTORY = "/Users/ljp2/Alpaca/Data"
    return ALL_FILE_DIRECTORY

def calcOutlierBounds(df:pd.DataFrame, col:str, multiple_of_std: float):
    x = df[col]
    m = x.mean()
    s = x.std()
    upper = m + 2.5 * s
    lower = m - 2.5 * s
    return {'lower': lower, 'upper': upper}

def removeOutliers(df):
    upper = calcOutlierBounds(df, 'high+5c', 2.5)['upper']
    lower = calcOutlierBounds(df, 'low+5c', 2.5)['lower']
    xf = df[df['high+5c'] < upper]
    xf = xf[xf['low+5c'] > lower]
    return xf

def calcXy(df: pd.DataFrame, col: str) -> object:
    xf = removeOutliers(df)
    y = xf[col]
    X = xf.drop(['hwap', 'high+5c', 'low+5c'], axis=1)
    return X,y


