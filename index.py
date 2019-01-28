# -*- coding:utf-8 -*-
# 用数据计算各种收益风险指标

import pandas as pd
import numpy as np


#将数据归一化,"数据"一列为要计算参数的那列,应为收益率
#因为数据有负数，如此归一化
#参考:https://www.zhihu.com/question/279542255
def DealwithData(data):
    maxd = data.数据.max()
    mind = data.数据.min()
    print(maxd, mind)
    data["数据"] = (data["数据"] - mind)/(maxd - mind)
    return data
    
    
#计算期间年化收益率
def GetAR(data):
    ar = (1+data.数据.iloc[-1])**(250.0/len(data.数据))-1
    return ar
    

#计算最大回撤
def GetMD(data):
    print(data.数据.cummax())
    md = ((data.数据.cummax() - data.数据)/data.数据.cummax()).max()
    return round(md, 4)



'''计算各指标的总函数，以后用户就调这个就行了。
data为要计算的策略的数据，basedata为基准数据。
safeIncome为无风险收益率，暂用余额宝的3%吧'''
def Index(data, safeIncome):
    ReturnRate(data)
    #print(data.收益率)


if __name__ == "__main__":
    total_etf = pd.read_csv("total_etf.csv")
    hist_300 = pd.read_csv("300etf.csv")
    #print(total_etf.收益率)
    etfdata = pd.DataFrame(
    {
    "日期":total_etf.日期.values,
    "数据":total_etf.收益率.values
    }
    )
    basedata = pd.DataFrame(
    {
    "日期":total_etf.日期.values,
    "数据":hist_300.close.values
    }
    )
    ar = GetAR(etfdata)
    print(ar)
    print(etfdata.head())
    etfdata = DealwithData(etfdata)
    print(etfdata.head())
    basedata = DealwithData(basedata)
    print(basedata.head())
    md = GetMD(etfdata)
    print(md)
    #Index(data,  0.03)