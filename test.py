# -*- coding:utf-8 -*-
# 用Python分析etf数据
#作者:赵瑜敏 zwdnet@163.com

import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt


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
    return (df_300, df_nas)
    
    
#主程序
if __name__ == "__main__":
    # 导入数据
    etfdata = ImportData("etfdata.csv")
    print(etfdata)
    # 探索数据
    ExploreData(etfdata)
    # 分离数据
    (df_300, df_nas) = DivData(etfdata)
    print(df_300)
    print(df_nas)
    #描述数据
    print(df_300.describe())
    print(df_nas.describe())
    x = df_300["成交日期"]
    #plt.figure() 
    plt.plot(df_300["成交均价"])
    plt.plot(df_nas["成交均价"])
    plt.savefig("成交均价.png")
    
