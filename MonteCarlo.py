# -*- coding:utf-8 -*-
#对数据用蒙特卡洛算法进行分析

import pandas as pd
import datetime
import numpy as np
import index
    
    
'''执行一次交易模拟
输入的参数
cost 总交易成本
time 交易周期的天数
freq 交易频率，几天交易一次
df_300, df_nas,分别为两个定投的etf的实盘成交数据
返回值为一个DataFrame，包含每个交易日的成本，收益，收益率等数据
'''
def work(cost, time, freq, df_300, df_nad):
    #计算交易次数
    tradetimes = int(time/freq)
    print(tradetimes)
    #计算每次交易的金额
    money = cost/tradetimes
    print(money)
    #把每次交易金额均分为两部分，分别买两个etf，如果钱不够交易，留到下次
    money_300 = money/2.0
    money_nas = money/2.0
    #开始模拟前定义相关变量
    money = [] #投入的总成本
    m3 = 0.0 #买300etf的钱
    mN = 0.0 #买纳指etf的钱
    fee = [] #手续费
    V3 = [] #300etf股票数量
    VN = [] #纳指etf股票数量
    Total3 = [] #300etf的当前市值
    TotalN = [] #纳指etf的当前市值
    Total = [] #当前总市值
    Income3 = [] #300etf的收益
    IncomeN = [] #nasetf的收益
    Rate3 = [] #300etf收益率
    RateN = [] #nasetf收益率
    Rate = [] #总收益率
    
    #开始模拟
    j = 0
    for i in range(time):
        if j == 0:   #交易
            
    
        

if __name__=="__main__":
    #实盘数据分析
    df_etf = pd.read_csv("total_etf.csv")
    df_300 = pd.read_csv("300etf.csv")
    df_nas = pd.read_csv("nasetf.csv")
    df_data = pd.DataFrame(
    {
    "数据":df_etf["收益率"].values
    }
    )
    df_base = pd.DataFrame(
    {
    "数据":df_300["close"].values
    }
    )
    result = index.index(df_data, df_base, 0.029)
    print(result)
    #进行模拟
    #先获取成本，交易周期等信息
    cost = df_etf["成本"].values[-1]
    print(cost)
    time = len(df_etf)
    #进行交易模拟
    work(cost, time, 10, df_300, df_nas)
    
    
