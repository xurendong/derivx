
# -*- coding: utf-8 -*-

# Copyright (c) 2021-2022 the DerivX authors
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
# 1、演示鲨鱼鳍结构参数设置；
# 2、演示鲨鱼鳍结构价格、收益曲面、希腊值曲面等的计算；
# 3、演示 tasker 任务信息创建；
# 4、演示 同步模式 和 异步模式 的 AssignTask 任务执行调用；
# 5、演示异步回调函数的编写和使用；

import json
import threading

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import syscfg
import tasker
import cyberx

func_calc_price = 1
func_calc_payoff = 2
func_calc_greeks = 3

event_task_finish = threading.Event()

g_option_european = 1 # 欧式
g_option_american = 2 # 美式

g_sharkfin_uc = 1 # 向上敲出看涨，看涨鲨鱼鳍
g_sharkfin_dp = 2 # 向下敲出看跌，看跌鲨鱼鳍
g_sharkfin_ucdp = 3 # 向上敲出看涨 + 向下敲出看跌，双鲨鱼鳍

class Config(object):
    def __init__(self):
        self.rand_rows = 0 # 随机数据行数 # InitRand
        self.rand_cols = 0 # 随机数据列数 # InitRand
        self.rand_quasi = False # 随机数据类型 # InitRand # 目前 quasi 随机数据只能使用单核处理
        self.rand_seed = [] # 随机数据种子 # InitRand # 非负整数，有效位数不超逻辑处理器数量，目前 quasi 仅第一位有效
        
        self.dual_smooth = True # 对偶平滑路径 # InitPath
        self.runs_size = 0 # 模拟路径数量 # InitPath
        self.runs_step = 0 # 价格变动步数 # InitPath
        self.year_days = 0 # 年交易日数量 # InitPath
        self.sigma = 0.0 # 波动率 # InitPath
        self.risk_free_rate = 0.0 # 无风险利率 # InitPath
        self.basis_rate = 0.0 # 股息或贴水 # InitPath
        self.price_limit_ratio = 0.0 # 涨跌停限制幅度 # InitPath
        self.price_limit_style = 0 # 涨跌停限制方式，0 不限制，1 超限部分移至下日，2 超限部分直接削掉 # InitPath
        
        self.s = 0.0 # 标的价格
        self.h_l = 0.0 # 障碍价格，低
        self.h_h = 0.0 # 障碍价格，高
        self.k_l = 0.0 # 行权价格，低
        self.k_h = 0.0 # 行权价格，高
        self.x_l = 0.0 # 敲出后需支付的年化资金，低，比如 s = 1.0 x = 0.035
        self.x_h = 0.0 # 敲出后需支付的年化资金，高，比如 s = 1.0 x = 0.035
        self.p_l = 0.0 # 参与率，低，未敲出情况下客户对收益的占比要求
        self.p_h = 0.0 # 参与率，高，未敲出情况下客户对收益的占比要求
        self.is_kop_delay = False # 敲出后是立即还是延期支付资金，False 为立即，True 为延期，欧式的此参数无效
        self.option_type = 0 # 期权类型
        self.barrier_type = 0 # 障碍类型
        self.trade_long = True # 交易方向
        self.option_fee = 0.0 # 期权费费率，目前未使用
        self.option_fee_interest = 0.0 # 期权费利率
        self.consumed_option_fee_rate = 0.0 # 对冲交易 消耗 的期权费占比，针对 option_fee 的小数非百分比格式
        self.occupied_option_fee_rate = 0.0 # 对冲交易 占用 的期权费占比，针对 option_fee 的小数非百分比格式
        self.back_end_load = False # 期权费支付方式，False 为前端，True 为后端
        self.discount_payoff = False # 是否对票息等收支进行贴现，False 为不贴现，True 为做贴现
        self.discount_option_fee = False # 是否对期权费收支进行贴现，影响期权费后付及先付时交易占用资金，False 为不贴现，True 为做贴现
        self.compound_option_fee = False # 是否对期权费收支进行复利，影响期权费先付及后付时垫付占用资金，False 为不复利，True 为做复利
        self.market_close = False # 是否已经收盘，会影响交易和估值，False 为未收盘，True 为已收盘
        
        self.calc_price = [] # 计算价格序列
        self.run_from = 0 # 起始天数，第一天为零
        self.run_days = 0 # 运行天数
        
        self.calc_greek = "" # 要计算的希腊值标识

    def ToJson(self):
        return json.dumps(self.__dict__)
        #return json.dumps(self.__dict__, sort_keys = False, indent = 4, separators = (",", ": "))

def FigureResult(config, result):
    figure = plt.figure()
    ax = Axes3D(figure)
    #ax = Axes3D(figure, auto_add_to_figure = False)
    #figure.add_axes(ax)
    x = np.arange(0, config.runs_step, 1)
    y = np.array(config.calc_price)
    X, Y = np.meshgrid(x, y)
    ax.plot_surface(X, Y, result, rstride = 1, cstride = 1, cmap = plt.get_cmap("rainbow"))
    plt.show()

