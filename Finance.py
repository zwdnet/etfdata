# -*- coding:utf-8 -*-
# 进行相关金融分析
#参考《Python金融实战》

import pandas as pd
from scipy import stats
import scipy as sp


if __name__ == "__main__":
    etf_total = pd.read_csv("total_etf.csv")
    etf_300 = pd.read_csv("300etf.csv")
    etf_nas = pd.read_csv("nasetf.csv")
    #t检验，看投资总收益率均数是否为0
    print(stats.ttest_1samp(etf_total.收益率, 0.0))
    #比较两个指数的相关性
    print(sp.stats.bartlett(etf_300.close, etf_nas.close))
    