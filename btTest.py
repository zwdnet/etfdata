# -*- coding:utf-8 -*-
# 尝试一下使用框架吧，自己写太乱了
# 这里用bt
# http://pmorissette.github.io/bt/#what-is-bt


import bt
import matplotlib.pyplot as plt


if __name__ == "__main__":
    # 获取数据
    data = bt.get("spy, agg", start = "2010-01-01")
    print(data.head())
    # 创建策略
    s = bt.Strategy("s1", 
    [bt.algos.RunMonthly(),
     bt.algos.SelectAll(),
     bt.algos.WeighEqually(),
     bt.algos.Rebalance()])
    # 建立回测
    test = bt.Backtest(s, data)
    res = bt.run(test)
    # 输出结果
    fig = res.plot()
    print(type(fig))
    plt.savefig("btTest.png")
    res.display()
    fig = res.plot_histogram()
    print(type(fig))
    plt.savefig("btHistTest.png")
    res.plot_security_weights()
    plt.savefig("btWeights.png")