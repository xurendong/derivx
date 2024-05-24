
# -*- coding: utf-8 -*-

# Copyright (c) 2021-2023 the DerivX authors
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

# 示例说明：
# 1、演示单障碍奇异期权理论价格、收益情况、希腊值等的计算；
# 2、演示通过 Create 方法获取执行模块实例；
# 3、演示 直接模式 DirectCalc 任务执行调用；
# 4、演示任务参数序列化和任务结果反序列化的封装；

import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import syscfg
import cyberx

func_calc_price  = 1
func_calc_payoff = 2
func_calc_greeks = 3

g_up_in    = 1 # 向上敲入
g_down_in  = 2 # 向下敲入
g_up_out   = 3 # 向上敲出
g_down_out = 4 # 向下敲出

# s # 标的价格
# h # 障碍价格
# k # 行权价格
# x # 未触及障碍所需支付资金
# v # 波动率
# r # 无风险利率
# q # 年化分红率
# t # 年化到期期限
# p # 参与率，未敲出情况下客户对收益的占比要求
# is_call # 看涨看跌
# is_kop_delay # 敲出后是立即还是延期支付资金，false 为立即，true 为延期
# barrier_type # 障碍类型
# calc_price # 计算价格序列
# runs_step # 价格变动步数
# year_days # 年交易日数量
# run_from # 起始天数，第一天为零
# run_days # 运行天数

def CalcPrice(module, s, h, k, x, v, r, q, t, p, is_call, is_kop_delay, barrier_type):
    inputs = {"s":s, "h":h, "k":k, "x":x, "v":v, "r":r, "q":q, "t":t, "p":p, "is_call":is_call, "is_kop_delay":is_kop_delay, "barrier_type":barrier_type}
    result = json.loads(module.DirectCalc(func_calc_price, 0, json.dumps(inputs)))
    if result["return_code"] != 0:
        print(result["return_code"], result["return_info"])
    return result["result_data"]

def CalcPayoff(module, s, h, k, x, v, r, q, t, p, is_call, is_kop_delay, barrier_type):
    inputs = {"s":s, "h":h, "k":k, "x":x, "v":v, "r":r, "q":q, "t":t, "p":p, "is_call":is_call, "is_kop_delay":is_kop_delay, "barrier_type":barrier_type}
    result = json.loads(module.DirectCalc(func_calc_payoff, 0, json.dumps(inputs)))
    if result["return_code"] != 0:
        print(result["return_code"], result["return_info"])
    return result["result_data"]

def CalcGreeks(module, calc_greek, s, h, k, x, v, r, q, t, p, is_call, is_kop_delay, barrier_type, calc_price, runs_step, year_days, run_from, run_days):
    inputs = {"calc_greek":calc_greek, "s":s, "h":h, "k":k, "x":x, "v":v, "r":r, "q":q, "t":t, "p":p, "is_call":is_call, "is_kop_delay":is_kop_delay, "barrier_type":barrier_type, 
              "calc_price":calc_price, "runs_step":runs_step, "year_days":year_days, "run_from":run_from, "run_days":run_days}
    result = json.loads(module.DirectCalc(func_calc_greeks, 0, json.dumps(inputs)))
    if result["return_code"] != 0:
        print(result["return_code"], result["return_info"])
    return result["result_data"]

def FigureResult(array_s, array_t, result):
    figure = plt.figure()
    ax = Axes3D(figure)
    #ax = Axes3D(figure, auto_add_to_figure = False)
    figure.add_axes(ax)
    x = array_t
    y = array_s
    X, Y = np.meshgrid(x, y)
    ax.plot_surface(X, Y, result, rstride = 1, cstride = 1, cmap = plt.get_cmap("rainbow"))
    #ax.view_init(20, -25) # 视角：距离到期 由远到近
    #ax.view_init(20, -125) # 视角：距离到期 由近到远
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.show()

def ExportResult(run_from, run_days, calc_price, result, file_path):
    df_result = pd.DataFrame(result[:, run_from : (run_from + config.run_days)]).iloc[::-1] # 上下倒下顺序
    df_result.index = calc_price[::-1]
    df_result.columns = ["day_%d" % (days + 1) for days in np.arange(run_from, run_from + config.run_days, 1)]
    df_result.to_excel(file_path, sheet_name = "result")
    print("导出结果：%s" % file_path)

