# -*- coding:utf8 -*-
#对转换好的数据进行数据分析

import pandas as pd
import matplotlib.pyplot as plt


#数据可视化
def Display(data):
    fig = plt.figure()
    ax1 = fig.add_subplot(2,2,1)
    ax2 = fig.add_subplot(2,2,2)
    ax3 = fig.add_subplot(2,2,3)
    ax4 = fig.add_subplot(2,2,4)
    #用各种不同的形式画图
    ax1.plot(data.收益率)
    ax2.hist(data.收益率, bins =10, alpha = 0.8, facecolor = 'b', normed = 1)
    ax3.scatter(range(len(data)), data.收益率, marker ='.')
    ax4.plot(data.收益率, 'k--')
    
    fig.savefig("可视化数据.png")
    #另一种方法
    fig,ax = plt.subplots(2,2)
    ax[0, 0].plot(data.收益率)
    ax[0, 1].plot(data.收益率, 'k--')
    ax[1, 0].plot(data.收益率, 'k-', drawstyle='steps-post')
    ax[1, 1].plot(data.收益率, linestyle='dashed', marker='o')
    fig.savefig("可视化数据2.png")
    #绘图并增加图例
    #正常显示中文，没成功，放弃 #plt.rcParams['font.sans-serif']=['SimHei']
    #plt.rcParams['axes.unicode_minus']=False
    fig,ax = plt.subplots(1,1)
    ax.plot(data.收益率, label ="income rate")
    fc = data.手续费/data.成本
    ax.plot(fc, label="fee percent")
    plt.legend(loc="best")
    fig.savefig("可视化数据3.png")
    #用pandas画图
    fig = plt.figure()
    data.收益率.plot(kind = 'bar', xticks = [0, 40, 80, 120, 160, 200])
    fig.savefig("pandas作图.png")
    fig = plt.figure()
    data.收益率.hist(bins =20, normed = True)
    fig.savefig("pandas作图2.png")
    
    
#移动时间窗口分析
def MovementWindows(data):
    #mean_5 = data.收益率.rolling(window=5, center = False).mean()
    #mean_10 = data.收益率.rolling(window=10, center = False).mean()
    #mean_15 = data.收益率.rolling(window=15, center = False).mean()
    mean_30 = data.收益率.rolling(window=30, center = False).mean()
    mean_60 = data.收益率.rolling(window=60, center = False).mean()
    std_30 = data.收益率.rolling(window=30, center = False).std()
    std_60 = data.收益率.rolling(window=60, center = False).std()
    fig = plt.figure()
    data.收益率.plot()
    #mean_5.plot()
    #mean_10.plot()
    #mean_15.plot()
    mean_30.plot()
    mean_60.plot()
    fig.savefig("均线图.png")
    fig = plt.figure()
    #data.收益率.plot()
    std_30.plot(label="30std")
    std_60.plot(label="60std")
    plt.legend(loc="best")
    fig.savefig("标准差图.png")
    
    

if __name__ == "__main__":
    etf_total = pd.read_csv("total_etf.csv")
    etf_300 = pd.read_csv("300etf.csv")
    etf_nas = pd.read_csv("nasetf.csv")
    #print(etf_total.head())
    #print(etf_300.head())
    #print(etf_nas.head())
    Display(etf_total)
    MovementWindows(etf_total)
    
    
