# -*- coding:utf-8 -*-
# 模拟交易程序


import pandas as pd
import matplotlib.pyplot as plt
import os


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
        # 止盈卖出后得到的钱
        self.money_cut = [0.0, 0.0]
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
        # 最低，最高收益率，用来计算止盈止损点
        self.minPrice = [0.0] * 2
        self.maxPrice = [0.0] * 2
        # 是否正在止盈
        self.bStop = [False] * 2
        # 是否正在停止止盈
        self.bStart = [False] * 2
        # 最后一次止盈的钱
        self.cutValue = [0.0] * 2
        self.cutFee = [0.0] * 2
    

        #清屏
        os.system("clear")
        
        
    # 判断是否进行止盈操作，根据days前的交易情况，code为0或1
    def isStopProfit(self, code, days):
        # return False # 测试用
        price = self.data[code]["close"][days]
        # 没有正在进行止盈
        if self.bStop[code] == False:
            if self.minPrice[code] > price:
                self.minPrice[code] = price
            if self.maxPrice[code] < price:
                self.maxPrice[code] = price
            # 判断止盈条件
            if price/self.maxPrice[code] <= 1.0 - self.stopPoint:
                self.bStop[code] = True
                # 将最高/低价调整到现价
                self.maxPrice[code] = price
                self.minPrice[code] = price
                return True
        # 如果已经进行了止盈
        if self.bStop[code] == True:
            if self.minPrice[code] > price:
                self.minPrice[code] = price
            # 判断止盈条件
            if price/self.maxPrice[code] <= 1.0 - self.stopPoint:
                # 将最高/低价调整到现价
                self.maxPrice[code] = price
                self.minPrice[code] = price
                return True
        return False
                
        
    # 进行止盈操作
    def doStopProfit(self, code, days):
        money = self.value[code][days-1]/2.0
        num = self.getTradeNumber(money, self.data[code]["close"][days])
        value = num * self.data[code]["close"][days]
        fee = self.getFee(num, self.data[code]["close"][days])
        # 更新数据
        # 只有股票数量大于一手并且交易金额小于预定金额才做
        if num > 100 and value + fee <= money:
            # print("止盈前", code, days, self.value[code][days], self.cost[code][days], self.stock[code][days], self.rate[code][days], num, value, fee)
            self.money_cut[code] += value - fee
        
            # print("a", code, days, money, num, value, fee)
            # 进行止盈操作
            self.stock[code][days] -= num
            self.value[code][days] -= value
            self.fee[code][days] += fee
            self.rate[code][days] = (self.value[code][days] + self.money_cut[code])/ self.cost[code][days] -1.0
            #self.cutValue[code] = value
