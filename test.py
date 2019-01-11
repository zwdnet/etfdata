# -*- coding:utf-8 -*-
# 用Python分析etf数据
#作者:赵瑜敏 zwdnet@163.com

import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import numpy as np


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
    
    
#有问题，暂存
'''
#记录每次交易的股票量，成交金额，手续费
    vol = []         #成交股票量
    money = []  #成交金额(含手续费)
    fee = []        #手续费
    date = []      #日期
    i = 0
    print(inverstData["成交日期"])
    for d in histData.date:
        time = d
        #print(i, inverstData["成交量"][i], inverstData["成交金额"][i], inverstData["手续费"][i])
        print(TransfDate2(time))
        print(TransfDate2(time) in inverstData["成交日期"])
        #第一个日期，一定是有交易记录的
        if i == 0:
            date.append(time)       
            vol.append(inverstData["成交量"][i])
            money.append(inverstData["成交金额"][i])
            fee.append(inverstData["手续费"][i])
        else:    #不是第一个日期
            #先判断这个日期有没有交易
            if TransfDate2(time) == inverstData["成交日期"][i]:
                #该日期存在交易
                print("a")
            #再判断该日期是否已有交易被记录
                if time in date:
                    #该日期已有交易被记录，累加
                    print("b")
                    vol[i-1] += inverstData["成交量"][i]
                    money[i-1] += inverstData["成交金额"][i]
                    fee[i-1] += inverstData["手续费"][i]
                else:
                    #没有交易被记录，新增
                    print("c")
                    date.append(time)       
                    vol.append(inverstData["成交量"][i] + vol[i-1]) 
                    money.append(inverstData["成交金额"][i])
                    fee.append(inverstData["手续费"][i])
            #该日期没有交易，复制上一个交易日的持仓数据，其余为0
            else:
                print("d")
                date.append(time)
                vol.append(vol[i-1])
                money.append(0.0)
                fee.append(0.0)
        i = i+1
    #print(date)
    #print(vol)
    #print(money)
    #print(fee)
'''
    
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
    #s = "2018-11-25"
    #print(TransfDate2(s))
    df = pd.DataFrame(np.arange(12).reshape(3,4), columns=["a", "b", "c", "d"])
    print(df)
    print(df.d)
    print(df["d"][0])
    print(3 == df["d"][0])
    
    
