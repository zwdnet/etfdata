# -*- coding:utf-8 -*-
#对数据用蒙特卡洛算法进行分析

import pandas as pd
import datetime
import numpy as np
import index
    
    
'''执行一次交易模拟
输入的参数
cost 总交易成本
time 交易周期的天数
freq 交易频率，几天交易一次
df_300, df_nas,分别为两个定投的etf的实盘成交数据
返回值为一个DataFrame，包含每个交易日的成本，收益，收益率等数据
'''
def work(cost, time, freq, df_300, df_nad):
    #计算交易次数
    tradetimes = int(time/freq)
    print(tradetimes)
    #计算每次交易的金额
    money = cost/tradetimes
    print(money)
    #手续费比率
    fee_rate = 0.0003
    #把每次交易金额均分为两部分，分别买两个etf，如果钱不够交易，留到下次
    money_300 = money/2.0
    money_nas = money/2.0
    #开始模拟前定义相关变量
    cost = [] #投入的总成本
    cost3 = [] #买300etf的成本
    costN = [] #买纳指etf的成本
    m3 = 0.0 #买300etf的钱
    mN = 0.0 #买纳指etf的钱
    fee = [] #手续费
    V3 = [] #300etf股票数量
    VN = [] #纳指etf股票数量
    Total3 = [] #300etf的当前市值
    TotalN = [] #纳指etf的当前市值
    Total = [] #当前总市值
    Income3 = [] #300etf的收益
    IncomeN = [] #nasetf的收益
    Income = [] #总收益
    Rate3 = [] #300etf收益率
    RateN = [] #nasetf收益率
    Rate = [] #总收益率
    #每次交易剩下的钱
    money_300_rem = 0.0
    money_nas_rem = 0.0
    
    #开始模拟
    j = 0
    for i in range(time):
        if j == 0:   #交易
            #计算可以买的股票数量
            num_300 = int(money_300/df_300["close"][i]/100)*100
            num_nas = int(money_nas/df_nas["close"][i]/100)*100
            if i == 0:
                V3.append(num_300)
                VN.append(num_nas)
            else:
                V3.append(V3[i-1] + num_300)
                VN.append(VN[i-1]+ num_nas)
            #计算购入成本
            m3 = num_300*df_300["close"][i]
            fee_300 = m3*fee_rate
            if fee_300 < 0.1:
                fee_300 = 0.1
            money_300_rem = money_300 - m3 - fee_300
            money_300 += money_300_rem
            mN = num_nas*df_nas["close"][i]
            fee_nas = mN*fee_rate
            if fee_nas < 0.1:
                fee_nas = 0.1
            fee.append(fee_300 + fee_nas)
            money_nas_rem = money_nas - mN - fee_nas
            money_nas += money_nas_rem
            
            #计算总成本
            total_cost = m3+fee_300+mN+fee_nas
            if i == 0:
                cost3.append(m3+fee_300)
                costN.append(mN+fee_nas)
                cost.append(cost3[i] + costN[i])
            else:
                cost3.append(cost3[i-1] + m3 + fee_300)
                costN.append(costN[i-1] + mN + fee_nas)
                cost.append(cost[i-1] + cost3[i] + costN[i])
            #其它数据无论是否交易都要算，放最后
        else:    #不交易
            fee.append(0.0)
            cost.append(cost[i-1])
            V3.append(V3[i-1])
            VN.append(VN[i-1])
        #无论是否交易都要算的持仓市值，收益，收益率
        j += 1
        if j >= freq:
            j = 0
        Total3.append(V3[i]*df_300["close"][i])
        TotalN.append(VN[i]*df_nas["close"][i])
        Total.append(Total3[i] + TotalN[i])
        print(len(Total3), len(cost3), i)
        Income3.append(Total3[i] - cost3[i])
        IncomeN.append(TotalN[i] - costN[i])   
        Income.append(Income3[i] + IncomeN[i])
        Rate3.append(Income3[i]/cost3[i])
        RateN.append(IncomeN[i]/costN[i])
        Rate.append(Income[i]/cost[i])
        
    data = pd.DataFrame(
    {
    "成本":cost.values,
    "手续费":fee.values,
    "市值":Total.values,
    "收益":Income.values,
    "收益率":Rate.values
    }
    )
    return data

if __name__=="__main__":
    #实盘数据分析
    df_etf = pd.read_csv("total_etf.csv")
    df_300 = pd.read_csv("300etf.csv")
    df_nas = pd.read_csv("nasetf.csv")
    df_data = pd.DataFrame(
    {
    "数据":df_etf["收益率"].values
    }
    )
    df_base = pd.DataFrame(
    {
    "数据":df_300["close"].values
    }
    )
    result = index.index(df_data, df_base, 0.029)
    print(result)
    #进行模拟
    #先获取成本，交易周期等信息
    cost = df_etf["成本"].values[-1]
    print(cost)
    time = len(df_etf)
    #进行交易模拟
    data = work(cost, time, 10, df_300, df_nas)
    print(data.head())
    
    
