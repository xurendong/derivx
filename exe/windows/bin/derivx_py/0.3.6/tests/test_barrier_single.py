
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

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import derivx

g_up_in    = 1 # 向上敲入
g_down_in  = 2 # 向下敲入
g_up_out   = 3 # 向上敲出
g_down_out = 4 # 向下敲出

class Config(object):
    def __init__(self, s, h, k, x, v, r, q, t, p, is_call, is_kop_delay, barrier_type):
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
        self.is_kop_delay = is_kop_delay # 敲出后是立即还是延期支付资金
        self.barrier_type = barrier_type # 障碍类型
        
        self.calc_price = np.array([]) # 计算价格序列
        self.runs_step = 0 # 价格变动步数
        self.year_days = 0 # 年交易日数量
        self.run_from = 0 # 起始天数，第一天为零
        self.run_days = 0 # 运行天数

    def ToArgs(self):
        return self.__dict__

def FigureResult(config, result):
    figure = plt.figure()
    ax = Axes3D(figure)
    #ax = Axes3D(figure, auto_add_to_figure = False)
    #figure.add_axes(ax)
    x = np.arange(0, config.runs_step, 1)
    y = config.calc_price
    X, Y = np.meshgrid(x, y)
    ax.plot_surface(X, Y, result, rstride = 1, cstride = 1, cmap = plt.get_cmap("rainbow"))
    plt.show()

def ExportResult(config, result, file_path):
    export_days = config.run_days
    if export_days > 255: # Excel 最大 256 列，首列显示价格，剩余可用 255 列
        export_days = 255
        print("提示：Excel 最大 256 列，剩余 %d 列数据未作导出！" % (config.run_days - 255))
    df_result = pd.DataFrame(result[:, config.run_from : (config.run_from + export_days)]).iloc[::-1] # 上下倒下顺序
    df_result.index = config.calc_price[::-1]
    df_result.columns = ["day_%d" % (days + 1) for days in np.arange(config.run_from, config.run_from + export_days, 1)]
    df_result.to_excel(file_path, sheet_name = "result")
    print("导出结果：%s" % file_path)

