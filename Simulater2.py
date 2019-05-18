# -*- coding:utf-8 -*-
# 重新建立一个交易模拟函数吧
# 之前的太乱了


import pandas as pd
import matplotlib.pyplot as plt
import os
import getIndex
import xirr_cal as xirr
import datetime
import GetHistoryData
import copy
import BacktestIndex as BTI

"""
模拟交易类
money: 每次投资金额
data: 历史收盘数据
totalTimes: 投资总时间
cost: 总成本(即投入的资金总数)
position: 持仓量
freq: 交易频率，即隔几天交易一次
feeRate: 交易手续费费率
fee: 交易手续费
value: 持仓市值
income: 收益
incomeRate: 收益率
xirr: 年化收益率
cashFlow: 现金流量表
cashDate: 交易日期
totalCost: 总成本
totalFee: 总费用
totalValue: 总市值
totalIncome: 总收益
totalRate: 总收益率
totalCashFlow: 总现金流量表
totalCashDate: 总现金流量发生日期
totalXirr: 总年化收益率
money_rem: 每次交易剩下的钱
testIndex: 回测指标
"""
class simulater(object):
    def __init__(self, money, data, totalTimes, freq, feeRate):
        self.money = money
        self.data = data
        self.totalTimes = totalTimes
        self.cost =  [[0.0] * self.totalTimes for row in range(2)]
        self.position = [[0.0] * self.totalTimes for row in range(2)]
        self.fee = [[0.0] * self.totalTimes for row in range(2)]
        self.freq = freq
        self.feeRate = feeRate
        self.value = [[0.0] * self.totalTimes for row in range(2)]
        self.income = [[0.0] * self.totalTimes for row in range(2)]
        self.incomeRate = [[0.0] * self.totalTimes for row in range(2)]
        self.xirr = [[0.0] * self.totalTimes for row in range(2)]
        self.cashFlow = [[] * self.totalTimes for row in range(2)]
        self.cashDate = [[] * self.totalTimes for row in range(2)]
        self.totalCost = [0] * self.totalTimes
        self.totalFee = [0] * self.totalTimes
        self.totalValue = [0] * self.totalTimes
        self.totalIncome = [0] * self.totalTimes
        self.totalRate = [0] * self.totalTimes
        self.totalCashFlow = []
        self.totalCashDate = []
        self.totalXirr = [0] * self.totalTimes
        self.money_rem = [0.0, 0.0]
        self.testIndex = None
        
        
    # 计算交易手续费
    def getFee(self, number, price):
        fee = number*price*self.feeRate
        if fee < 0.1:
            fee = 0.1
        return fee
        
        
    # 计算给定资金能买多少股票
    def getStockNumber(self, money, price):
        num = int(money/price/100)*100
        fee = self.getFee(num, price)
        if num*price + fee <= money:
            return num
        elif num >= 200:
            if (num - 100)*price <= money:
                return num - 100
            else:
                return 0
        else:
            return 0
            
            
    # 更新盈利数据
    def updateIncome(self, days):
        income = [0.0, 0.0]
        incomeRate = [0.0, 0.0]
        totalCost = [0.0, 0.0]
        for code in range(2):
            #总成本 = 购买成本 + 手续费 + 剩余的钱
            totalCost[code] = self.cost[code][days] + self.fee[code][days] + self.money_rem[code]
            # 收益 = 市值 - 总成本
            income[code] = self.value[code][days] - totalCost[code]
            incomeRate[code] = income[code]/totalCost[code]
            # 更新收益数据
            self.income[code][days] = income[code]
            self.incomeRate[code][days] = incomeRate[code]
            
            
    # 进行输出
    def display(self, days):
        print("交易日:%d 成本1:%.2f 持仓量1:%.2f 市值1:%.2f 收益率1:%.2f 年化收益率1:%.2f 成本2:%.2f 持仓量2:%.2f 市值2:%.2f 收益率2:%.2f 总收益率:%.2f 年化收益率2:%.2f 总年化收益率:%.2f" % (days, self.cost[0][days], self.position[0][days], self.value[0][days], self.incomeRate[0][days], self.xirr[0][days], self.cost[1][days], self.position[1][days], self.value[1][days], self.incomeRate[1][days], self.totalRate[days], self.xirr[1][days], self.totalXirr[days]))
        
        
    # 执行交易
    def doTrade(self, days):
        # 计算能买股票的资金
        self.money_rem[0] += self.money/2.0
        self.money_rem[1] += self.money/2.0
        # 计算资金能买到的股票数量
        stock = [0, 0]
        for code in range(2):
            stock[code] = self.getStockNumber(self.money_rem[code], self.data[code]["close"][days])
        value = [0.0, 0.0]
        cost = [0.0, 0.0]
        fee = [0.0, 0.0]
        for code in range(2):
            # 进行买入操作
            value[code] = stock[code] * self.data[code]["close"][days]
            fee[code] = self.getFee(stock[code], self.data[code]["close"][days])
            cost[code] = value[code]
            # 将数据存入
            if days == 0:    # 第一天
                self.cost[code][days] = cost[code]
                self.fee[code][days] = fee[code]
                self.position[code][days] = stock[code]
            else: # 不是第一天，计算累计值
                self.cost[code][days] = self.cost[code][days-1] + cost[code]
                self.fee[code][days] = self.fee[code][days-1] + fee[code]
                self.position[code][days] = self.position[code][days-1] + stock[code]
            # 更新现金流量表，算xirr用的
            v = (value[code] + fee[code]) * (-1)
            d = GetHistoryData.TransfDate2Datetime(self.data[code]["date"][days])
            self.cashFlow[code].append(v)
            self.cashDate[code].append(d)
            self.totalCashFlow.append(v)
            self.totalCashDate.append(d)
            
            # 存入总市值
            self.value[code][days] = self.position[code][days] * self.data[code]["close"][days]
            # 更新剩余资金数据
            self.money_rem[code] -= cost[code]
            # 更新盈利数据
            self.updateIncome(days)
            
        
        
    # 没有进行交易的日期更新数据
    def update(self, code, days):
        if days == 0:
            return
        else:
            self.cost[code][days] = self.cost[code][days-1]
            self.position[code][days] = self.position[code][days-1]
            self.fee[code][days] = self.fee[code][days-1]
            self.value[code][days] = self.position[code][days] * self.data[code]["close"][days]
            self.updateIncome(days)
            
            
    # 将两个个股的数据合并
    def combine(self, days):
        self.totalCost[days] = self.cost[0][days] + self.cost[1][days]
        self.totalFee[days] = self.fee[0][days] + self.fee[1][days]
        self.totalValue[days] = self.value[0][days] + self.value[1][days]
        self.totalIncome[days] = self.totalValue[days] - self.totalCost[days] - self.totalFee[days]
        self.totalRate[days] = self.totalIncome[days]/self.totalCost[days]
        
        
    # 作图
    def draw(self):
        plt.figure()
        plt.plot(self.incomeRate[0], label = "300etf", linestyle = "-")
        plt.plot(self.data[0]["close"]/self.data[0]["close"][0]-1.0, label = "300", linestyle = "-.")
        plt.legend(loc="best")
        plt.savefig("simulater_01.png")
        
        plt.figure()
        plt.plot(self.incomeRate[1], label = "nasetf", linestyle = "--")
        plt.plot(self.data[1]["close"]/self.data[1]["close"][0]-1.0, label = "nas", linestyle = ":")
        plt.legend(loc="best")
        plt.savefig("simulater_02.png")
        
        plt.figure()
        plt.plot(self.data[0]["close"]/self.data[0]["close"][0]-1.0, label = "300", linestyle = "-.")
        plt.plot(self.data[1]["close"]/self.data[1]["close"][0]-1.0, label = "nas", linestyle = ":")
        plt.plot(self.totalRate, label = "total")
        plt.legend(loc="best")
        plt.savefig("simulater_03.png")
        
        plt.figure()
        plt.plot(self.totalCost, label = "cost", linestyle = "-.")
        plt.plot(self.totalIncome, label = "income", linestyle = ":")
        plt.plot(self.totalValue, label = "total")
        plt.legend(loc="best")
        plt.savefig("simulater_04.png")
        
        plt.figure()
        plt.plot(self.totalIncome, label = "total")
        plt.legend(loc="best")
        plt.savefig("simulater_05.png")
        
        plt.figure()
        plt.plot(self.xirr[0], label = "300")
        plt.plot(self.xirr[1], label = "nas")
        plt.plot(self.totalXirr, label = "total")
        plt.legend(loc="best")
        plt.savefig("simulater_06.png")
        
        
    # 计算回测指标
    def index(self, data):
        # 先整理数据，市场基准数据用300etf
        testdata = {"市场":self.xirr[0], "策略":data}
        InputData = pd.DataFrame(testdata)
        tester = BTI.GetIndex(InputData)
        result = tester.run()
        print(result)
        self.testIndex = result
        
        
    # 用xirr计算年化收益率
    def cal_xirr(self, days):
        v = 0.0
        date = GetHistoryData.TransfDate2Datetime(self.data[0]["date"][days])
        for code in range(2):
            value = self.data[code]["close"][days] * self.position[code][days]
            v += value
            self.cashFlow[code].append(value)
            self.cashDate[code].append(date)
            retXIRR = xirr.xirr(self.cashFlow[code], self.cashDate[code])
            # 开始的时候会出现无限大的值，所以加这个
            # 画图得知，前150天数据不靠谱，都设成0吧
            if days <= 150:
                retXIRR = 0.0
            self.xirr[code][days] = retXIRR
            self.cashFlow[code].pop()
            self.cashDate[code].pop()
        self.totalCashFlow.append(v)
        self.totalCashDate.append(date)
        totalXIRR = xirr.xirr(self.totalCashFlow, self.totalCashDate)
        if days <= 150:
            totalXIRR = 0.0
        self.totalXirr[days] = totalXIRR
        self.totalCashFlow.pop()
        self.totalCashDate.pop()
        
        
    # 获取回测数据
    def GetIndex(self):
        return self.testIndex
    
        
    # 交易循环
    def run(self):
        for days in range(self.totalTimes):
            if days % self.freq == 0: #进行交易
                self.doTrade(days)
            else:
                for code in range(2):
                    self.update(code, days)
            self.combine(days)
            self.cal_xirr(days)
            # print(self.xirr[0][days], self.xirr[1][days])
            #self.display(days)
            #print(self.cashFlow, self.cashDate)
        # print(self.xirr[0])
        self.draw()
        self.index(self.totalXirr)
        
        
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
    # print(data[0].head())
    #dates = datetime.date(df_300["date"][0])
    #print(dates)
    test = simulater(1000, data, len(df_300), 10, 0.0003)
    test.run()
    
