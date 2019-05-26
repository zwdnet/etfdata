# -*- coding:utf-8 -*-
# bt文档里的例子 改策略


import bt
import pandas as pd
import matplotlib.pyplot as plt


# 获取数据
def getData():
    # data = bt.get("aapl, msft, c, gs, ge",  start = "2010-01-01")
    # data.to_csv("btexam_data.csv")
    data = pd.read_csv("btexam_data.csv")
    data["Date"] = pd.to_datetime(data["Date"])
    data.set_index("Date", inplace=True)
    return data


# 选择何时操作的类
class SelectWhere(bt.Algo):
    def __init__(self, signal):
        self.signal = signal
        
    def __call__(self, target):
        if target.now in self.signal.index:
            sig = self.signal.ix[target.now]
            selected = list(sig.index[sig])
            target.temp["selected"] = selected
        return True


# 移动平均线策略
"""
选择:高于其50日均线的证券
权重:均等
再平衡投资组合以反映目标权重
"""
def SMA(data):
    sma = data.rolling(50).mean()
    plot = bt.merge(data, sma).plot(figsize=(15, 5))
    plt.savefig("sma.png")
    
    # 建立策略
    s = bt.Strategy("above50sma",
        [SelectWhere(data > sma),
         bt.algos.WeighEqually(),
         bt.algos.Rebalance()
        ])
    # 建立回测
    t = bt.Backtest(s, data)
    # 执行回测
    res = bt.run(t)
    # 输出结果
    res.display()
    res.plot()
    plt.savefig("sma_result.png")
    
    # 多种策略的测试
    sma10 = above_sma(data, sma_per = 10, name = "sma10")
    sma20 = above_sma(data, sma_per = 10, name = "sma20")
    sma40 = above_sma(data, sma_per = 10, name = "sma40")
    base_line = baseTest(data)
    
    # 一起运行回测
    res2 = bt.run(sma10, sma20, sma40, base_line)
    # 输出结果
    res2.display()
    res2.plot()
    plt.savefig("sma.png")
    plt.savefig("multi_sma_result.png")
    
    
# 可以改变参数的测试函数
def above_sma(data, sma_per = 50, name = "above_sma"):
    sma = data.rolling(sma_per).mean()
    s = bt.Strategy(name,
    [bt.algos.SelectWhere(data > sma),
     bt.algos.WeighEqually(),
     bt.algos.Rebalance()
    ])
    return bt.Backtest(s, data)
    
    
# 一次买入，作为基线测试
def baseTest(data):
    s = bt.Strategy("base_line",
    [bt.algos.RunOnce(),
     bt.algos.SelectAll(),
     bt.algos.WeighEqually(),
     bt.algos.Rebalance()
    ])
    return bt.Backtest(s, data)


if __name__ == "__main__":
    # 获取数据
    data = getData()
    print(data.head())
    print(data.describe())
    SMA(data)
    
    