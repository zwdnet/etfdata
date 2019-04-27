# -*- coding:utf-8 -*-
# 计算回测指标


import pandas as pd


#新建一个类来完成吧
class getIndex(object):
    def __init__(self, data):
        self.data = pd.DataFrame(data, columns = ["Income"])
        self.md = 0.00  # 最大回撤
    
    
    def max_drawdown(self):
       md = ((self.data.cummax() - self.data)).max()
       self.md = round(md, 4)
       print(self.data.cummax())
       
        