def Test_DerivX_Barrier_Single():
    result = 0.0
    greeks = []
    kernel = cyberx.Kernel(syscfg.SysCfg().ToArgs()) # 全局唯一
    module = cyberx.Create("derivx_barrier_single")
    
    #for s in [80.0, 82.0, 84.0, 86.0, 88.0, 90.0, 92.0, 94.0, 96.0, 98.0, 100.0, 102.0, 104.0]:
    #    result = CalcPrice(module, s, 80.0, 100.0, 0.0, 0.3, 0.03, 0.02, 1.0, 1.0, True, False, g_down_in)
    #    #result = CalcPrice(module, s, 80.0, 100.0, 0.0, 0.3, 0.03, 0.02, 1.0, 1.0, True, False, g_down_out)
    #    #result = CalcPrice(module, s, 80.0, 100.0, 0.0, 0.3, 0.03, 0.02, 1.0, 1.0, False, False, g_down_in)
    #    #result = CalcPrice(module, s, 80.0, 100.0, 0.0, 0.3, 0.03, 0.02, 1.0, 1.0, False, False, g_down_out)
    #    print(result)
    
    """
    args_cdo = [[90.0, 95.0, 0.25], [100.0, 95.0, 0.25], [110.0, 95.0, 0.25], [90.0, 100.0, 0.25], [100.0, 100.0, 0.25], [110.0, 100.0, 0.25],
                [90.0, 95.0, 0.30], [100.0, 95.0, 0.30], [110.0, 95.0, 0.30], [90.0, 100.0, 0.30], [100.0, 100.0, 0.30], [110.0, 100.0, 0.30]] # k, h, v
    for args in args_cdo:
        result = CalcPrice(module, 100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, True, False, g_down_out)
        print(result)
    
    args_cuo = [[90.0, 105.0, 0.25], [100.0, 105.0, 0.25], [110.0, 105.0, 0.25], [90.0, 105.0, 0.30], [100.0, 105.0, 0.30], [110.0, 105.0, 0.30]] # k, h, v
    for args in args_cuo:
        result = CalcPrice(module, 100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, True, False, g_up_out)
        print(result)
    
    args_cdi = [[90.0, 95.0, 0.25], [100.0, 95.0, 0.25], [110.0, 95.0, 0.25], [90.0, 100.0, 0.25], [100.0, 100.0, 0.25], [110.0, 100.0, 0.25],
                [90.0, 95.0, 0.30], [100.0, 95.0, 0.30], [110.0, 95.0, 0.30], [90.0, 100.0, 0.30], [100.0, 100.0, 0.30], [110.0, 100.0, 0.30]] # k, h, v
    for args in args_cdi:
        result = CalcPrice(module, 100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, True, False, g_down_in)
        print(result)
    
    args_cui = [[90.0, 105.0, 0.25], [100.0, 105.0, 0.25], [110.0, 105.0, 0.25], [90.0, 105.0, 0.30], [100.0, 105.0, 0.30], [110.0, 105.0, 0.30]] # k, h, v
    for args in args_cui:
        result = CalcPrice(module, 100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, True, False, g_up_in)
        print(result)
    
    args_pdo = [[90.0, 95.0, 0.25], [100.0, 95.0, 0.25], [110.0, 95.0, 0.25], [90.0, 100.0, 0.25], [100.0, 100.0, 0.25], [110.0, 100.0, 0.25],
                [90.0, 95.0, 0.30], [100.0, 95.0, 0.30], [110.0, 95.0, 0.30], [90.0, 100.0, 0.30], [100.0, 100.0, 0.30], [110.0, 100.0, 0.30]] # k, h, v
    for args in args_pdo:
        result = CalcPrice(module, 100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, False, False, g_down_out)
        print(result)
    
    args_puo = [[90.0, 105.0, 0.25], [100.0, 105.0, 0.25], [110.0, 105.0, 0.25], [90.0, 105.0, 0.30], [100.0, 105.0, 0.30], [110.0, 105.0, 0.30]] # k, h, v
    for args in args_puo:
        result = CalcPrice(module, 100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, False, False, g_up_out)
        print(result)
    
    args_pdi = [[90.0, 95.0, 0.25], [100.0, 95.0, 0.25], [110.0, 95.0, 0.25], [90.0, 100.0, 0.25], [100.0, 100.0, 0.25], [110.0, 100.0, 0.25],
                [90.0, 95.0, 0.30], [100.0, 95.0, 0.30], [110.0, 95.0, 0.30], [90.0, 100.0, 0.30], [100.0, 100.0, 0.30], [110.0, 100.0, 0.30]] # k, h, v
    for args in args_pdi:
        result = CalcPrice(module, 100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, False, False, g_down_in)
        print(result)
    
    args_pui = [[90.0, 105.0, 0.25], [100.0, 105.0, 0.25], [110.0, 105.0, 0.25], [90.0, 105.0, 0.30], [100.0, 105.0, 0.30], [110.0, 105.0, 0.30]] # k, h, v
    for args in args_pui:
        result = CalcPrice(module, 100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, False, False, g_up_in)
        print(result)
    """
    
    """
    args_list = []
    
    args_list.append([100.0, 80.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, True, False, g_down_out]) # 未敲出 s - k = 10.0
    args_list.append([100.0, 120.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, True, False, g_down_out]) # 已敲出 x = 3.0
    args_list.append([100.0, 80.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, False, False, g_down_out]) # 未敲出 k - s = 15.0
    args_list.append([100.0, 120.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, False, False, g_down_out]) # 已敲出 x = 3.0
    
    args_list.append([100.0, 120.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, True, False, g_up_out]) # 未敲出 s - k = 10.0
    args_list.append([100.0, 80.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, True, False, g_up_out]) # 已敲出 x = 3.0
    args_list.append([100.0, 120.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, False, False, g_up_out]) # 未敲出 k - s = 15.0
    args_list.append([100.0, 80.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, False, False, g_up_out]) # 已敲出 x = 3.0
    
    args_list.append([100.0, 80.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, True, False, g_down_in]) # 未敲入 x = 3.0
    args_list.append([100.0, 120.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, True, False, g_down_in]) # 已敲入 s - k = 10.0
    args_list.append([100.0, 80.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, False, False, g_down_in]) # 未敲入 x = 3.0
    args_list.append([100.0, 120.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, False, False, g_down_in]) # 已敲入 k - s = 15.0
    
    args_list.append([100.0, 120.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, True, False, g_up_in]) # 未敲入 x = 3.0
    args_list.append([100.0, 80.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, True, False, g_up_in]) # 已敲入 s - k = 10.0
    args_list.append([100.0, 120.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, False, False, g_up_in]) # 未敲入 x = 3.0
    args_list.append([100.0, 80.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, False, False, g_up_in]) # 已敲入 k - s = 15.0
    
    for args in args_list:
        result = CalcPayoff(module, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], args[9], args[10], args[11])
        print(result)
    """
    
    calc_price_u = 115.0 # 价格点上界
    calc_price_d = 75.0 # 价格点下界
    calc_price_g = 1.0 # 价格点间隔
    #calc_price = np.array([65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0, 100.0, 105.0]).tolist() # 计算价格序列
    calc_price = np.arange(calc_price_d, calc_price_u + calc_price_g, calc_price_g).tolist() # 含价格点上下界
    
    runs_step = 244 # 价格变动步数
    year_days = 244 # 年交易日数量
    run_from = 0 # 起始天数，第一天为零
    run_days = 244 # 运行天数
    
    #greek_flags = {"delta":"d"}
    greek_flags = {"delta":"d", "gamma":"g", "vega":"v", "theta":"t", "rho":"r"}
    for name, flag in greek_flags.items():
        #greeks = CalcGreeks(module, flag, 100.0, 105.0, 101.0, 3.0, 0.2, 0.03, 0.05, 1.0, 1.0, True, True, g_up_out, calc_price, runs_step, year_days, run_from, run_days)
        greeks = CalcGreeks(module, flag, 100.0, 95.0, 99.0, 3.0, 0.2, 0.03, 0.05, 1.0, 1.0, False, True, g_down_out, calc_price, runs_step, year_days, run_from, run_days)
        FigureResult(np.array(calc_price), np.arange(0, runs_step, 1), np.array(greeks))
        ExportResult(run_from, run_days, calc_price, np.array(greeks), "/export_greeks_%s.xlsx" % name)

if __name__ == "__main__":
    Test_DerivX_Barrier_Single()
