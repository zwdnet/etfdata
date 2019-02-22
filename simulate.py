# -*- coding:utf-8 -*-
# 模拟交易程序


class simulate(object):
    def __init__(self, totalTimes):
        self.tradeTimes = 0  #已经交易次数
        self.totalTimes = totalTimes
        pass
        
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
    def doTrade(self):
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
        while self.tradeTimes < self.totalTimes:
            self.getValue()
            if self.isStopProfit():
                self.doStopProfit()
            else:
                if self.isReturnBuy():
                    self.doReturnBuy()
                else:
                    self.doTrade()
            self.updateData()
            self.tradeTimes += 1
        self.getIndex()
            

if __name__ == "__main__":
    test = simulate(10)
    test.run()
    