def ExportResult(config, result, file_path):
    export_days = config.run_days
    if export_days > 255: # Excel 最大 256 列，首列显示价格，剩余可用 255 列
        export_days = 255
        print("提示：Excel 最大 256 列，剩余 %d 列数据未作导出！" % (config.run_days - 255))
    df_result = pd.DataFrame(result[:, config.run_from : (config.run_from + export_days)]).iloc[::-1] # 上下倒下顺序
    df_result.index = np.array(config.calc_price)[::-1]
    df_result.columns = ["day_%d" % (days + 1) for days in np.arange(config.run_from, config.run_from + export_days, 1)]
    df_result.to_excel(file_path, sheet_name = "result")
    print("导出结果：%s" % file_path)

def MakeStepDown(duration, observe_start, default_ratio, stepdown_start, stepdown_ratio):
    stepdown = np.array([])
    stepdown_times = duration - stepdown_start + 2
    for i in range(stepdown_start - observe_start - 1):
        stepdown = np.append(stepdown, default_ratio)
    for i in range(stepdown_times):
        stepdown = np.append(stepdown, default_ratio - stepdown_ratio * i)
    print(stepdown)
    return stepdown

def OnResult_Price(result):
    try:
        print("Callback OnResult_Price:", result)
        if result["return_code"] != 0:
            print(result["return_code"], result["return_info"])
        else:
            result = json.loads(result["result_data"])
            print("price:", result)
    except Exception as e:
        print("OnResult_Price 异常！%s" % e)
    event_task_finish.set() #

def OnResult_Payoff(result):
    try:
        if result["return_code"] != 0:
            print(result["return_code"], result["return_info"])
        else:
            result = json.loads(result["result_data"])
            print("payoff:", result)
    except Exception as e:
        print("OnResult_Payoff 异常！%s" % e)
    event_task_finish.set() #

def OnResult_Greeks(result):
    try:
        if result["return_code"] != 0:
            print(result["return_code"], result["return_info"])
        else:
            result = json.loads(result["result_data"])
            print("greeks:", result)
    except Exception as e:
        print("OnResult_Greeks 异常！%s" % e)
    event_task_finish.set() #

