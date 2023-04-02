import os

apikey = 'PKKJZYB9P6Q36H84YMXF'
secretkey = 'hBnEAEiD1f67p6hM4DKkUBtixY01YulNWSuGHOyx'

def getBarsDirectory():
    if os.name == "nt":
        BARS1_DIRECTORY = "C:/Alpaca/Data/bars1"
    else:
        BARS1_DIRECTORY = "/Users/ljp2/Alpaca/Data/bars1"
    return BARS1_DIRECTORY


def getAllFileDirectory():
    if os.name == "nt":
        ALL_FILE = "C:/Alpaca/Data/all.csv"
    else:
        ALL_FILE = "/Users/ljp2/Alpaca/Data"
    return ALL_FILE
