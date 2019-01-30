# -*- coding:utf-8 -*-
# 用数据计算各种收益风险指标

import pandas as pd
import numpy as np
from scipy import stats


#将数据归一化,"数据"一列为要计算参数的那列,应为收益率
#因为数据有负数，如此归一化
#参考:https://www.zhihu.com/question/279542255
def DealwithData(data):
    maxd = data["数据"].max()
    mind = data["数据"].min()
    #print(maxd, mind)
    data["数据"] = (data["数据"] - mind)/(maxd - mind)
    return data
    
    
#计算期间年化收益率，用原始数据
def GetAR(data):
    ar = (1+data["数据"].iloc[-1])**(250.0/len(data["数据"]))-1
    return ar
    

#计算最大回撤，因为数据已经是收益率了，直接减就行了。用原始数据。
def GetMD(data):
    md = (data["数据"].cummax() - data["数据"]).max()
    return round(md, 4)
    
    
#计算β和α系数
#因为是指数定投，不存在停盘等数据缺失的问题
def AlphaBeta(data, basedata):
    x = basedata["数据"].values #基准数据
    y = data["数据"].values #要评价的数据
    b,a,r_value,p_value,std_err = stats.linregress(x, y)
    #print(b, a, r_value, p_value, std_err)
    a = round(a*250, 3)
    AB = [a, round(b, 3)]
    return (AB)


#计算夏普比率,saferate为无风险收益，用余额宝收益吧。
def Sharpe(data, saferate):
    exReturn = data["数据"] - saferate/250.0
    sharperatio = np.sqrt(len(exReturn))*exReturn.mean()/exReturn.std()
    #print(sharperatio)
    return sharperatio
    
    
#计算信息比率
def Information(data, basedata):
    ex_return = data["数据"] - basedata["数据"]
    information = np.sqrt(len(ex_return))*ex_return.mean()/ex_return.std()
    #print(information)
    return information


'''计算各指标的总函数，以后用户就调这个就行了。
data为要计算的策略的数据，basedata为基准数据。
safeIncome为无风险收益率，暂用余额宝的3%吧'''
def index(data, basedata, safeIncome):
    AR = GetAR(data) #计算年化收益率
    MD = GetMD(data) #计算最大回撤
    AB = AlphaBeta(data, basedata) #计算αβ系数
    SR = Sharpe(data, safeIncome) #计算夏普系数
    IR = Information(data, basedata)
    result = [AR, MD, AB[0], AB[1], SR, IR]
    df_result = pd.Series(data = result, index =["年化收益率", "最大回撤", "α系数", "β系数", "夏普系数", "信息比率"])
    return df_result
    
    
if __name__ == "__main__":
    total_etf = pd.read_csv("total_etf.csv")
    hist_300 = pd.read_csv("300etf.csv")
    #print(total_etf.收益率)
    etfdata = pd.DataFrame(
    {
    "数据":total_etf["收益率"].values
    }, index = total_etf["日期"]
    )
    basedata = pd.DataFrame(
    {
    "数据":hist_300["close"].values
    }, index = total_etf["日期"]
    )
    #ar = GetAR(etfdata)
#    print(ar)
#    md = GetMD(etfdata)
#    print(md)
#    Sharpe(etfdata, 0.03)
#    Information(etfdata, basedata)
    result = index(etfdata, basedata, 0.03)
    print(result)
    #AlphaBeta(etfdata, basedata)
    #print(etfdata.head())
    #etfdata = DealwithData(etfdata)
    #print(etfdata.head())
    #basedata = DealwithData(basedata)
    #print(basedata.head())
    #AlphaBeta(etfdata, basedata)
    
    #Index(data,  0.03)
