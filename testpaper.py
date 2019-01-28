# -*- coding:utf-8 -*-
# 测试这篇文章的 
# https://zhuanlan.zhihu.com/p/55425806

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

import tushare as ts


#获取数据
def get_data(code, start_date = '2009-01-01',  end_date = '2019-01-25'):
    df = ts.get_k_data(code, start = start_date, end = end_date)
    df.index = pd.to_datetime(df.date)
    return df.close
    
    
#计算最大回撤
def max_drawdown(df):
    md = ((df.cummax() - df)/df.cummax()).max()
    return round(md, 4)
    
    
if __name__ == "__main__":
    stocks = {'sh':'上证综指', 
    '600519':'贵州茅台',
    '601398':'工商银行',
    '601318':'中国平安'}
    start_date = "2009-01-01"
    end_date = '2019-01-18'
    df = pd.DataFrame()
    
    for code, name in stocks.items():
        df[name] = get_data(code, start_date, end_date)
        #print(name, df[name].isnull().value_counts())
#        df[name].fillna(method = "ffill")
#        print(name, df[name].isnull().value_counts())
        
        
    #print(df['上证综指'])
    df_new = df/df.iloc[0]
    print(df_new.head())
    #绘图
    fig = plt.figure()
    df_new.plot(figsize=(16,7))
    #my_ticks = pd.date_range(start_date, end_date, freq = 'Y')
    #plt.xticks(my_ticks)
    plt.savefig("test1.png")
    
    #区间累积收益率
    #print(df_new.iloc[-1])
    total_ret = df_new.iloc[-1] - 1
    print(total_ret)
    TR = pd.DataFrame(total_ret.values, columns = ["累积收益率"], index = total_ret.index)
    print(TR)
    md = {}
    for code, name in stocks.items():
        md[name] = max_drawdown(df_new[name])
    #md = max_drawdown(df_new)
    MD = pd.DataFrame(md, index = ["最大回撤"])
    print(MD)
    #用前值替代缺失值
    rets = (df.fillna(method = 'pad')).apply(lambda x:x/x.shift(1) - 1)[1:]
    print(df.head())
    print(rets.head())
    #print((df/df.shift(1)-1)[1:])
    #计算α和β值
    #基准指数为x, 个股收益率为y
    x = rets.iloc[:, 0].values
    y = rets.iloc[:,1:].values
    AB = pd.DataFrame()
    alpha = []
    beta = []
    for i in range(3):
        b,a,r_value,p_value,std_err = stats.linregress(x, y[:, i])
        #α转化为年化的
        alpha.append(round(a*250, 3))
        beta.append(round(b, 3))
    AB["alpha"] = alpha
    AB["beta"] = beta
    AB.index = rets.columns[1:]
    print(AB)
    #夏普比例
    exReturn = rets - 0.03/250
    sharperatio = np.sqrt(len(exReturn))*exReturn.mean()/exReturn.std()
    SHR = pd.DataFrame(sharperatio, columns = ["夏普比率"])
    print(SHR)
    #计算信息比率
    ex_return = pd.DataFrame()
    ex_return['贵州茅台'] = rets.iloc[:,1] - rets.iloc[:,0]
    ex_return['工商银行'] = rets.iloc[:,2] - rets.iloc[:,0]
    ex_return['中国平安'] = rets.iloc[:,3] - rets.iloc[:,0]
    information = np.sqrt(len(ex_return))*ex_return.mean()/ex_return.std()
    INR = pd.DataFrame(information, columns = ['信息比率'])
    print(INR)
    indicators = pd.concat([TR,MD,AB,SHR,INR], axis = 1, join = 'outer')
    print(indicators.round(3))
