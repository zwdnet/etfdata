# -*- coding:utf-8 -*-
# 用Python分析etf数据
#作者:赵瑜敏 zwdnet@163.com

import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import tushare as ts


#从csv文件读入数据
def ImportData(FileName):
    df = pd.read_csv(FileName)
    return df
    
    
#探索数据
def ExploreData(Data):
    #每列的索引名称
    print(Data.columns)
    print(Data["成交金额"])
    print(Data.证券代码)
    #输出指定行的信息
    print(Data.ix[1])
    #返回Data的值
    print(Data.values)
    #对数据进行筛选
    print(Data[Data["证券名称"] == "300ETF"])
    
    
#分离数据:根据买入的etf的不同划分数据
def DivData(Data):
    df_300 = Data[Data["证券名称"] == "300ETF"]
    df_nas = Data[Data["证券名称"] == "纳指ETF"]
    #重置index
    df_300.index = range(len(df_300))
    df_nas.index = range(len(df_nas))
    return (df_300, df_nas)
    
 
#将八位数字的日期转换为yyyy-mm-dd
def TransfDate(d):
    year = int(d/10000)
    month = int((d - year*10000)/100)
    day = int((d - year*10000 - month*100))
    date = format("%4d-%02d-%02d" % (year, month, day))
    return date
    

#上面函数的逆操作，将日期转化为数字
def TransfDate2(s):
    year = int(s[0:4])
    month = int(s[5:7])    
    day = int(s[8:11])
    date = year*10000+month*100+day
    return date
    
    
#抓取历史数据
def GetHistoryData(Code, BeginTime, EndTime):
    df = ts.get_k_data(Code, index = False,  start = TransfDate(BeginTime), end = TransfDate(EndTime))
    return df
    
    
#测试数据，因为手工合并了同一天的多个
#交易数据，验证一下。
def TestData(data):
    i = 0
    v = data.成交量
    p = data.成交均价
    m1 = data.成交金额
    f = data.手续费
    m2 = data.发生金额
    for date in data.成交日期:
        a = v[i]*p[i]
        b = a + f[i]
        if m1[i] !=  a or m2[i] != b:
            print("日期%d的数据出错 %f %f %f %f"%(date, m1[i], a, m2[i], b))
        i = i+1
    print("测试完毕")
    
    
#根据投资记录和历史数据计算持仓收益率等数据。
def Calculator(inverstData, histData):
    i = 0
    j = 0
    vol = []    #持仓股票数量
    fee = []    #手续费
    money = []   #投资总额
    rate = []     #收益率
    time = []   #时间
    market = []  #股票市值
    
    for date in histData.date:
        d1 = TransfDate2(date)
        d2 = inverstData.成交日期[i]
        b = (d1 == d2)
        time.append(d1)
        #该日期有交易，改变数据
        if b == True:  
            if i == 0: #第一天，直接插
                vol.append(inverstData.成交量[i])
                fee.append(inverstData.手续费[i])
                money.append(inverstData.发生金额[i])
                market.append(vol[i]*histData.close[i])
                #计算收益率=市值/投资总额
                rate.append(market[i]/money[i] - 1.0)
            else: #不是第一天，但有交易
                 vol.append(vol[j-1] + inverstData.成交量[i])
                 fee.append(fee[j-1] + inverstData.手续费[i])
                 money.append(money[j-1] + inverstData.发生金额[i])
                 market.append(vol[j]*histData.close[j])
                 #计算收益率=市值/投资总额
                 rate.append(market[j]/money[j] -1.0)
            i = i+1
        else: #没有交易，复制上一天的数据
            vol.append(vol[j-1])
            fee.append(fee[j-1])
            money.append(money[j-1])
            market.append(vol[j]*histData.close[j])
            rate.append(market[j]/money[j] - 1.0)
        j = j+1
    data = pd.DataFrame({
    "日期":time,
    "持仓量":vol,
    "手续费":fee,
    "成本":money,
    "市值":market,
    "收益率":rate})
    return data
        
        
#合并两个数据，算出总的持仓收益率等数据
def MergeData(data1, data2, histData1, histData2):
    #合并日期，持仓金额，手续费,市值，并计算持仓收益率
    money = []   #成本
    fee = []          #手续费总额
    market = []   #总的股票市值
    rate = []         #总的收益率
    time = []        #日期
    i = 0
    for date in histData1.date:
        date = TransfDate2(date)
        time.append(date)
        money.append(data1.成本[i] + data2.成本[i])
        fee.append(data1.手续费[i] + data2.手续费[i])
        market.append(data1.市值[i] + data2.市值[i])
        #计算收益率
        rate.append(market[i]/money[i] - 1.0)
        i = i + 1
    data = pd.DataFrame({
    "日期":time,
    "成本":money,
    "手续费":fee,
    "市值":market,
    "收益率":rate
    })
    return data
        
    
    
#主程序
if __name__ == "__main__":
    # 导入数据
    etfdata = ImportData("etfdata.csv")
    #print(etfdata)
    # 探索数据
    #ExploreData(etfdata)
    # 分离数据
    (df_300, df_nas) = DivData(etfdata)
    #print(df_300)
    #print(df_nas)
    #描述数据
    #print(df_300.describe())
    #print(df_nas.describe())
    #print(df_300["成交日期"])
    plt.plot(df_300["成交均价"])
    plt.plot(df_nas["成交均价"])
    plt.savefig("成交均价.png")
    
    #找出最早开始定投的时间
    #beginTime = df_300.成交日期.min()
    #endTime = df_300.成交日期.max()
    #抓取历史价格数据
    #df_300_hist = GetHistoryData("510300", beginTime, endTime)
    #df_nas_hist = GetHistoryData("513100", beginTime, endTime)
    #保存到csv文件
    #df_300_hist.to_csv("300etf.csv")
    #df_nas_hist.to_csv("nasetf.csv")
    #上面运行一次就行了，以后从csv读取
    df_300_hist = pd.read_csv("300etf.csv")
    df_nas_hist = pd.read_csv("nasetf.csv")
    #print(df_300_hist)
    df_300_hist = df_300_hist.loc[0:len(df_300_hist), ["date", "close"]]
    df_nas_hist = df_nas_hist.loc[0:len(df_nas_hist), ["date", "close"]]
    #print(df_300_hist)
    #TestData(df_300)
    #TestData(df_nas)
    data_300 = Calculator(df_300, df_300_hist)
    data_nas = Calculator(df_nas, df_nas_hist)
    #将收益率数据合并，算出总的持仓数据
    data_total = MergeData(data_300, data_nas, df_300_hist, df_nas_hist)
    data_total.to_csv("total_etf.csv")
    plt.figure()
    plt.plot(data_300.收益率, label = "300etf")
    plt.plot(data_nas.收益率, label = "nasetf")
    plt.plot(data_total.收益率, label = "etf")
    plt.legend(loc = "upper right")
    plt.savefig("收益率.png")
    
    
    