def Test_DerivX_Barrier_Sharkfin():
    kernel = cyberx.Kernel(syscfg.SysCfg().ToArgs()) # 全局唯一

    config = Config()
    config.rand_rows = 50000 # 随机数据行数 # InitRand
    config.rand_cols = 250 # 随机数据列数 # InitRand
    config.rand_quasi = False # 随机数据类型 # InitRand # 目前 quasi 随机数据只能使用单核处理
    config.rand_seed = [0, 1, 2, 3, 4, 5, 6, 7] # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量，目前 quasi 仅第一位有效
    
    config.dual_smooth = True # 对偶平滑路径 # InitPath
    config.runs_size = 100000 # 模拟路径数量 # InitPath
    config.runs_step = 244 # 价格变动步数 # InitPath
    config.year_days = 244 # 年交易日数量 # InitPath
    config.sigma = 0.16 # 波动率 # InitPath
    config.risk_free_rate = 0.03 # 无风险利率 # InitPath
    config.basis_rate = 0.06 # 股息或贴水 # InitPath
    config.price_limit_ratio = 0.1 # 涨跌停限制幅度 # InitPath
    config.price_limit_style = 0 # 涨跌停限制方式，0 不限制，1 超限部分移至下日，2 超限部分直接削掉 # InitPath
    
    config.s = 1.0 # 标的价格
    config.h_l = 0.95 # 障碍价格，低
    config.h_h = 1.05 # 障碍价格，高
    config.k_l = 0.99 # 行权价格，低
    config.k_h = 1.01 # 行权价格，高
    config.x_l = 0.035 # 敲出后需支付的年化资金，低，比如 s = 1.0 x = 0.035
    config.x_h = 0.035 # 敲出后需支付的年化资金，高，比如 s = 1.0 x = 0.035
    config.p_l = 1.0 # 参与率，低，未敲出情况下客户对收益的占比要求
    config.p_h = 1.0 # 参与率，高，未敲出情况下客户对收益的占比要求
    config.is_kop_delay = True # 敲出后是立即还是延期支付资金，False 为立即，True 为延期，欧式的此参数无效
    config.option_type = g_option_american # 期权类型
    config.barrier_type = g_sharkfin_ucdp # 障碍类型
    config.trade_long = False # 交易方向
    config.option_fee = 0.035 # 期权费费率，CalcPrice 时此入参不参与计算
    config.option_fee_interest = 0.03 # 期权费利率
    config.consumed_option_fee_rate = 0.0 # 对冲交易 消耗 的期权费占比，针对 option_fee 的小数非百分比格式
    config.occupied_option_fee_rate = 0.0 # 对冲交易 占用 的期权费占比，针对 option_fee 的小数非百分比格式
    config.back_end_load = False # 期权费支付方式，False 为前端，True 为后端
    config.discount_payoff = False # 是否对票息等收支进行贴现，False 为不贴现，True 为做贴现
    config.discount_option_fee = False # 是否对期权费收支进行贴现，影响期权费后付及先付时交易占用资金，False 为不贴现，True 为做贴现
    config.compound_option_fee = False # 是否对期权费收支进行复利，影响期权费先付及后付时垫付占用资金，False 为不复利，True 为做复利
    config.market_close = False # 是否已经收盘，会影响交易和估值，False 为未收盘，True 为已收盘
    
    calc_price_u = 1.1 # 价格点上界
    calc_price_d = 0.9 # 价格点下界
    calc_price_g = 0.01 # 价格点间隔
    #config.calc_price = np.array([0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00, 1.05]).tolist() # 计算价格序列
    config.calc_price = np.arange(calc_price_d, calc_price_u + calc_price_g, calc_price_g).tolist() # 含价格点上下界
    
    config.run_from = 0 # 起始天数，第一天为零
    config.run_days = 1 # 运行天数
    
    ret_cols = config.runs_step
    ret_rows = len(config.calc_price)
    
    #print(config.ToJson())
    
    result = None
    
    tasker_test = tasker.Tasker()
    tasker_test.plugin_id = "derivx_barrier_sharkfin"
    tasker_test.timeout_wait = 3600 # 秒
    tasker_test.common_args = config.ToJson()
    
    tasker_test.method_id = func_calc_price
    
    #result = kernel.AssignTask(tasker_test.ToArgs()) # 同步
    #print("同步:", result)
    #if result["return_code"] != 0:
    #    print(result["return_code"], result["return_info"])
    #else:
    #    result = json.loads(result["result_data"])
    #    print("price:", result)
    
    #event_task_finish.clear()
    #result = kernel.AssignTask(tasker_test.ToArgs(), OnResult_Price) # 异步
    #print("异步:", result)
    #if result["return_code"] != 0:
    #    print(result["return_code"], result["return_info"])
    #else:
    #    tasker_id = result["tasker_id"]
    #    ret_wait = event_task_finish.wait(timeout = tasker_test.timeout_wait) # 等待任务结果
    #    if ret_wait != True:
    #        print("等待任务结果超时！", tasker_id)
    
    tasker_test.method_id = func_calc_payoff
    
    #result = kernel.AssignTask(tasker_test.ToArgs()) # 同步
    #if result["return_code"] != 0:
    #    print(result["return_code"], result["return_info"])
    #else:
    #    result = json.loads(result["result_data"])
    #    FigureResult(config, np.array(result))
    #    ExportResult(config, np.array(result), "/export_payoff.xls")
    
    #event_task_finish.clear()
    #result = kernel.AssignTask(tasker_test.ToArgs(), OnResult_Payoff) # 异步
    #print("异步:", result)
    #if result["return_code"] != 0:
    #    print(result["return_code"], result["return_info"])
    #else:
    #    tasker_id = result["tasker_id"]
    #    ret_wait = event_task_finish.wait(timeout = tasker_test.timeout_wait) # 等待任务结果
    #    if ret_wait != True:
    #        print("等待任务结果超时！", tasker_id)
    
    tasker_test.method_id = func_calc_greeks
    
    #greek_flags = {"delta":"d"}
    greek_flags = {"delta":"d", "gamma":"g", "vega":"v", "theta":"t", "rho":"r"}
    for name, flag in greek_flags.items():
        config.calc_greek = flag
        tasker_test.common_args = config.ToJson()
        
        #result = kernel.AssignTask(tasker_test.ToArgs()) # 同步
        #if result["return_code"] != 0:
        #    print(result["return_code"], result["return_info"])
        #else:
        #    result = json.loads(result["result_data"])
        #    FigureResult(config, np.array(result))
        #    ExportResult(config, np.array(result), "/export_greeks_%s.xls" % name)
        
        #event_task_finish.clear()
        #result = kernel.AssignTask(tasker_test.ToArgs(), OnResult_Greeks) # 异步
        #print("异步:", result)
        #if result["return_code"] != 0:
        #    print(result["return_code"], result["return_info"])
        #else:
        #    tasker_id = result["tasker_id"]
        #    ret_wait = event_task_finish.wait(timeout = tasker_test.timeout_wait) # 等待任务结果
        #    if ret_wait != True:
        #        print("等待任务结果超时！", tasker_id)

if __name__ == "__main__":
    Test_DerivX_Barrier_Sharkfin()
