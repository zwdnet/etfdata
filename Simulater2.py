# 重新建立一个交易模拟函数吧
# 之前的太乱了


import pandas as pd
import matplotlib.pyplot as plt
import os


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
totalFee: 总费用
totalValue: 总市值
totalRate: 总收益率
money_rem: 每次交易剩下的钱
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
        self.totalFee = [0] * self.totalTimes
        self.totalValue = [0] * self.totalTimes
        self.totalRate = [0] * self.totalTimes
        self.money_rem = [0.0, 0.0]
        
        
    # 执行交易
    def doTrade(self, days):
        pass
        
        
    # 没有进行交易的日期更新数据
    def update(self, code, days):
        pass
        
        
    # 交易循环
    def run(self):
        for days in range(self.totalTimes):
            if days % self.freq == 0: #进行交易
                self.doTrade(days)
            else:
                for code in range(2):
                    self.update(code, days)
        
        
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
    test = simulater(1000, data, len(df_300), 10, 0.0003)
    