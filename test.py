# -*- coding:utf-8 -*-
# 用Python分析etf数据
#作者:赵瑜敏 zwdnet@163.com

import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt


#从csv文件读入数据
def ImportData(FileName):
    df = pd.read_csv(FileName)
    return df
    
    
#探索数据
def ExploreData(Data):
    #每列的索引名称
    print(Data.columns)
    print(Data["成交金额"])
    print(Data.证券代码)
    #输出指定行的信息
    print(Data.ix[1])
    #返回Data的值
    print(Data.values)
    #对数据进行筛选
    print(Data[Data["证券名称"] == "300ETF"])
    
    
#分离数据:根据买入的etf的不同划分数据
def DivData(Data):
    df_300 = Data[Data["证券名称"] == "300ETF"]
    df_nas = Data[Data["证券名称"] == "纳指ETF"]
    return (df_300, df_nas)
    
    
def TransfDate2(s):
    year = int(s[0:4])
    month = int(s[5:7])    
    day = int(s[8:11])
    date = year*10000+month*100+day
    return date
    
    
#主程序
if __name__ == "__main__":
    #d = 20180105
#    year = int(d/10000)
#    month = int((d - year*10000)/100)
#    day = int((d - year*10000 - month*100))
#    date = format("%4d-%02d-%02d" % (year, month, day))
#    print(date)
    
    
    #import tushare
    #print(tushare.__version__)
    s = "2018-11-25"
    print(TransfDate2(s))
    
    
