# -*- coding:utf-8 -*-
# 进行相关金融分析
#参考《Python金融实战》

import pandas as pd
from scipy import stats
import scipy as sp
import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":
    etf_total = pd.read_csv("total_etf.csv")
    etf_300 = pd.read_csv("300etf.csv")
    etf_nas = pd.read_csv("nasetf.csv")
    #t检验，看投资总收益率均数是否为0
    print(stats.ttest_1samp(etf_total.收益率, 0.0))
    #比较两个指数的相关性
    print(sp.stats.bartlett(etf_300.close, etf_nas.close))
    #优化 最小值
    from scipy.optimize import minimize
    def y_f(x):
        return (3+2*x**2)
    x0=100
    res = minimize(y_f, x0, method="nelder-mead", options={"xtol":1e-8, "disp":True})
    print(res.x)
    #计量运行时间
    #import time
#    start = time.clock()
#    n = 10000000
#    for i in range(1, n):
#        k = i+i+2
#    diff = time.clock() - start
#    print("%.2f" % diff)
    #正态分布
    x = sp.random.standard_normal(size = 10)
    print(x[0:5])
    #另一种方式
    x = sp.random.normal(0, 1, 10)
    print(x[0:5])
    #生成随机数
    sp.random.seed(12345)
    x = sp.random.normal(0, 1, 20)
    print(x[0:5])
    #画出正态分布图
    sp.random.seed(12345)
    x = sp.random.normal(0.08, 0.2, 1000)
    fig = plt.figure()
    plt.hist(x, 15, normed = True)
    fig.savefig("norm_hist.png")
    #对数正态分布
    x = np.linspace(0, 3, 200)
    mu =0
    sigma0 = [0.25, 0.5, 1.0]
    color = ['blue', 'red', 'green']
    target = [(1.2, 1.3), (1.7, 0.4), (0.18, 0.7)]
    start = [(1.8, 1.4), (1.9, 0.6), (0.18, 1.6)]
    fig = plt.figure()
    for i in range(len(sigma0)):
        sigma = sigma0[i]
        y = 1/(x*sigma*np.sqrt(2*np.pi))*np.exp(-(np.log(x)-mu)**2/(2*sigma*sigma))
        plt.annotate('mu = '+str(mu)+', sigma = '+str(sigma), xy = target[i], xytext = start[i], arrowprops = dict(facecolor = color[i], shrink = 0.01))
        plt.plot(x, y, color[i])
    fig.savefig("lognorm.png")
    #平均分布
    sp.random.seed(123345)
    x = sp.random.uniform(low = 1, high = 100, size = 10)
    print(x[0:5])
    #用蒙特卡洛算法求圆周率
    n = 100000
    x = sp.random.uniform(0, 1, n)
    y = sp.random.uniform(0, 1, n)
    dist = np.sqrt(x**2 + y**2)
    in_circle = dist[dist <= 1]
    our_pi = len(in_circle)*4./n
    print('pi = ', our_pi)
    print('error (%)= ', (our_pi - np.pi)/np.pi)
