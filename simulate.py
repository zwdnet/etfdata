# -*- coding:utf-8 -*-
# 模拟交易程序


import pandas as pd
import matplotlib.pyplot as plt


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
        self.feerate = feerate
        self.data = data
        self.stopPoint = stopPoint
        self.startPoint = startPoint
        # 股票交易数据
        # 每次交易剩下的钱
        self.money_rem = [0.0, 0.0]
        # 成本
        self.cost = [[0] * self.totalTimes for row in range(2)]
        # 持仓股票数量
        self.stock = [[0] * self.totalTimes for row in range(2)]
        # 市值
        self.value = [[0] * self.totalTimes for row in range(2)]
        # 手续费
        self.fee = [[0] * self.totalTimes for row in range(2)]
        # 收益率
        self.rate = [[0] * self.totalTimes for row in range(2)]
        # 总成本
        self.totalcost = [0] * self.totalTimes
        # 总费用
        self.totalfee = [0] * self.totalTimes
        # 总市值
        self.totalvalue = [0] * self.totalTimes
        # 总收益率
        self.totalrate = [0] * self.totalTimes
        
        
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
    def doTrade(self, days):
        # 计算资金能买多少股票
        self.money_rem[0] += self.money/2.0
        self.money_rem[1] += self.money/2.0
        num0 = self.getTradeNumber(self.money_rem[0], self.data[0]["close"][days])
        num1 = self.getTradeNumber(self.money_rem[0], self.data[1]["close"][days])
        # print(days, num0, num1)
        # 进行买入操作
        value0 = num0 * self.data[0]["close"][days]
        fee0 = self.getFee(num0, self.data[0]["close"][days])
        cost0 = value0 + fee0
        self.money_rem[0] -= cost0
        value1 = num1 * self.data[1]["close"][days]
        fee1 = self.getFee(num1, self.data[1]["close"][days])
        cost1 = value1 + fee1
        self.money_rem[1] -= cost1
        # 将相关数据存入
        if days == 0:
            self.cost[0][days] = cost0
            self.stock[0][days] = num0
            self.value[0][days] = value0
            self.fee[0][days] = fee0
            self.rate[0][days] = value0/cost0 -1.0
            self.cost[1][days] = cost1
            self.stock[1][days] = num1
            self.value[1][days] = value1
            self.fee[1][days] = fee1
            self.rate[1][days] = value1/cost1 -1.0
        else: # 不是第一天，计算累加值
            self.cost[0][days] = cost0 + self.cost[0][days - 1]
            self.stock[0][days] = num0 + self.stock[0][days - 1]
            self.value[0][days] = self.stock[0][days] * self.data[0]["close"][days]
            self.fee[0][days] = fee0 + self.fee[0][days - 1]
            self.rate[0][days] = self.value[0][days] / self.cost[0][days] -1.0
            self.cost[1][days] = cost1 + self.cost[1][days - 1]
            self.stock[1][days] = num1 + self.stock[1][days - 1]
            self.value[1][days] = self.stock[1][days] * self.data[1]["close"][days]
            self.fee[1][days] = fee1 + self.fee[1][days - 1]
            self.rate[1][days] = self.value[1][days] / self.cost[1][days] -1.0
        print(days, self.cost[0][days], self.stock[0][days], self.value[0][days], self.rate[0][days], self.rate[1][days])
            
        
    # 计算给定数量资金和股价可以买多少股票
    def getTradeNumber(self, money, price):
        num = int(money/price/100)*100
        fee = self.getFee(num, price)
        if num*price + fee <= money:
            return num
        elif num >= 100:
            return num - 100
        else:
            return 0
            
    # 计算手续费
    def getFee(self, num, price):
        fee = num*price*self.feerate
        if fee < 0.1:
            fee = 0.1
        return fee
        
    # 判断是否需要重新购买
    def isReturnBuy(self):
        pass
        
    # 用止盈的钱重新购买etf
    def doReturnBuy(self):
        pass
        
    # 更新相关数据
    def updateData(self, days):
        self.cost[0][days] = self.cost[0][days - 1]
        self.stock[0][days] = self.stock[0][days - 1]
        self.value[0][days] = self.stock[0][days] * self.data[0]["close"][days]
        self.fee[0][days] = self.fee[0][days - 1]
        self.rate[0][days] = self.value[0][days] / self.cost[0][days] -1.0
        self.cost[1][days] = self.cost[1][days - 1]
        self.stock[1][days] = self.stock[1][days - 1]
        self.value[1][days] = self.stock[1][days] * self.data[1]["close"][days]
        self.fee[1][days] = self.fee[1][days - 1]
        self.rate[1][days] = self.value[1][days] / self.cost[1][days] - 1.0
            
    # 将两个个股的数据综合，计算总收益率
    def combine(self, days):
        self.totalcost[days] = self.cost[0][days] + self.cost[1][days]
        self.totalfee[days] = self.fee[0][days] + self.fee[1][days]
        self.totalvalue[days] = self.value[0][days] + self.value[1][days]
        self.totalrate[days] = self.totalvalue[days] / self.totalcost[days] - 1.0
        print(days, self.totalcost[days], self.totalfee[days], self.totalvalue[days], self.totalrate[days])
    
        
    # 计算回测指标
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
            else:
                self.updateData(days)
            self.combine(days)
            self.tradeTimes += 1
        self.getIndex()
        # 作图测试
        plt.figure()
        plt.plot(self.rate[0], label = "300etf")
        plt.plot(self.rate[1], label = "nasetf")
        plt.plot(self.totalrate, label = "total")
        plt.legend(loc="best")
        plt.savefig("simulate_test.png")
        
            
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
    
