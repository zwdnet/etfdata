# -*- coding:utf-8 -*-
#对数据用蒙特卡洛算法进行分析

import pandas as pd
import datetime
import numpy as np


#将八位数字格式日期转化为datetime类型
def GetDatetime(d):
    year = int(d/10000)
    month = int((d - year*10000)/100)
    day = int((d - year*10000 - month*100))
    date = datetime.datetime(year, month, day)
    return date


#返回指定年份的天数
def Days(year):
    if year % 100 == 0:
        if year % 400 == 0:
            return 366
        else:
            return 365
    elif year % 4 == 0:
        return 366
    else:
        return 365

#计算投资策略的相关评价数据
def Judgement(data, basedata, saferate):
    #1.计算年化收益率，算最大最小的吧
    maxInput = data.收益率.max()
    minInput = data.收益率.min()
    #print(maxInput, minInput)
    #计算最大年化收益率
    dateend = data[data.收益率 == maxInput].日期
    datebegin = data.日期[0]
    #print(datebegin)
    dateb = GetDatetime(datebegin)
    datee = GetDatetime(dateend)
    days = (datee - dateb).days
    #print(days)
    days_per_year = Days(int(dateend/10000))
    MaxRate = maxInput/days*days_per_year
    #计算最大损失率
    dateend = data[data.收益率 == minInput].日期
    #print(dateend)
    datee = GetDatetime(dateend)
    days = (datee - dateb).days
    #print(days)
    days_per_year = Days(int(dateend/10000))
    MinRate = minInput/days*days_per_year
    #print(MaxRate, MinRate)
    #2.计算最大回撤率
    i = 0
    maxRedraw = 0.0
    maxRedrawRate = 0.0
    for rate in data.收益率:
        Redraw = data.收益率[i:].max() - data.收益率[i:].min()
        RedrawRate = Redraw/data.收益率[i:].max()
        if RedrawRate > maxRedrawRate:
            maxRedrawRate = RedrawRate
        i += 1
    #print(maxRedrawRate)
    #3.计算beta比例
    #用平均收益率，先计算沪深300的基准收益率,以及标准差
    baserate = [0.0] #设第一天收益率为0
    i = 0
    for i in range(1, len(basedata.close)):
        baserate.append((basedata.close[i] - basedata.close[i-1])/basedata.close[i-1])
    mean_baserate = np.mean(baserate)
    std_baserate = np.std(baserate)
    #计算投资组合的平均收益率
    mean_rate = data.收益率.mean()
    std_rate = data.收益率.std()
    #print(mean_rate, std_rate)
    
    #saferate为无风险收益，余额宝的收益
    #计算β系数
    #以余额宝收益率3%为无风险收益率
    n = len(data)
    rate_year = (data.收益率[n-1]/data.收益率[0])**(250.0/n - 1)
    baserate_year = (basedata.close[n-1]/basedata.close[0])**(250.0/n - 1)
    beta = (rate_year-saferate)/(baserate_year-saferate)
    #print(beta)
    #4.计算α系数
    # print(rate_year-saferate, beta*(baserate_year-saferate))
    alpha = rate_year - saferate - beta*(baserate_year - saferate)
    #print(alpha)
    #5.计算夏普指数
    shape = (mean_rate-saferate)/std_rate
    #print(shape)
    return pd.Series([MaxRate, MinRate, maxRedrawRate, beta, alpha, shape])
    
    

if __name__=="__main__":
    df_etf = pd.read_csv("total_etf.csv")
    df_300 = pd.read_csv("300etf.csv")
    print(df_etf.head())
    print(df_300.head())
    result = Judgement(df_etf, df_300, 0.029)
    print(result)
