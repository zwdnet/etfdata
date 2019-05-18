# -*- coding:utf-8 -*-
# 计算回测指标 重写 用已经计算好的年化收益率来计算


import pandas as pd
import numpy as np
from scipy import stats


class GetIndex(object):
    # data: 策略每天的年化收益率
    # 有两列数据，
    # 一列为市场，市场的基准收益，
    # 一列为策略，为我们的策略收益
    def __init__(self, data):
        self.data = data    #每天的年化收益率
        self.MD = 0.0 #最大回撤
        self.AB = 0.0 #αβ值
        self.SHR = 0.0 #夏普比例
        self.INR = 0.0 #信息比例
        self.indicators = 0.0 #合并的回测结果


    # 最大回撤
    def max_drawdown(self):
        md=((self.data.cummax()-self.data)/self.data.cummax()).max()
        self.MD = pd.DataFrame(md.values, columns=["最大回撤"], index = md.index)
        return self.MD
        
        
    # αβ值
    def alpha_beta(self):
        x = self.data["市场"].values
        y = self.data["策略"].values
        b,a,r_value,p_value,std_err=stats.linregress(x, y)        
        self.AB = pd.DataFrame([a], columns = ["alpha"], index = ["策略"])
        self.AB["beta"] = [b]
        print(self.AB)
        return self.AB
        
        
    # 夏普比例
    def sharp(self):
        # 无风险年化收益率3%
        exReturn = self.data - 0.03
        sharperatio=np.sqrt(len(exReturn))*exReturn.mean()/exReturn.std()
        self.SHR=pd.DataFrame(sharperatio, columns=["夏普比例"])
        return self.SHR
        
        
    # 信息比例
    def information(self):
        ex_return = pd.DataFrame()
        ex_return = self.data.iloc[:,1] - self.data.iloc[:,0]
        information=np.sqrt(len(ex_return))*ex_return.mean()/ex_return.std()
        self.INR=pd.DataFrame([information],columns=['信息比率'], index = ["策略"])
        return self.INR
        
        
    # 合并回测策略
    def combine(self):
        self.indicators=pd.concat([self.MD, self.AB, self.SHR, self.INR], axis=1, join='outer')
        return self.indicators
        
        
    # 计算回测策略
    def run(self):
        self.max_drawdown()
        self.alpha_beta()
        self.sharp()
        self.information()
        self.combine()
        print(self.MD)
        print(self.AB)
        print(self.SHR)
        print(self.INR)
        return self.indicators


if __name__ == "__main__":
    data1 = [1, -3, -5, 3, -8, 6, 5]
    data2 = [2,-100, 3, 7, -5, -7, 9]
    d = {"市场":data1, "策略":data2}
    data = pd.DataFrame(d)
    print(data)
    print(data.cummax())
    index = GetIndex(data)
    md = index.max_drawdown()
    print(md)
    print(data["市场"].values, data["策略"].values)
    a= np.var(data["市场"].values)
    b=np.cov(data["策略"].values, data["市场"].values)
    beta = b[0][1]/a
    print(beta)
    B,A,r_value,p_value,std_err=stats.linregress(data["市场"].values, data["策略"].values)
    print(B)
    ab = index.alpha_beta()
    print(ab)
    
    shr = index.sharp()
    print(shr)
    
    print(data)
    print(data.iloc[:,0])
    print(data.iloc[:,1])
    
    inf = index.information()
    print(inf)
    
    indicators = index.run()
    print(indicators)