
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

g_up_in    = 1 # 向上敲入
g_down_in  = 2 # 向下敲入
g_up_out   = 3 # 向上敲出
g_down_out = 4 # 向下敲出

class Config(object):
    def __init__(self, s, h, k, x, v, r, q, t, p, is_call, is_knock, is_kop_delay, barrier_type):
        self.s = s # 标的价格
        self.h = h # 障碍价格
        self.k = k # 行权价格
        self.x = x # 未触及障碍所需支付资金
        self.v = v # 波动率
        self.r = r # 无风险利率
        self.q = q # 年化分红率
        self.t = t # 年化到期期限
        self.p = p # 参与率，未敲出情况下客户对收益的占比要求
        self.is_call = is_call # 看涨看跌
        self.is_knock = is_knock # 是否已经敲入敲出
        self.is_kop_delay = is_kop_delay # 敲出后是立即还是延期支付资金
        self.barrier_type = barrier_type # 障碍类型

    def ToArgs(self):
        return self.__dict__

def Test_Barrier_Single():
    barrier = derivx.Barrier("Single")
    
    # Config(s, h, k, x, v, r, q, t, p, is_call, is_knock, is_kop_delay, barrier_type)
    
    # for s in [80.0, 82.0, 84.0, 86.0, 88.0, 90.0, 92.0, 94.0, 96.0, 98.0, 100.0, 102.0, 104.0]:
    #     #config = Config(s, 80.0, 100.0, 0.0, 0.3, 0.03, 0.02, 1.0, 1.0, True, False, False, g_down_in)
    #     #config = Config(s, 80.0, 100.0, 0.0, 0.3, 0.03, 0.02, 1.0, 1.0, True, False, False, g_down_out)
    #     #config = Config(s, 80.0, 100.0, 0.0, 0.3, 0.03, 0.02, 1.0, 1.0, False, False, False, g_down_in)
    #     config = Config(s, 80.0, 100.0, 0.0, 0.3, 0.03, 0.02, 1.0, 1.0, False, False, False, g_down_out)
    #     if barrier.InitArgs(config.ToArgs()) < 0:
    #         print(barrier.GetError())
    #         return
    #     try:
    #         price = barrier.CalcPrice()
    #         print(price)
    #     except Exception as e:
    #         print("计算价格发生异常！%s" % e)
    #         return
    
    args_cdo = [[90.0, 95.0, 0.25], [100.0, 95.0, 0.25], [110.0, 95.0, 0.25], [90.0, 100.0, 0.25], [100.0, 100.0, 0.25], [110.0, 100.0, 0.25],
                [90.0, 95.0, 0.30], [100.0, 95.0, 0.30], [110.0, 95.0, 0.30], [90.0, 100.0, 0.30], [100.0, 100.0, 0.30], [110.0, 100.0, 0.30]] # k, h, v
    for args in args_cdo:
        config = Config(100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, True, False, False, g_down_out)
        if barrier.InitArgs(config.ToArgs()) < 0:
            print(barrier.GetError())
            return
        try:
            price = barrier.CalcPrice()
            print(price)
        except Exception as e:
            print("cdo 计算价格发生异常！%s" % e)
            return
    
    args_cuo = [[90.0, 105.0, 0.25], [100.0, 105.0, 0.25], [110.0, 105.0, 0.25], [90.0, 105.0, 0.30], [100.0, 105.0, 0.30], [110.0, 105.0, 0.30]] # k, h, v
    for args in args_cuo:
        config = Config(100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, True, False, False, g_up_out)
        if barrier.InitArgs(config.ToArgs()) < 0:
            print(barrier.GetError())
            return
        try:
            price = barrier.CalcPrice()
            print(price)
        except Exception as e:
            print("cuo 计算价格发生异常！%s" % e)
            return
    
    args_cdi = [[90.0, 95.0, 0.25], [100.0, 95.0, 0.25], [110.0, 95.0, 0.25], [90.0, 100.0, 0.25], [100.0, 100.0, 0.25], [110.0, 100.0, 0.25],
                [90.0, 95.0, 0.30], [100.0, 95.0, 0.30], [110.0, 95.0, 0.30], [90.0, 100.0, 0.30], [100.0, 100.0, 0.30], [110.0, 100.0, 0.30]] # k, h, v
    for args in args_cdi:
        config = Config(100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, True, False, False, g_down_in)
        if barrier.InitArgs(config.ToArgs()) < 0:
            print(barrier.GetError())
            return
        try:
            price = barrier.CalcPrice()
            print(price)
        except Exception as e:
            print("cdi 计算价格发生异常！%s" % e)
            return
    
    args_cui = [[90.0, 105.0, 0.25], [100.0, 105.0, 0.25], [110.0, 105.0, 0.25], [90.0, 105.0, 0.30], [100.0, 105.0, 0.30], [110.0, 105.0, 0.30]] # k, h, v
    for args in args_cui:
        config = Config(100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, True, False, False, g_up_in)
        if barrier.InitArgs(config.ToArgs()) < 0:
            print(barrier.GetError())
            return
        try:
            price = barrier.CalcPrice()
            print(price)
        except Exception as e:
            print("cui 计算价格发生异常！%s" % e)
            return
    
    args_pdo = [[90.0, 95.0, 0.25], [100.0, 95.0, 0.25], [110.0, 95.0, 0.25], [90.0, 100.0, 0.25], [100.0, 100.0, 0.25], [110.0, 100.0, 0.25],
                [90.0, 95.0, 0.30], [100.0, 95.0, 0.30], [110.0, 95.0, 0.30], [90.0, 100.0, 0.30], [100.0, 100.0, 0.30], [110.0, 100.0, 0.30]] # k, h, v
    for args in args_pdo:
        config = Config(100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, False, False, False, g_down_out)
        if barrier.InitArgs(config.ToArgs()) < 0:
            print(barrier.GetError())
            return
        try:
            price = barrier.CalcPrice()
            print(price)
        except Exception as e:
            print("pdo 计算价格发生异常！%s" % e)
            return
    
    args_puo = [[90.0, 105.0, 0.25], [100.0, 105.0, 0.25], [110.0, 105.0, 0.25], [90.0, 105.0, 0.30], [100.0, 105.0, 0.30], [110.0, 105.0, 0.30]] # k, h, v
    for args in args_puo:
        config = Config(100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, False, False, False, g_up_out)
        if barrier.InitArgs(config.ToArgs()) < 0:
            print(barrier.GetError())
            return
        try:
            price = barrier.CalcPrice()
            print(price)
        except Exception as e:
            print("puo 计算价格发生异常！%s" % e)
            return
    
    args_pdi = [[90.0, 95.0, 0.25], [100.0, 95.0, 0.25], [110.0, 95.0, 0.25], [90.0, 100.0, 0.25], [100.0, 100.0, 0.25], [110.0, 100.0, 0.25],
                [90.0, 95.0, 0.30], [100.0, 95.0, 0.30], [110.0, 95.0, 0.30], [90.0, 100.0, 0.30], [100.0, 100.0, 0.30], [110.0, 100.0, 0.30]] # k, h, v
    for args in args_pdi:
        config = Config(100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, False, False, False, g_down_in)
        if barrier.InitArgs(config.ToArgs()) < 0:
            print(barrier.GetError())
            return
        try:
            price = barrier.CalcPrice()
            print(price)
        except Exception as e:
            print("pdi 计算价格发生异常！%s" % e)
            return
    
    args_pui = [[90.0, 105.0, 0.25], [100.0, 105.0, 0.25], [110.0, 105.0, 0.25], [90.0, 105.0, 0.30], [100.0, 105.0, 0.30], [110.0, 105.0, 0.30]] # k, h, v
    for args in args_pui:
        config = Config(100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, False, False, False, g_up_in)
        if barrier.InitArgs(config.ToArgs()) < 0:
            print(barrier.GetError())
            return
        try:
            price = barrier.CalcPrice()
            print(price)
        except Exception as e:
            print("pui 计算价格发生异常！%s" % e)
            return
    
    # Config(s, h, k, x, v, r, q, t, p, is_call, is_knock, , is_kop_delay, barrier_type)
    
    config_list = []
    
    config_list.append(Config(100.0, 0.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, True, False, False, g_down_out)) # s - k = 10.0
    config_list.append(Config(100.0, 0.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, True, True, False, g_down_out)) # x = 3.0
    config_list.append(Config(100.0, 0.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, False, False, False, g_down_out)) # k - s = 15.0
    config_list.append(Config(100.0, 0.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, False, True, False, g_down_out)) # x = 3.0
    
    config_list.append(Config(100.0, 0.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, True, False, False, g_up_out)) # s - k = 10.0
    config_list.append(Config(100.0, 0.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, True, True, False, g_up_out)) # x = 3.0
    config_list.append(Config(100.0, 0.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, False, False, False, g_up_out)) # k - s = 15.0
    config_list.append(Config(100.0, 0.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, False, True, False, g_up_out)) # x = 3.0
    
    config_list.append(Config(100.0, 0.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, True, False, False, g_down_in)) # x = 3.0
    config_list.append(Config(100.0, 0.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, True, True, False, g_down_in)) # s - k = 10.0
    config_list.append(Config(100.0, 0.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, False, False, False, g_down_in)) # x = 3.0
    config_list.append(Config(100.0, 0.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, False, True, False, g_down_in)) # k - s = 15.0
    
    config_list.append(Config(100.0, 0.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, True, False, False, g_up_in)) # x = 3.0
    config_list.append(Config(100.0, 0.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, True, True, False, g_up_in)) # s - k = 10.0
    config_list.append(Config(100.0, 0.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, False, False, False, g_up_in)) # x = 3.0
    config_list.append(Config(100.0, 0.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, False, True, False, g_up_in)) # k - s = 15.0
    
    for config in config_list:
        if barrier.InitArgs(config.ToArgs()) < 0:
            print(barrier.GetError())
            return
        try:
            payoff = barrier.CalcPayoff()
            print(payoff)
        except Exception as e:
            print("计算损益发生异常！%s" % e)
            return

if __name__ == "__main__":
    Test_Barrier_Single()
