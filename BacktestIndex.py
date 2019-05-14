# -*- coding:utf-8 -*-
# 计算回测指标 重写 用已经计算好的年化收益率来计算


import pandas as pd
import numpy as np
from scipy import stats


class GetIndex(object):
    # data: 策略每天的年化收益率
    # 有两列策略，
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
        self.AB = pd.DataFrame()
        self.AB["alpha"] = [a]
        self.AB["beta"] = [b]
        print(a,b)
        return self.AB
        
        
    # 夏普比例
    def sharp(self):
        pass
        
        
    # 信息比例
    def information(self):
        pass
        
        
    # 合并回测策略
    def combine(self):
        pass
        
        
    # 计算回测策略
    def run(self):
        pass


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