def Test_Barrier_Single():
    barrier = derivx.Barrier("Single")
    
    # Config(s, h, k, x, v, r, q, t, p, is_call, is_kop_delay, barrier_type)
    
    # for s in [80.0, 82.0, 84.0, 86.0, 88.0, 90.0, 92.0, 94.0, 96.0, 98.0, 100.0, 102.0, 104.0]:
    #     #config = Config(s, 80.0, 100.0, 0.0, 0.3, 0.03, 0.02, 1.0, 1.0, True, False, g_down_in)
    #     #config = Config(s, 80.0, 100.0, 0.0, 0.3, 0.03, 0.02, 1.0, 1.0, True, False, g_down_out)
    #     #config = Config(s, 80.0, 100.0, 0.0, 0.3, 0.03, 0.02, 1.0, 1.0, False, False, g_down_in)
    #     config = Config(s, 80.0, 100.0, 0.0, 0.3, 0.03, 0.02, 1.0, 1.0, False, False, g_down_out)
    #     if barrier.InitArgs(config.ToArgs()) < 0:
    #         print(barrier.GetError())
    #         return
    #     try:
    #         price = barrier.CalcPrice()
    #         print(price)
    #     except Exception as e:
    #         print("计算价格发生异常！%s" % e)
    #         return
    
    """
    args_cdo = [[90.0, 95.0, 0.25], [100.0, 95.0, 0.25], [110.0, 95.0, 0.25], [90.0, 100.0, 0.25], [100.0, 100.0, 0.25], [110.0, 100.0, 0.25],
                [90.0, 95.0, 0.30], [100.0, 95.0, 0.30], [110.0, 95.0, 0.30], [90.0, 100.0, 0.30], [100.0, 100.0, 0.30], [110.0, 100.0, 0.30]] # k, h, v
    for args in args_cdo:
        config = Config(100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, True, False, g_down_out)
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
        config = Config(100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, True, False, g_up_out)
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
        config = Config(100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, True, False, g_down_in)
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
        config = Config(100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, True, False, g_up_in)
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
        config = Config(100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, False, False, g_down_out)
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
        config = Config(100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, False, False, g_up_out)
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
        config = Config(100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, False, False, g_down_in)
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
        config = Config(100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, False, False, g_up_in)
        if barrier.InitArgs(config.ToArgs()) < 0:
            print(barrier.GetError())
            return
        try:
            price = barrier.CalcPrice()
            print(price)
        except Exception as e:
            print("pui 计算价格发生异常！%s" % e)
            return
    """
    
    # Config(s, h, k, x, v, r, q, t, p, is_call, is_kop_delay, barrier_type)
    
    """
    config_list = []
    
    config_list.append(Config(100.0, 80.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, True, False, g_down_out)) # 未敲出 s - k = 10.0
    config_list.append(Config(100.0, 120.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, True, False, g_down_out)) # 已敲出 x = 3.0
    config_list.append(Config(100.0, 80.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, False, False, g_down_out)) # 未敲出 k - s = 15.0
    config_list.append(Config(100.0, 120.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, False, False, g_down_out)) # 已敲出 x = 3.0
    
    config_list.append(Config(100.0, 120.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, True, False, g_up_out)) # 未敲出 s - k = 10.0
    config_list.append(Config(100.0, 80.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, True, False, g_up_out)) # 已敲出 x = 3.0
    config_list.append(Config(100.0, 120.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, False, False, g_up_out)) # 未敲出 k - s = 15.0
    config_list.append(Config(100.0, 80.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, False, False, g_up_out)) # 已敲出 x = 3.0
    
    config_list.append(Config(100.0, 80.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, True, False, g_down_in)) # 未敲入 x = 3.0
    config_list.append(Config(100.0, 120.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, True, False, g_down_in)) # 已敲入 s - k = 10.0
    config_list.append(Config(100.0, 80.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, False, False, g_down_in)) # 未敲入 x = 3.0
    config_list.append(Config(100.0, 120.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, False, False, g_down_in)) # 已敲入 k - s = 15.0
    
    config_list.append(Config(100.0, 120.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, True, False, g_up_in)) # 未敲入 x = 3.0
    config_list.append(Config(100.0, 80.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, True, False, g_up_in)) # 已敲入 s - k = 10.0
    config_list.append(Config(100.0, 120.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, False, False, g_up_in)) # 未敲入 x = 3.0
    config_list.append(Config(100.0, 80.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, False, False, g_up_in)) # 已敲入 k - s = 15.0
    
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
    """
    
    # Config(s, h, k, x, v, r, q, t, p, is_call, is_kop_delay, barrier_type)
    
    config = Config(100.0, 105.0, 101.0, 3.0, 0.2, 0.03, 0.05, 1.0, 1.0, True, True, g_up_out)
    #config = Config(100.0, 95.0, 99.0, 3.0, 0.2, 0.03, 0.05, 1.0, 1.0, False, True, g_down_out)
    
    calc_price_u = 115.0 # 价格点上界
    calc_price_d = 75.0 # 价格点下界
    calc_price_g = 1.0 # 价格点间隔
    #config.calc_price = np.array([65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0, 100.0, 105.0]) # 计算价格序列
    config.calc_price = np.arange(calc_price_d, calc_price_u + calc_price_g, calc_price_g) # 含价格点上下界
    
    config.runs_step = 244 # 价格变动步数
    config.year_days = 244 # 年交易日数量
    config.run_from = 0 # 起始天数，第一天为零
    config.run_days = 244 # 运行天数
    
    ret_cols = config.runs_step
    ret_rows = len(config.calc_price)
    
    if barrier.InitArgs(config.ToArgs()) < 0:
        print(barrier.GetError())
        return
    
    greek_flags = {"delta":"d"}
    #greek_flags = {"delta":"d", "gamma":"g", "vega":"v", "theta":"t", "rho":"r"}
    for name, flag in greek_flags.items():
        result = np.zeros((ret_rows, ret_cols))
        barrier.CalcGreeks(flag, result)
        FigureResult(config, result)
        ExportResult(config, result, "/export_greeks_%s.xls" % name)

if __name__ == "__main__":
    Test_Barrier_Single()
