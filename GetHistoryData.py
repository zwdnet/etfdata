# -*- coding:utf-8 -*-
# 获取历史数据

import tushare as ts
import os


#将八位数字的日期转换为yyyy-mm-dd
def TransfDate(d):
    year = int(d/10000)
    month = int((d - year*10000)/100)
    day = int((d - year*10000 - month*100))
    date = format("%4d-%02d-%02d" % (year, month, day))
    return date
    

#上面函数的逆操作，将日期转化为数字
def TransfDate2(s):
    year = int(s[0:4])
    month = int(s[5:7])    
    day = int(s[8:11])
    date = year*10000+month*100+day
    return date


# 获取历史数据
def GetHistoryData(Code, BeginTime, EndTime):
    df = ts.get_k_data(Code, index = False,  start = TransfDate(BeginTime), end = TransfDate(EndTime))
    return df
    
    
# 更新数据
def updateData(endTime):
    beginTime = 20130515
    if endTime <= beginTime:
        print("结束时间必须大于20130515，程序将结束。")
        os.exit(1)
        return
    etf300 = GetHistoryData("510300", beginTime, endTime)
    etfnas = GetHistoryData("513100", beginTime, endTime)
    #保存文件
    etf300.to_csv("df_300_hist.csv")
    etfnas.to_csv("df_nas_hist.csv")
    
    
if __name__ == "__main__":
    updateData(20190423)
    print("历史数据获取成功")
    
