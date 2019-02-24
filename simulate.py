# -*- coding:utf-8 -*-
# 模拟交易程序


import pandas as pd


"""
模拟交易类
初始参数:
    money:每次定投投入的资金
    totalTime:总的交易天数
    freq:交易频率，隔几天交易一次
    feerate:手续费费率
    data:股票历史数据，为一个数组。
    stopPoint: 止盈点
    startPoint: 止盈以后何时停止止盈
"""
class simulate(object):
    def __init__(self, money, totalTimes, freq, feerate, data, stopPoint, startPoint):
        self.money = money
        self.tradeTimes = 0  # 已经交易次数
        self.totalTimes = totalTimes
        self.freq = freq
        self.data = data
        self.stopPoint = stopPoint
        self.startPoint = startPoint
        # 股票交易数据
        # 每次交易剩下的钱
        self.money_rem_0 = 0.0
        self.money_rem_1 = 0.0
        # 成本
        self.cost = [[0] * self.totalTimes for row in range(2)]
        # 市值
        self.value = [[0] * self.totalTimes for row in range(2)]
        # 手续费
        self.fee = [[0] * self.totalTimes for row in range(2)]
        # 收益率
        self.rate = [[0] * self.totalTimes for row in range(2)]
        
        
    # 计算持仓股票市值
    def getValue(self):
        pass
        
    # 判断是否进行止盈操作
    def isStopProfit(self):
        pass
        
    # 进行止盈操作
    def doStopProfit(self):
        pass
        
    # 进行交易
    def doTrade(days):
        pass
        
    # 判断是否需要重新购买
    def isReturnBuy(self):
        pass
        
    # 用止盈的钱重新购买etf
    def doReturnBuy(self):
        pass
        
    # 更新相关数据
    def updateData(self):
        pass
        
    #计算回测指标
    def getIndex(self):
        pass
        
    # 执行交易循环
    def run(self):
        for days in range(self.totalTimes):
            if days > 0:
                if self.isStopProfit():
                    self.doStopProfit()
            if self.isReturnBuy():
                self.doReturnBuy()
            if days % self.freq == 0: #进行交易
                self.doTrade(days)
            self.updateData()
            self.tradeTimes += 1
        self.getIndex()
            

if __name__ == "__main__":
    #读取数据
    df_300 = pd.read_csv("df_300_hist.csv")
    df_nas = pd.read_csv("df_nas_hist.csv")
    #只保留收盘价
    length1 = len(df_300)
    length2 = len(df_nas)
    df_300 = df_300.loc[0:length1, ["date", "close"]]
    df_nas = df_nas.loc[0:length2, ["date", "close"]]
    data = [df_300, df_nas]
    print(data[0].head())
    test = simulate(1000, len(df_300), 10, 0.0003, data, 0.1, 0.1)
    test.run()
    