#            self.cutFee[code] = fee
            # print(self.cost[code])
            # print(self.value[code])
            # print(self.rate[code])
            # print("止盈后", code, days, self.value[code][days], self.cost[code][days], self.stock[code][days], self.rate[code][days], num, value, fee)
        else:
            self.bStop[code] = False
        

    # 判断是否需要重新购买
    def isReturnBuy(self, code, days):
        # return False #测试用
        # 如果进行了止盈，判断是否停止止盈
        if self.bStop[code] == True or self.bStart[code] == True:
            price = self.data[code]["close"][days]
            if price/self.minPrice[code] >= 1.0 + self.startPoint:
                self.bStart[code] = True
                # 将最高/低价调整到现价
                self.maxPrice[code] = price
                self.minPrice[code] = price
                # 停止止盈
                self.bStop[code] = False
                return True
        return False


    # 用止盈的钱重新购买etf
    def doReturnBuy(self, code, days):
        # 用止盈得到的剩余的钱的一半以现价再投资。
        money = self.money_cut[code]/2.0
        num = self.getTradeNumber(money, self.data[code]["close"][days])
        value = num * self.data[code]["close"][days]
        fee = self.getFee(num, self.data[code]["close"][days])
        # print("止盈", code, days, money, num, value, fee)
        # 如果可以交易的股票数量低于一手，或者股价+手续费大于预定的金额，则停止交易。
        if num <= 100 or value + fee > money:
            self.bStart[code] = False
        else: # 进行交易并更新数据。
            # print("停止止盈前", code, days, self.value[code][days], self.cost[code][days], self.stock[code][days], self.rate[code][days], num, value, fee)
            self.stock[code][days] += num
            self.value[code][days] += value
            self.fee[code][days] += fee
            self.money_cut[code] -= value+fee
            # print("停止止盈后", code, days, self.value[code][days], self.cost[code][days], self.stock[code][days], self.rate[code][days], num, value, fee)

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
            self.rate[0][days] = (self.value[0][days] + self.money_cut[0])/ self.cost[0][days] -1.0
            self.cost[1][days] = cost1 + self.cost[1][days - 1]
            self.stock[1][days] = num1 + self.stock[1][days - 1]
            self.value[1][days] = self.stock[1][days] * self.data[1]["close"][days]
            self.fee[1][days] = fee1 + self.fee[1][days - 1]
            self.rate[1][days] = (self.value[1][days] + self.money_cut[1])/ self.cost[1][days] -1.0
        # print(days, self.cost[0][days], self.stock[0][days], self.value[0][days], self.rate[0][days], self.rate[1][days])
            
        
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

        
    # 更新相关数据
    def update(self, code, days):
        # 更新股票数据
        self.cost[code][days] = self.cost[code][days - 1]
        self.stock[code][days] = self.stock[code][days - 1]
        self.value[code][days] = self.stock[code][days] * self.data[code]["close"][days]
        self.fee[code][days] = self.fee[code][days - 1]
        self.rate[code][days] = (self.value[code][days] + self.money_cut[code])/ self.cost[code][days] -1.0
        
        
    # 在止盈操作以后更新数据
    def cutUpdate(self, code, days):
        pass
            
            
    # 将两个个股的数据综合，计算总收益率
    def combine(self, days):
        self.totalcost[days] = self.cost[0][days] + self.cost[1][days]
        self.totalfee[days] = self.fee[0][days] + self.fee[1][days]
        self.totalvalue[days] = self.value[0][days] + self.value[1][days]
        self.totalrate[days] = (self.totalvalue[days] + self.money_cut[0] + self.money_cut[1])/ self.totalcost[days] - 1.0
        # print(days, self.totalcost[days], self.totalfee[days], self.totalvalue[days], self.totalrate[days])
        # print(days, self.money_cut[0], self.money_cut[1])
    
        
    # 计算回测指标
    def getIndex(self):
        pass
        
    # 执行交易循环
    def run(self):
        for days in range(self.totalTimes):
            if days % self.freq == 0: #进行交易
                self.doTrade(days)
            else:
                for code in range(2):
                    self.update(code, days)
            # print("位置a", days, self.value[0][days], self.cost[0][days], self.rate[0][days], self.value[1][days], self.cost[1][days], self.rate[1][days], self.totalrate[days])
            if days == 0:
                self.minPrice[0] = self.data[0]["close"][0]
                self.minPrice[1] = self.data[1]["close"][0]
                self.maxPrice[0] = self.data[0]["close"][0]
                self.maxPrice[1] = self.data[1]["close"][0]
            else:
                for code in range(2):
                    if self.isStopProfit(code, days):
                        self.doStopProfit(code, days)
                        # print(code, days, "止盈")
                        # print(code, days, self.cost[code][days-1], self.value[code][days-1], self.cost[code][days], self.value[code][days])

            for code in range(2):
                if self.isReturnBuy(code, days):
                    self.doReturnBuy(code, days)
                    # print(code, days, "停止止盈")
                    # print(code, days, self.cost[code][days-1], self.value[code][days-1], self.cost[code][days], self.value[code][days])

            # # 止盈后更新数据
            # for code in range(2):
            #     self.cutUpdate(code, days)
            self.combine(days)
            # print("位置b", days, self.value[0][days], self.cost[0][days], self.rate[0][days], self.value[1][days], self.cost[1][days], self.rate[1][days], self.totalrate[days])
            self.tradeTimes += 1
            # print(days, self.totalcost[days], self.totalvalue[days], self.totalrate[days])
        self.getIndex()
        # 作图测试
        plt.figure()
        plt.plot(self.rate[0], label = "300etf", linestyle = "-")
        plt.plot(self.data[0]["close"]/self.data[0]["close"][0]-1.0, label = "300", linestyle = "-.")
        plt.legend(loc="best")
        # plt.show()
        plt.savefig("simulate_01.png")
        plt.figure()
        plt.plot(self.rate[1], label = "nasetf", linestyle = "--")
        plt.plot(self.data[1]["close"]/self.data[1]["close"][0]-1.0, label = "nas", linestyle = ":")
        plt.legend(loc="best")
        # plt.show()
        plt.savefig("simulate_02.png")
        plt.figure()
        plt.plot(self.data[0]["close"]/self.data[0]["close"][0]-1.0, label = "300", linestyle = "-.")
        plt.plot(self.data[1]["close"]/self.data[1]["close"][0]-1.0, label = "nas", linestyle = ":")
        plt.plot(self.totalrate, label = "total")
        plt.legend(loc="best")
        # plt.show()
        plt.savefig("simulate_03.png")
        
        plt.figure()
        
        plt.plot(self.value[0], label = "300value")
        plt.plot(self.cost[0], label = "300cost")
        plt.legend(loc = "best")
        plt.savefig("debug1.png")
        
        plt.figure()
        
        plt.plot(self.value[1], label = "nasvalue")
        plt.plot(self.cost[1], label = "nascost")
        plt.legend(loc = "best")
        plt.savefig("debug2.png")
        
            
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
    test = simulate(1000, len(df_300), 10, 0.0003, data, 0.1, 0.1)
    test.run()
    
