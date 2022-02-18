
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
# 1、演示凤凰结构参数设置；
# 2、演示凤凰结构客户票息、收益曲面、希腊值曲面等的计算；
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

func_calc_coupon = 1
func_calc_payoff = 2
func_calc_greeks = 3

event_task_finish = threading.Event()

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
        
        self.notional = 0.0 # 名义本金
        self.trade_long = True # 交易方向
        self.start_price = 0.0 # 初始价格
        self.strike_price = 0.0 # 敲入后执行价格
        self.knock_o_ratio = 0.0 # 敲出比率，非百分比
        self.knock_i_ratio = 0.0 # 敲入比率，非百分比
        self.knock_o_steps = 0.0 # 敲出比例逐月递减率
        self.knock_i_occur = False # 是否已经发生敲入
        self.knock_i_margin_call = True # 是否敲入后可追加保证金，置为 False 则变成不追保凤凰
        self.coupon_rate = 0.0 # 客户单次票息，CalcCoupon 时此入参不参与计算
        self.margin_rate = 0.0 # 保证金比例
        self.margin_interest = 0.0 # 保证金利率
        self.calc_price = [] # 计算价格序列
        self.run_from = 0 # 起始天数，第一天为零
        self.run_days = 0 # 运行天数
        self.knock_o_days = [] # 敲出日期序列
        self.knock_o_rate = [] # 敲出比率序列
        
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

def OnResult_Coupon(result):
    try:
        print("Callback OnResult_Coupon:", result)
        if result["return_code"] != 0:
            print(result["return_code"], result["return_info"])
        else:
            result = json.loads(result["result_data"])
            print("coupon:", result)
    except Exception as e:
        print("OnResult_Coupon 异常！%s" % e)
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

