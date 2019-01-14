# -*- coding:utf8 -*-
#对转换好的数据进行数据分析

import pandas as pd



if __name__ == "__main__":
    etf_total = pd.read_csv("total_etf.csv")
    etf_300 = pd.read_csv("300etf.csv")
    etf_nas = pd.read_csv("nasetf.csv")
    print(etf_total.head())
    print(etf_300.head())
    print(etf_nas.head())
    