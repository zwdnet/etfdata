# -*- coding:utf-8 -*-
# 使用bt框架进行交易模拟


import bt
import pandas as pd
import matplotlib.pyplot as plt


#获取数据
def GetData():
    #读取数据
    df_300 = pd.read_csv("df_300_hist.csv")
    df_nas = pd.read_csv("df_nas_hist.csv")
    #只保留收盘价
    length1 = len(df_300)
    length2 = len(df_nas)
    df_300 = df_300.loc[0:length1, ["date", "close"]]
    df_nas = df_nas.loc[0:length2, ["date", "close"]]
    # 更改数据格式，使其符合bt要求
    df_300.columns = ["Date", "300etf"]
    df_300["Date"] = pd.to_datetime(df_300["Date"])
    df_300.set_index("Date", inplace = True)
    
    df_nas.columns = ["Date", "nasetf"]
    df_nas["Date"] = pd.to_datetime(df_nas["Date"])
    df_nas.set_index("Date", inplace = True)
    
    # 合并数据
    data = pd.concat([df_300, df_nas], axis = 1, join = "inner")
    
    # 返回数据
    return data
    
    
# 建立策略
def CreateStrategy(name):
    strategy = bt.Strategy(name,
    [bt.algos.RunWeekly(),
     bt.algos.SelectAll(),
     bt.algos.WeighEqually(),
     bt.algos.Rebalance()
    ])
    return strategy


# 输出回测结果
def outputResult(res):
    fig = res.plot()
    plt.savefig("BTStimulateTest.png")
    res.display()
    fig = res.plot_histogram()
    plt.savefig("BTStimulateHistTest.png")
    res.plot_security_weights()
    plt.savefig("BTStimulateWeights.png")


# 计算交易手续费
def getFee(quantity, price):
    rate = 0.0003
    fee = quantity*price*rate
    if fee < 0.1:
        fee = 0.1
    return fee


if __name__ == "__main__":
    data = GetData()
    print(data.describe())
    strategy = CreateStrategy("第一个定投策略")
    strategy.set_commissions(getFee)
    test = bt.Backtest(strategy, data)
    res = bt.run(test)
    outputResult(res)
    
    
    