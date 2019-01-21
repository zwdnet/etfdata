# -*- coding:utf-8 -*-
#对数据用蒙特卡洛算法进行分析

import pandas as pd
import datetime


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
def Judgement(data):
    #1.计算年化收益率，算最大最小的吧
    maxInput = data.收益率.max()
    minInput = data.收益率.min()
    print(maxInput, minInput)
    #计算最大年化收益率
    dateend = data[data.收益率 == maxInput].日期
    datebegin = data.日期[0]
    print(datebegin)
    dateb = GetDatetime(datebegin)
    datee = GetDatetime(dateend)
    days = (datee - dateb).days
    print(days)
    days_per_year = Days(int(dateend/10000))
    MaxRate = maxInput/days*days_per_year
    #计算最大损失率
    dateend = data[data.收益率 == minInput].日期
    print(dateend)
    datee = GetDatetime(dateend)
    days = (datee - dateb).days
    print(days)
    days_per_year = Days(int(dateend/10000))
    MinRate = minInput/days*days_per_year
    print(MaxRate, MinRate)
    

if __name__=="__main__":
    df_etf = pd.read_csv("total_etf.csv")
    print(df_etf.head())
    Judgement(df_etf)