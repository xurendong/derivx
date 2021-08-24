
# -*- coding: utf-8 -*-

# Copyright (c) 2021-2021 the DerivX authors
# All rights reserved.
#
# The project sponsor and lead author is Xu Rendong.
# E-mail: xrd@ustc.edu, QQ: 277195007, WeChat: xrd_ustc
# See the contributors file for names of other contributors.
#
# Commercial use of this code in source and binary forms is
# governed by a LGPL v3 license. You may get a copy from the
# root directory. Or else you should get a specific written 
# permission from the project author.
#
# Individual and educational use of this code in source and
# binary forms is governed by a 3-clause BSD license. You may
# get a copy from the root directory. Certainly welcome you
# to contribute code of all sorts.
#
# Be sure to retain the above copyright notice and conditions.

import derivx

class Config_CashOrNothing(object):
    def __init__(self):
        self.s = 0.0 # 标的价格
        self.k = 0.0 # 行权价格
        self.r = 0.0 # 无风险利率
        self.q = 0.0 # 年化分红率
        self.sigma = 0.0 # 波动率
        self.t = 0.0 # 年化到期期限
        self.cash = 0.0 # 现金回报
        self.is_call = True # 看涨看跌

    def ToArgs(self):
        return self.__dict__

class Config_AssetOrNothing(object):
    def __init__(self):
        self.s = 0.0 # 标的价格
        self.k = 0.0 # 行权价格
        self.r = 0.0 # 无风险利率
        self.q = 0.0 # 年化分红率
        self.sigma = 0.0 # 波动率
        self.t = 0.0 # 年化到期期限
        self.is_call = True # 看涨看跌

    def ToArgs(self):
        return self.__dict__

class Config_SuperShare(object):
    def __init__(self):
        self.s = 0.0 # 标的价格
        self.k_l = 0.0 # 低端行权价格
        self.k_h = 0.0 # 高端行权价格
        self.r = 0.0 # 无风险利率
        self.q = 0.0 # 年化分红率
        self.sigma = 0.0 # 波动率
        self.t = 0.0 # 年化到期期限

    def ToArgs(self):
        return self.__dict__

def Test_Digital_Simple():
    digital = derivx.Digital("CashOrNothing")
    
    config = Config_CashOrNothing()
    config.s = 100.0 # 标的价格
    config.k = 80.0 # 行权价格
    config.r = 0.06 # 无风险利率
    config.q = 0.06 # 年化分红率
    config.sigma = 0.35 # 波动率
    config.t = 0.75 # 年化到期期限
    config.cash = 10.0 # 现金回报
    
    config.is_call = False # 看涨看跌
    if digital.InitArgs(config.ToArgs()) < 0:
        print(digital.GetError())
        return
    print("price:", digital.CalcPrice())
    
    config.is_call = True # 看涨看跌
    if digital.InitArgs(config.ToArgs()) < 0:
        print(digital.GetError())
        return
    print("payoff:", digital.CalcPayoff())
    
    ##################################################
    
    digital = derivx.Digital("AssetOrNothing")
    
    config = Config_AssetOrNothing()
    config.s = 70.0 # 标的价格
    config.k = 65.0 # 行权价格
    config.r = 0.07 # 无风险利率
    config.q = 0.05 # 年化分红率
    config.sigma = 0.27 # 波动率
    config.t = 0.5 # 年化到期期限
    
    config.is_call = False # 看涨看跌
    if digital.InitArgs(config.ToArgs()) < 0:
        print(digital.GetError())
        return
    print("price:", digital.CalcPrice())
    
    config.is_call = True # 看涨看跌
    if digital.InitArgs(config.ToArgs()) < 0:
        print(digital.GetError())
        return
    print("payoff:", digital.CalcPayoff())
    
    ##################################################
    
    digital = derivx.Digital("SuperShare")
    
    config = Config_SuperShare()
    config.s = 100.0 # 标的价格
    config.k_l = 90.0 # 低端行权价格
    config.k_h = 110.0 # 高端行权价格
    config.r = 0.1 # 无风险利率
    config.q = 0.1 # 年化分红率
    config.sigma = 0.2 # 波动率
    config.t = 0.25 # 年化到期期限
    
    if digital.InitArgs(config.ToArgs()) < 0:
        print(digital.GetError())
        return
    print("price:", digital.CalcPrice())
    
    if digital.InitArgs(config.ToArgs()) < 0:
        print(digital.GetError())
        return
    print("payoff:", digital.CalcPayoff())

if __name__ == "__main__":
    Test_Digital_Simple()
