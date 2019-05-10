# -*- coding:utf-8 -*-
# 计算定投年化收益率的程序
# 直接从github上抄的
# https://github.com/peliot/XIRR-and-XNPV/edit/master/financial.py
# 照这里重写吧
# https://github.com/Tacombel/XIRR.py?files=1


import datetime
from scipy import optimize 
from random import random
import pandas as pd
import copy
import xirr_cal as xirr
import matplotlib.pyplot as plt

    
# 返回给定数据的年化收益率
def aRets(data, now, price, stocks):
    # 方法，在data里加一行数据，卖出现有持仓，然后计算
    tempData = copy.deepcopy(data)
    value = stocks*price
    tempData.append((now, value))
    values = []
    dates = []
    for d,v in tempData:
        values.append(v)
        dates.append(d)
    retRate = xirr.xirr(values, dates)
    return retRate


if __name__ == "__main__":
    beginDate = datetime.date(2018,1,1)
    timedelta = datetime.timedelta(days = 1)
    now = beginDate
    cost = 0.0
    money = 1000
    freq = 10
    money_rem = 0.0
    price = 1.0
    feeRate = 0.0003
    stocks = 0
    value = 0.0
    data = []
    returnRates = []
    for day in range(365):
        now = now + timedelta
        r = random()
        if r < 0.5:
            price = price - 0.01
            if price < 0.0:
                price = 0.0
        else:
            price = price + 0.01
        if day % freq == 0:
            money = money + money_rem
            money_rem = 0
            num = int(money/price/100)*100
            fee = num*price*feeRate
            if fee < 0.1:
                fee = 0.1
            if num*price + fee <= money:
                num = num
            elif num >= 200:
                if (num - 100)*price <= money:
                    num = num - 100
                else:
                    num = 0
            cost = num*price + fee
            stocks += num
            value = stocks*price
            money_rem = money - cost
            data.append((now, cost*(-1.0)))
        if day >100:
            # 计算今日的年化收益率
            rate = aRets(data, now, price, stocks)
            returnRates.append(rate)
    print(returnRates)
    plt.figure()
    plt.plot(returnRates)
    plt.savefig("xirr_test.png")
    val = [-10000, -1000, 1010, 10000]
    date = [datetime.date(2012, 1,1), datetime.date(2012, 1, 11), datetime.date(2012, 1, 12),
    datetime.date(2012,12,31)]
    result = xirr.xirr(val, date)
    print(result)
            
