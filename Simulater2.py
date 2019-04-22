# 重新建立一个交易模拟函数吧
# 之前的太乱了


import pandas as pd
import matplotlib.pyplot as plt
import os


"""
模拟交易类
"""
class simulater(object):
    def __init__(self):
        pass
        
        
if __name__ == "__main__":
    #读取数据
    df_300 = pd.read_csv("df_300_hist.csv")
    df_nas = pd.read_csv("df_nas_hist.csv")
    #只保留收盘价
    length1 = len(df_300)
    length2 = len(df_nas)
    df_300 = df_300.loc[0:length1, ["date", "close"]]
    df_nas = df_nas.loc[0:length2, ["date", "close"]]
    data = [df_300, df_nas]
    print(data[0].head())
    test = simulater()
    