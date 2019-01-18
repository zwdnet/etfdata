# -*- coding:utf-8 -*-
# 进行相关金融分析
#参考《Python金融实战》

import pandas as pd


if __name__ == "__main__":
    etf_total = pd.read_csv("total_etf.csv")
    etf_300 = pd.read_csv("300etf.csv")
    etf_nas = pd.read_csv("nasetf.csv")
    