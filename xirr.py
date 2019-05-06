# -*- coding:utf-8 -*-
# 计算定投年化收益率的程序
# 直接从github上抄的
# https://github.com/peliot/XIRR-and-XNPV/edit/master/financial.py


import datetime
from scipy import optimize 
from random import random
import pandas as pd


def secant_method(tol, f, x0):
    """
    Solve for x where f(x)=0, given starting x0 and tolerance.
    
    Arguments
    ----------
    tol: tolerance as percentage of final result. If two subsequent x values are with tol percent, the function will return.
    f: a function of a single variable
    x0: a starting value of x to begin the solver

    Notes
    ------
    The secant method for finding the zero value of a function uses the following formula to find subsequent values of x. 
    
    x(n+1) = x(n) - f(x(n))*(x(n)-x(n-1))/(f(x(n))-f(x(n-1)))
    
    Warning 
    --------
    This implementation is simple and does not handle cases where there is no solution. Users requiring a more robust version should use scipy package optimize.newton.

    """

    x1 = x0*1.1
    while (abs(x1-x0)/abs(x1) > tol):
        x0, x1 = x1, x1-f(x1)*(x1-x0)/(f(x1)-f(x0))
    return x1


def xnpv(rate,cashflows):
    """
    Calculate the net present value of a series of cashflows at irregular intervals.

    Arguments
    ---------
    * rate: the discount rate to be applied to the cash flows
    * cashflows: a list object in which each element is a tuple of the form (date, amount), where date is a python datetime.date object and amount is an integer or floating point number. Cash outflows (investments) are represented with negative amounts, and cash inflows (returns) are positive amounts.
    
    Returns
    -------
    * returns a single value which is the NPV of the given cash flows.

    Notes
    ---------------
    * The Net Present Value is the sum of each of cash flows discounted back to the date of the first cash flow. The discounted value of a given cash flow is A/(1+r)**(t-t0), where A is the amount, r is the discout rate, and (t-t0) is the time in years from the date of the first cash flow in the series (t0) to the date of the cash flow being added to the sum (t).  
    * This function is equivalent to the Microsoft Excel function of the same name. 

    """

    chron_order = sorted(cashflows, key = lambda x: x[0])
    t0 = chron_order[0][0] #t0 is the date of the first cash flow

    return sum([cf/(1+rate)**((t-t0).days/365.0) for (t,cf) in chron_order])
    

def xirr(cashflows,guess=0.1):
    """
    Calculate the Internal Rate of Return of a series of cashflows at irregular intervals.

    Arguments
    ---------
    * cashflows: a list object in which each element is a tuple of the form (date, amount), where date is a python datetime.date object and amount is an integer or floating point number. Cash outflows (investments) are represented with negative amounts, and cash inflows (returns) are positive amounts.
    * guess (optional, default = 0.1): a guess at the solution to be used as a starting point for the numerical solution. 

    Returns
    --------
    * Returns the IRR as a single value
    
    Notes
    ----------------
    * The Internal Rate of Return (IRR) is the discount rate at which the Net Present Value (NPV) of a series of cash flows is equal to zero. The NPV of the series of cash flows is determined using the xnpv function in this module. The discount rate at which NPV equals zero is found using the secant method of numerical solution. 
    * This function is equivalent to the Microsoft Excel function of the same name.
    * For users that do not have the scipy module installed, there is an alternate version (commented out) that uses the secant_method function defined in the module rather than the scipy.optimize module's numerical solver. Both use the same method of calculation so there should be no difference in performance, but the secant_method function does not fail gracefully in cases where there is no solution, so the scipy.optimize.newton version is preferred.

    """
    
    #return secant_method(0.0001,lambda r: xnpv(r,cashflows),guess)
    return optimize.newton(lambda r: xnpv(r,cashflows),guess)


if __name__ == "__main__":
    # short = [(datetime.date(2000, 6, 9), 2500.0), (datetime.date(2000, 6, 9), -2500.0)]
    short = [
    (datetime.date(2017, 11, 21), -300.00),
    (datetime.date(2017, 12, 21), -400.00),
    (datetime.date(2018, 1, 4), -225.00),
    (datetime.date(2018, 1, 16), -400.00),
    (datetime.date(2018, 1, 16), 88.00),
    (datetime.date(2018, 1, 18), -400.00),
    (datetime.date(2018, 1, 22), 1680.00)
    ]
    ret = xirr(short)
    print(ret)
    
    beginDate = datetime.date(2018,1,1)
    timedelta = datetime.timedelta(days = 1)
    #print(beginDate)
#    print(timedelta)
#    print(beginDate + timedelta)
    now = beginDate
    cost = 0.0
    money = 1000
    freq = 10
    money_rem = 0.0
    price = 1.0
    feeRate = 0.0003
    stocks = 0
    value = 0.0
    data = []
    for day in range(365):
        now = now + timedelta
        # print(now)
        r = random()
        if r < 0.5:
            price = price - 0.01
            if price < 0.0:
                price = 0.0
        else:
            price = price + 0.01
        if day % freq == 0:
            money = money + money_rem
            money_rem = 0
            num = int(money/price/100)*100
            fee = num*price*feeRate
            if fee < 0.1:
                fee = 0.1
            if num*price + fee <= money:
                num = num
            elif num >= 200:
                if (num - 100)*price <= money:
                    num = num - 100
                else:
                    num = 0
            cost = num*price + fee
            stocks += num
            value = stocks*price
            money_rem = money - cost
            data.append((now, cost*(-1.0)))
    
    value = stocks*price
    print(stocks, value)
    data.append((now, value))
    print(data)
    xirr_res = xirr(data)
    print(xirr_res)
    file = pd.DataFrame(data, columns=["日期", "金额"])
    file.to_csv("xirr_test.csv")
    
            