# -*- coding:utf-8 -*-
# 尝试一下使用框架吧，自己写太乱了
# 这里用bt
# http://pmorissette.github.io/bt/#what-is-bt


import bt
import matplotlib.pyplot as plt
import pandas as pd


#输出结果
def Output(res):
    fig = res.plot()
    plt.savefig("btTest.png")
    res.display()
    fig = res.plot_histogram()
    plt.savefig("btHistTest.png")
    res.plot_security_weights()
    plt.savefig("btWeights.png")
    
    
if __name__ == "__main__":
    # 获取数据
    #data = bt.get("spy, agg", start = "2010-01-01")
    #print(data.head(), data.describe())
    #data.to_csv("btTest.csv")
    data2 = pd.read_csv("btTest.csv")
    data2["Date"] = pd.to_datetime(data2["Date"])
    data2.set_index("Date", inplace=True) 
    print(data2.head())

    # 创建策略
    s = bt.Strategy("s1", 
    [bt.algos.RunMonthly(),
     bt.algos.SelectAll(),
     bt.algos.WeighEqually(),
     bt.algos.Rebalance()])
    # 建立回测
    test = bt.Backtest(s, data2)
    res = bt.run(test)
    # 输出结果
    Output(res)
    # 建立新的策略
    s2 = bt.Strategy("s2",
    [bt.algos.RunWeekly(),
     bt.algos.SelectAll(),
     bt.algos.WeighInvVol(),
     bt.algos.Rebalance()])
    # 建立回测
    test2 = bt.Backtest(s2, data2)
    # 执行回测，一步一步显示
    res2 = bt.run(test, test2)
    # 输出
    Output(res2)
