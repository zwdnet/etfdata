# -*- coding:utf-8 -*-
# 计算回测指标
# 参考:https://zhuanlan.zhihu.com/p/55425806


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tushare as ts
import time
from scipy import stats


#新建一个类来完成吧
class getIndex(object):
    def __init__(self, data):
        self.data = pd.DataFrame(data, columns = ["Income"])
        self.md = 0.00  # 最大回撤
    
    # 直接根据收益率算最大回撤
    def max_drawdownRate(self):
       md = ((self.data.cummax() - self.data)).max()
       self.md = round(md, 4)
       print(self.data.cummax())
       
       
    # 数据1 累积收益率 年化收益率
    def total_ret(self, data):
        total_ret = data.iloc[-1] - 1.0
        ar = (1+total_ret)**(250/len(data)) - 1.0
        TR=pd.DataFrame(total_ret.values, columns=['累计收益率'],index=total_ret.index)
        AR=pd.DataFrame(ar.values, columns=["年化收益率"], index=ar.index)
        
        return (TR, AR)
       
       
    # 数据2 最大回撤
    def max_drawdown(self, data):
        md=((df.cummax()-df)/df.cummax()).max()
        MD = pd.DataFrame(md.values, columns=["最大回撤"], index = md.index)
        return MD
        
    # 数据3 αβ值
    def alpha_beta(self, rets):
        #市场指数为x，个股收益率为y
        x=rets.iloc[:,0].values
        y=rets.iloc[:,1:].values
        AB = pd.DataFrame()
        alpha = []
        beta = []
        for i in range(3):
            b,a,r_value,p_value,std_err=stats.linregress(x,y[:,i])
            alpha.append(round(a*250,3))
            beta.append(round(b,3))
        AB["alpha"] = alpha
        AB["beta"] = beta
        AB.index = rets.columns[1:]
        return AB
        
        
    # 数据4 夏普比例
    def sharp(self, rets):
        #超额收益率以无风险收益率为基准
        #假设无风险收益率为年化3%
        exReturn=rets-0.03/250
        sharperatio=np.sqrt(len(exReturn))*exReturn.mean()/exReturn.std()
        SHR=pd.DataFrame(sharperatio, columns=["夏普比例"])
        return SHR
        
        
    # 数据5 信息比例
    def information(self, rets):
        #超额收益率以无风险收益率为基准
        #假设无风险收益率为年化3%
        ex_return=pd.DataFrame()
        ex_return['贵州茅台']=rets.iloc[:,1]-rets.iloc[:,0]
        ex_return['工商银行']=rets.iloc[:,2]-rets.iloc[:,0]
        ex_return['中国平安']=rets.iloc[:,3]-rets.iloc[:,0]
        information=np.sqrt(len(ex_return))*ex_return.mean()/ex_return.std()
        INR=pd.DataFrame(information,columns=['信息比率'])
        return INR
       
       
# 获取股价信息
def get_data(code,start_date="2009-01-01", end_date="2019-01-18"):
    df = ts.get_k_data(code, index=False,  start=start_date, end=end_date)
    time.sleep(1)
    df.index=pd.to_datetime(df.date)
    return df.close
       
       
# 测试程序
if __name__ == "__main__":
       stocks={'sh':'上证综指',
       '600519':'贵州茅台',
       '601398':'工商银行',
       '601318':'中国平安'}
       df = pd.DataFrame()
       for code, name in stocks.items():
           df[name] = get_data(code)
           #filename = name+".csv"
           # df[name].to_csv(filename)
           #df[name] = pd.read_csv(filename)
            
       df_new = df/df.iloc[0]
       df_new.plot(figsize = (16, 7))
       my_ticks = pd.date_range('2008-01-01','2019-01-18',freq='M')
       plt.xticks(my_ticks, fontsize = 12)
       ax=plt.gca()
       ax.spines['right'].set_color('none')
       ax.spines['top'].set_color('none')
       plt.savefig("index.png")
       
       index = getIndex(df_new)
       
       TR,AR = index.total_ret(df_new)
       print(TR)
       print(AR)
       
       MD = index.max_drawdown(df_new)
       print(MD)
       
       rets=(df.fillna(method='pad')).apply(lambda x:x/x.shift(1)-1)[1:]
       AB = index.alpha_beta(rets)
       print(AB)
       
       SHR = index.sharp(rets)
       print(SHR)
       
       INR = index.information(rets)
       print(INR)
       
       indicators=pd.concat([TR,AR, MD,AB,SHR,INR],axis=1,join='outer')
       
       print(indicators)