def Test_DerivX_Autocall_Phoenix():
    kernel = cyberx.Kernel(syscfg.SysCfg().ToArgs()) # 全局唯一

    config = Config()
    config.rand_rows = 50000 # 随机数据行数 # InitRand
    config.rand_cols = 250 # 随机数据列数 # InitRand
    config.rand_quasi = False # 随机数据类型 # InitRand # 目前 quasi 随机数据只能使用单核处理
    config.rand_seed = [0, 1, 2, 3, 4, 5, 6, 7] # 随机数据种子 # InitRand # 非负整数，有效位数不超逻辑处理器数量，目前 quasi 仅第一位有效
    
    config.dual_smooth = True # 对偶平滑路径 # InitPath
    config.runs_size = 100000 # 模拟路径数量 # InitPath
    config.runs_step = 244 # 价格变动步数 # InitPath
    config.year_days = 244 # 年交易日数量 # InitPath
    config.sigma = 0.16 # 波动率 # InitPath
    config.risk_free_rate = 0.03 # 无风险利率 # InitPath
    config.basis_rate = 0.05 # 股息或贴水 # InitPath
    config.price_limit_ratio = 0.1 # 涨跌停限制幅度 # InitPath
    config.price_limit_style = 0 # 涨跌停限制方式，0 不限制，1 超限部分移至下日，2 超限部分直接削掉 # InitPath
    
    config.notional = 100000.0 # 名义本金
    config.trade_long = False # 交易方向
    config.start_price = 100.0 # 初始价格
    config.strike_price = 100.0 # 敲入后执行价格
    config.knock_o_ratio = 1.0 # 敲出比率，非百分比
    config.knock_i_ratio = 0.8 # 敲入比率，非百分比
    config.knock_o_steps = 0.0 # 敲出比例逐月递减率
    config.knock_i_occur = False # 是否已经发生敲入
    config.knock_i_margin_call = True # 是否敲入后可追加保证金，置为 False 则变成不追保凤凰
    config.coupon_rate = 0.013 # 客户单次票息，CalcCoupon 时此入参不参与计算
    config.margin_rate = 1.0 # 保证金比例
    config.margin_interest = 0.03 # 保证金利率
    
    #   1    2    3    4    5    6    7    8    9   10   11   12   13   14   15   16   17   18   19   20   21   22   23   24   25   26   27   28   29   30   31   32   33   34   35   36  
    #  20,  40,  61,  81, 101, 122, 142, 162, 183, 203, 223, 244, 264, 284, 305, 325, 345, 366, 386, 406, 427, 447, 467, 488, 508, 528, 549, 569, 589, 610, 630, 650, 671, 691, 711, 732
    # 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0
    
    #config.knock_o_days = np.array([20, 40, 60]).tolist() # 敲出观察日
    config.knock_o_days = np.array([20, 40, 61, 81, 101, 122, 142, 162, 183, 203, 223, 244]).tolist() # 敲出观察日
    #config.knock_o_days = np.array([61, 71, 81, 91, 101, 112, 122, 132, 142, 152, 162, 173, 183, 193, 203, 213, 223, 234, 244, 254, 264, 274, 284, 295, 305, 315, 325, 335, 345, 356, 366, 376, 386, 396, 406, 417, 427, 437, 447, 457, 467, 478, 488]).tolist() # 敲出观察日
    #config.knock_o_days = np.array([66, 82, 103, 124, 147, 163, 183, 204, 223, 243, 265, 287, 309, 327, 347, 369, 391, 407, 427, 449, 469, 491]).tolist() # 敲出观察日
    #config.knock_o_days = np.array([61, 81, 101, 122, 142, 162, 183, 203, 223, 244, 264, 284, 305, 325, 345, 366, 386, 406, 427, 447, 467, 488, 508, 528, 549, 569, 589, 610, 630, 650, 671, 691, 711, 732]).tolist() # 敲出观察日
    
    #config.knock_o_rate = MakeStepDown(duration = 24, observe_start = 3, default_ratio = config.knock_o_ratio, stepdown_start = 4, stepdown_ratio = 0.01).tolist()
    #   1     2     3     4     5     6     7     8     9    10    11    12    13    14    15    16    17    18    19    20    21    22    23    24
    # 1.0, 0.99, 0.98, 0.97, 0.96, 0.95, 0.94, 0.93, 0.92, 0.91, 0.90, 0.89, 0.88, 0.87, 0.86, 0.85, 0.84, 0.83, 0.82, 0.81, 0.80, 0.79, 0.78, 0.77
    
    #config.knock_o_rate = MakeStepDown(duration = 36, observe_start = 6, default_ratio = config.knock_o_ratio, stepdown_start = 9, stepdown_ratio = 0.005).tolist()
    #   1      2     3      4     5      6     7      8     9     10    11     12    13     14    15     16    17     18    19     20   21     22    23     24    25     26    27     28    29     30    31     32
    # 1.0, 0.995, 0.99, 0.985, 0.98, 0.975, 0.97, 0.965, 0.96, 0.955, 0.95, 0.945, 0.94, 0.935, 0.93, 0.925, 0.92, 0.915, 0.91, 0.905, 0.9, 0.895, 0.89, 0.885, 0.88, 0.875, 0.87, 0.865, 0.86, 0.855, 0.85, 0.845
    
    knock_o_rate = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]) * config.knock_o_ratio # 敲出观察率
    #knock_o_rate = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]) * config.knock_o_ratio # 敲出观察率
    for i in range(len(knock_o_rate)):
        knock_o_rate[i] = knock_o_rate[i] - i * config.knock_o_steps
    config.knock_o_rate = knock_o_rate.tolist()
    #config.knock_o_rate = np.array([(1.0 - i * config.knock_o_steps) for i in range(len(config.knock_o_days))]).tolist() # 敲出观察率
    #config.knock_o_rate = np.array([1.0, 0.995, 0.99, 0.985, 0.98, 0.975, 0.97, 0.965, 0.96, 0.955, 0.95, 0.945, 0.94, 0.935, 0.93, 0.925, 0.92, 0.915, 0.91, 0.905, 0.9, 0.895]).tolist() # 敲出观察率
    #config.knock_o_rate = np.array([1.0, 0.99, 0.98, 0.97, 0.96, 0.95, 0.94, 0.93, 0.92, 0.91, 0.9, 0.89, 0.88, 0.87, 0.86, 0.85, 0.84, 0.83, 0.82, 0.81, 0.8, 0.79]).tolist() # 敲出观察率
    #config.knock_o_rate = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]).tolist() # 敲出观察率
    #print(config.knock_o_rate)
    
    calc_price_u = 105.0 # 价格点上界
    calc_price_d = 65.0 # 价格点下界
    calc_price_g = 1.0 # 价格点间隔
    #config.calc_price = np.array([65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0, 100.0, 105.0]).tolist() # 计算价格序列
    config.calc_price = np.arange(calc_price_d, calc_price_u + calc_price_g, calc_price_g).tolist() # 含价格点上下界
    
    config.run_from = 0 # 起始天数，第一天为零
    config.run_days = 1 # 运行天数
    
    ret_cols = config.runs_step
    ret_rows = len(config.calc_price)
    
    #print(config.ToJson())
    
    result = None
    
    tasker_test = tasker.Tasker()
    tasker_test.plugin_id = "derivx_autocall_phoenix"
    tasker_test.timeout_wait = 3600 # 秒
    tasker_test.common_args = config.ToJson()
    
    tasker_test.method_id = func_calc_coupon
    
    #result = kernel.AssignTask(tasker_test.ToArgs()) # 同步
    #print("同步:", result)
    #if result["return_code"] != 0:
    #    print(result["return_code"], result["return_info"])
    #else:
    #    result = json.loads(result["result_data"])
    #    print("coupon:", result)
    
    #event_task_finish.clear()
    #result = kernel.AssignTask(tasker_test.ToArgs(), OnResult_Coupon) # 异步
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
    Test_DerivX_Autocall_Phoenix()
