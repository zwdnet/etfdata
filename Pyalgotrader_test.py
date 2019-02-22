# coding=utf-8
from pyalgotrade import strategy
from pyalgotrade.bar import Frequency
from pyalgotrade.barfeed.csvfeed import GenericBarFeed
 
# 1.构建一个策略
class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(MyStrategy, self).__init__(feed)
        self.__instrument = instrument
 
    def onBars(self, bars):# 每一个数据都会抵达这里，就像becktest中的next
        bar = bars[self.__instrument]
        self.info(bar.getClose())# 我们打印输出收盘价
 
# 2.获得回测数据，官网来源于yahoo，由于墙的关系，我们用本地数据
feed = GenericBarFeed(Frequency.DAY, None, None)
feed.addBarsFromCSV("fd", "fd.csv")
 
# 3.把策略跑起来
myStrategy = MyStrategy(feed, "fd")
myStrategy.run()
