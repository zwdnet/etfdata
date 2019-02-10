# -*- coding:utf-8 -*-
#对数据用蒙特卡洛算法进行分析

import pandas as pd
import datetime
import numpy as np
import index
import matplotlib.pyplot as plt
import etfdata
    
    
'''执行一次交易模拟
输入的参数
cost_pertime 每次投入金额
time 交易周期的天数
freq 交易频率，几天交易一次
df_300, df_nas,分别为两个定投的etf的实盘成交数据
返回值为一个DataFrame，包含每个交易日的成本，收益，收益率等数据
'''
def work(cost_pertime, time, freq, df_300, df_nas):
    #计算交易次数
    tradetimes = int(time/freq)
    #print(tradetimes)
    #print(money)
    #手续费比率
    fee_rate = 0.0003
    #把每次交易金额均分为两部分，分别买两个etf，如果钱不够交易，留到下次
    money_300 = cost_pertime/2.0
    money_nas = cost_pertime/2.0
    #下面两个是每次变动的成本
    m_300 = money_300
    m_nas = money_nas
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
    t = 0 #交易次数
    for i in range(time):
        if j == 0:   #交易
            #计算可以买的股票数量
            num_300 = int(m_300/df_300["close"][i]/100)*100
            num_nas = int(m_nas/df_nas["close"][i]/100)*100
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
            m_300 = m_300 + money_300_rem - m3 - fee_300
            mN = num_nas*df_nas["close"][i]
            fee_nas = mN*fee_rate
            if fee_nas < 0.1:
                fee_nas = 0.1
            fee.append(fee_300 + fee_nas)
            money_nas_rem = money_nas - mN - fee_nas
            m_nas = m_nas + money_nas_rem - mN - fee_nas
            
            print(i, m_300, m_nas)
            #计算总成本
            #total_cost = m3+fee_300+mN+fee_nas
            cost3.append(money_300*(t+1))
            costN.append(money_nas*(t+1))
            cost.append(cost_pertime*(t+1))
            t += 1
            print(i, cost3[i], costN[i], cost[i])
            #其它数据无论是否交易都要算，放最后
        else:    #不交易
            fee.append(0.0)
            cost.append(cost[i-1])
            cost3.append(cost3[i-1])
            costN.append(costN[i-1])
            V3.append(V3[i-1])
            VN.append(VN[i-1])
        #无论是否交易都要算的持仓市值，收益，收益率
        j += 1
        if j >= freq:
            j = 0
        Total3.append(V3[i]*df_300["close"][i])
        TotalN.append(VN[i]*df_nas["close"][i])
        Total.append(Total3[i] + TotalN[i])
        Income3.append(Total3[i] - cost3[i])
        IncomeN.append(TotalN[i] - costN[i])   
        Income.append(Income3[i] + IncomeN[i])
        Rate3.append(Income3[i]/cost3[i])
        RateN.append(IncomeN[i]/costN[i])
        Rate.append(Income[i]/cost[i])
        print(Total3[i], TotalN[i], Total[i])
        #print(i, Income3[i], IncomeN[i], Income[i], Rate3[i], RateN[i], Rate[i])
        
    data = pd.DataFrame(
    {
    "成本":cost,
    "手续费":fee,
    "市值":Total,
    "收益":Income,
    "收益率":Rate
    }
    )
    return data
    
    
#按不同交易频率进行交易
def Run(cost, time, df_300, df_nas):
    data = []
    for freq in range(1, 31):
        data.append(work(cost, time, freq, df_300, df_nas))
    return data


if __name__=="__main__":
    #实盘数据分析
#    df_etf = pd.read_csv("total_etf.csv")
#    df_300 = pd.read_csv("300etf.csv")
#    df_nas = pd.read_csv("nasetf.csv")
#    df_data = pd.DataFrame(
#    {
#    "数据":df_etf["收益率"].values
#    }
#    )
#    df_base = pd.DataFrame(
#    {
#    "数据":df_300["close"].values
#    }
#    )
#    #result = index.index(df_data, df_base, 0.029)
#    #print(result)
#    #进行模拟
#    #先获取成本，交易周期等信息
#    cost = df_etf["成本"].values[-1]
#    print(cost)
#    time = len(df_etf)
#    #进行交易模拟
#    data = work(cost, time, 10, df_300, df_nas)
#    print(data.head())
#    testdata = pd.DataFrame(
#    {
#    "数据":data["收益率"].values
#    }
#    )
#    result = index.index(testdata, df_base, 0.03)
#    print(result)
#    #测试成功，现在模拟不同交易频率对结果的影响
#    testresult = Run(cost, time, df_300, df_nas)
#    testindex = [] #保存测试结果的回测指标
#    for res in testresult:
#        print(res.head())
#        test = pd.DataFrame(
#        {
#        "数据":res["收益率"].values
#        }
#        )
#        testindex.append(index.index(test, df_base, 0.03))
#    AR = []
#    MD = []
#    alpha = []
#    shaper = []
#    for test in testindex:
#        print(test.head())
#        AR.append(test["年化收益率"])
#        MD.append(test["最大回撤"])
#        alpha.append(test["α系数"])
#        shaper.append(test["夏普系数"])
#    #数据可视化
#    fig = plt.figure()
#    plt.plot(AR)
#    fig.savefig("montecarlo_ar.png")
#    fig = plt.figure()
#    plt.plot(MD)
#    fig.savefig("montecarlo_md.png")
#    fig = plt.figure()
#    plt.plot(alpha)
#    fig.savefig("montecarlo_α.png")
#    fig = plt.figure()
#    plt.plot(shaper)
#    fig.savefig("montecarlo_shaper.png")
    #获取从2013年5月15日至2019年02月01日的数据
    #beginTime = 20130515
#    endTime = 20190201
#    etf300 = etfdata.GetHistoryData("510300", beginTime, endTime)
#    etfnas = etfdata.GetHistoryData("513100", beginTime, endTime)
#    print(len(etf300), len(etfnas))
#    #保存文件
#    etf300.to_csv("df_300_hist.csv")
#    etfnas.to_csv("df_nas_hist.csv")
    #读取数据
    df_300 = pd.read_csv("df_300_hist.csv")
    df_nas = pd.read_csv("df_nas_hist.csv")
    #只保留收盘价
    length1 = len(df_300)
    length2 = len(df_nas)
    df_300 = df_300.loc[0:length1, ["date", "close"]]
    df_nas = df_nas.loc[0:length2, ["date", "close"]]
    print(len(df_300), len(df_nas))
    #试试用实盘的策略的模拟结果
    freq = 10
    times = len(df_300)
    data = work(1000, times, freq, df_300, df_nas)
    print(data)
    #计算指标
    #先处理基准指标，剔除没交易的日期的数据
    #df_300 = df_300[df_300["date"].isin(data.日期.values)]
    df_base = pd.DataFrame(
    {
    "数据":df_300["close"].values
    }
    )
    
    testdata = pd.DataFrame(
    {
    "数据":data["收益率"].values
    }
    )
    print(df_base.head(), len(df_base))
    print(testdata.head())
    result = index.index(testdata, df_base, 0.03)
    print(result)
    #画图看看吧。
    fig = plt.figure()
    plt.plot(testdata[("数据")])
    fig.savefig("模拟结果.png")
    
    
    
    
    
