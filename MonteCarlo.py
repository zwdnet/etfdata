# -*- coding:utf-8 -*-
#对数据用蒙特卡洛算法进行分析

import pandas as pd
import datetime
import numpy as np
import index
import matplotlib.pyplot as plt
import etfdata
    
    
#此函数作废，重写
'''执行一次交易模拟
输入的参数
cost_pertime 每次投入金额
time 交易周期的天数
freq 交易频率，几天交易一次
df_300, df_nas,分别为两个定投的etf的实盘成交数据
返回值为一个DataFrame，包含每个交易日的成本，收益，收益率等数据
'''
def work2(cost_pertime, time, freq, df_300, df_nas):
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
    
    
'''执行一次交易模拟
输入的参数
cost_pertime 每次投入金额
time 交易周期的天数
freq 交易频率，几天交易一次
df_300, df_nas,分别为两个定投的etf的实盘成交数据
返回值为一个DataFrame，包含每个交易日的成本，收益，收益率等数据
bCut,是否止盈止损
up,止盈点
down,止损点
'''
def work(cost_pertime, time, freq, df_300, df_nas, bCut, up, down):
    #计算交易次数
    tradetimes = int(time/freq)
    #手续费费率
    fee_rate = 0.0003
    #买每个etf的金额为总投资额的一半
    money_per_etf = cost_pertime/2.0
    #每次实际投资金额
    money_300 = money_per_etf
    money_nas = money_per_etf
    #每次剩下的钱，累加到下一次
    money_300_rem = 0
    money_nas_rem = 0
    
    #定义变量
    #成本
    cost300 = []
    costNas = []
    cost = []
    #手续费
    fee300 = []
    feeNas = []
    fee = []
    #持仓量
    stack300 = []
    stackNas = []
    stack = []
    #市值
    value300 = []
    valueNas = []
    value = []
    #持仓收益
    income = []
    #持仓收益率
    rate = []
    
    #执行模拟
    j = 0
    #保存最大最小收益率
    minRate = 0.0
    maxRate = 0.0
    bCutUp = False #下次是否止盈
    bCutDown = False #下次是否止损
    #止盈止损卖出股票得到的钱
    money_cut_300 = 0.0
    money_cut_nas = 0.0
    #是否进行了止盈止损操作
    bUp = False
    bDown = False
    
    for i in range(times):
        #进行交易，如果在止盈止损期间，暂停交易
        if j == 0 and ((bCutUp == False and bCutDown == False) or bCut == False):
            #先计算能投入的金额
            #如果进行过止盈止损，把卖出得到的钱加上
            money300 = money_300 + money_300_rem
            moneyNas = money_nas + money_nas_rem
            if bUp == True or bDown == True:
                money300 += money_cut_300
                moneyNas += money_cut_nas
                money_cut_300 = 0.0
                money_cut_nas = 0.0
                bUp = False
                bDown = False
            #计算买入数量
            num300 = TradeNumber(money300, df_300["close"][i])
            numNas = TradeNumber(moneyNas, df_nas["close"][i])
            if i == 0:
                stack300.append(num300)
                stackNas.append(numNas)
            else:
                stack300.append(stack300[i-1] + num300)
                stackNas.append(stackNas[i-1] + numNas)
            #print(i, num300, numNas)
            #计算买入成本
            cost_300 = TradeCost(num300, df_300["close"][i])
            fee_300 = TradeFee(cost_300, fee_rate)
            cost_nas = TradeCost(numNas, df_nas["close"][i])
            fee_nas = TradeFee(cost_nas, fee_rate)
            if i == 0:
                fee.append(fee_300 + fee_nas)
                cost300.append(cost_300 + fee_300)
                costNas.append(cost_nas + fee_nas)
            else:
                fee.append(fee[i-1] + fee_300 + fee_nas)
                cost300.append(cost300[i-1] + cost_300 + fee_300)
                costNas.append(costNas[i-1] + cost_nas + fee_nas)
            cost.append(cost300[i] + costNas[i])
            money_300_rem = money300 - cost_300 - fee_300
            money_nas_rem = moneyNas - cost_nas - fee_nas
        else:        #不进行交易
            stack300.append(stack300[i-1])
            stackNas.append(stackNas[i-1])
            cost300.append(cost300[i-1])
            costNas.append(costNas[i-1])
            cost.append(cost[i-1])
            fee.append(fee[i-1])
        j += 1
        if j == freq:
            j = 0
        #不管是否交易都要计算的数据
        #计算市值
        value300.append(stack300[i] * df_300["close"][i])
        valueNas.append(stackNas[i] * df_nas["close"][i])
        value.append(value300[i] + valueNas[i])
        #计算收益
        income.append(value[i] - cost[i])
        #计算收益率
        rate.append(income[i]/cost[i])
        
        #进行止盈止损操作
        if bCut == True:
            print(i, rate[i],  stack300[i], stackNas[i], minRate, maxRate, bCutUp, bCutDown)
            #保存最大最小收益率
            if bUp == False and bDown == False:
                minRate = min(rate)
                maxRate = max(rate)
            #判断是否触发止盈止损操作
            if rate[i] > up:
                bCutUp = True
                bCutDown = False
            elif rate[i] < down:
                bCutUp = False
                bCutDown = True
            else:
                bCutUp = False
                bCutDown = False
            
            #先判断进行止盈止损操作
            if i != 0 and (bCutUp == True or bCutDown == True):
                #进行止盈止损，每次卖存量的一半
                #300etf
                sellNumber300 = int(stack300[i]/200)*100
                if sellNumber300 < 100:
                    sellNumber300 = 0
                stack300[i] -= sellNumber300
                sellmoney300 = TradeCost(sellNumber300, df_300["close"][i])
                sellfee300 = TradeFee(sellmoney300, fee_rate)
                money_cut_300 = sellmoney300 + sellfee300
                value300[i] -=  money_cut_300
                cost300[i] -= money_cut_300
                #纳指etf
                sellNumberNas = int(stackNas[i]/200)*100
                if sellNumberNas < 100:
                    sellNumberNas = 0
                stackNas[i] -= sellNumberNas
                sellmoneyNas = TradeCost(sellNumberNas, df_nas["close"][i])
                sellfeeNas = TradeFee(sellmoneyNas, fee_rate)
                money_cut_Nas = sellmoneyNas + sellfeeNas
                valueNas[i] -=  money_cut_Nas
                costNas[i] -= money_cut_Nas
                #计算合并数据
                fee[i] += sellfee300 + sellfeeNas
                value[i] = value300[i] + valueNas[i]
                cost[i] = cost300[i] + costNas[i]
                income[i] = value[i] - cost[i]
                rate[i] = income[i]/cost[i]
                if bCutUp == True:
                    #设置止盈操作标志
                    bUp = True
                    minRate += up #将基线提高，看是否还要止盈的。
                    bCutUp = False
                    #print(i, "止盈")
                elif bCutDown == True:
                    #设置止损标志
                    bDown = True
                    maxRate -= down #将基线降低，看是否需要止损的
                    bCutDown = False
                    #print(i, "止损")
                #print(i, bUp, bDown, rate[i]-minRate, maxRate-rate[i], rate[i], money_cut_300, money_cut_nas)
                    
    
    #形成返回数据
    data = FormResult(cost, fee, value, income, rate)
    return data
    
    
#形成返回数据
def FormResult(cost, fee, value, income, rate):
    data = pd.DataFrame(
    {
    "成本":cost,
    "手续费":fee,
    "市值":value,
    "收益":income,
    "收益率":rate
    }
    )
    return data
    

#根据可用的资金和收盘价，计算可以买的股票数量
def TradeNumber(money, price):
    num = int(money/price/100)*100
    return num
    
    
#根据成交量和成交价计算成本，不含手续费
def TradeCost(number, price):
    cost = number*price
    return cost
    
    
#根据交易金额,费率计算手续费
def TradeFee(money, rate):
    fee = money * rate
    if fee < 0.1:
        fee = 0.1
    return fee
    
    
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
    #试试用实盘的策略的模拟结果
    freq = 10
    times = len(df_300)
    data = work(1000, times, freq, df_300, df_nas, True, 0.15, -0.1)
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
    result = index.index(testdata, df_base, 0.03)
    print(result)
    #画图看看吧。
    fig = plt.figure()
    plt.plot(testdata[("数据")])
    fig.savefig("模拟结果.png")
    