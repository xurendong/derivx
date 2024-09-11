
# -*- coding: utf-8 -*-

# Copyright (c) 2021-2024 the DerivX authors
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
# 1、演示累计结构参数设置；
# 2、演示累计结构价格、收益曲面、希腊值曲面等的计算；
# 3、演示 tasker 任务信息创建；
# 4、演示 同步模式 和 异步模式 的 AssignTask 任务执行调用；
# 5、演示异步回调函数的编写和使用；

# 标准型：标准累购/累沽、标准末日加倍累购/累沽、熔断累购/累沽、熔断末日加倍累购/累沽、标准不敲出累购/累沽、标准不敲出末日加倍累购/累沽
# 固定型：固定赔付累购/累沽、固定赔付末日加倍累购/累沽、固定赔付熔断累购/累沽、固定赔付熔断末日加倍累购/累沽、固定赔付不敲出累购/累沽、固定赔付不敲出末日加倍累购/累沽
# 增强型：增强累购/累沽、增强末日加倍累购/累沽、熔断增强累购/累沽、熔断增强末日加倍累购/累沽

# 注意：版本 >= 0.5.14 的，编译环境 Visual Studio 从 17.9.X 升级为 17.10.X 后，
#      对于 Python 3.6、3.7、3.8、3.9、3.10、3.11 存在一些兼容问题，
#      需要将 import cyberx 语句放在 import 如 pandas、PyQt5 等其他第三方库之前，
#      对于 Python 3.12 则仍然可以正常地任意放置，初始化 cyberx.Kernel 时不会异常。

import json
import threading

import cyberx

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import syscfg
import tasker
# import cyberx

func_calc_price  = 1
func_calc_payoff = 2
func_calc_greeks = 3

event_task_finish = threading.Event()

g_option_accrual_cash = 1 # 现金
g_option_accrual_kind = 2 # 实物
g_option_accrual_mixs = 3 # 混合

g_barrier_accrual_uc = 1 # 看涨（累购，累计多头）
g_barrier_accrual_dp = 2 # 看跌（累沽，累计空头）

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
        self.basis_rate = 0.0 # 股息或贴水 # InitPath
        self.risk_free_rate = 0.0 # 无风险利率 # InitPath
        self.price_limit_ratio = 0.0 # 涨跌停限制幅度 # InitPath
        self.price_limit_style = 0 # 涨跌停限制方式，0 不限制，1 超限部分移至下日，2 超限部分直接削掉 # InitPath
        
        self.notional = 0.0 # 名义本金，目前未使用
        self.trade_long = False # 交易方向
        self.option_type = 0 # 期权类型，现金、实物、混合
        self.barrier_type = 0 # 障碍类型，看涨、看跌
        self.start_price = 0.0 # 标的价格，具体价格点位
        self.strike_price = 0.0 # 执行价格，具体价格点位（敲入价格）
        self.knock_o_price = 0.0 # 敲出价格，具体价格点位（熔断价格）# 设为极大数或极小数即为无障碍型
        self.knock_o_valid = True # 是否允许熔断即敲出终止 # 设为否即为向上或向下敲出型，也即敲出不终止
        self.knock_o_boost = False # 是否允许敲出增强 # 设为是即为增强型
        self.p_knock_i = 0.0 # 参与率，敲入，杠杆系数
        self.p_knock_i_end = 0.0 # 参与率，敲入，期末额外倍数 # 设置可为末日加倍型
        self.p_knock_n = 0.0 # 参与率，未敲入未敲出
        self.p_knock_o = 0.0 # 参与率，敲出
        self.multiplier = 0.0 # 头寸乘数，每日规模
        self.ukiuko_fix_pay = 0.0 # 对于未敲入未敲出情况，使用绝对补偿，而不是挂钩收盘价（实物模式此参无效）# 设置即为区间固定赔付型
        self.ukiuko_fix_pay_use = False # 对于未敲入未敲出情况，是否使用绝对补偿（实物模式此参无效）# 设置即为区间固定赔付型
        
        self.option_fee = 0.0 # 期权费费率，非百分比（年化），CalcPrice 时此入参不参与计算 # option_fee * start_price 为所付期权费
        self.option_fee_interest = 0.0 # 期权费利率
        self.back_end_load = False # 期权费支付方式，False 为前端，True 为后端
        self.is_kop_delay = False # 敲出后是立即还是延期支付资金，False 为立即，True 为延期
        self.is_futures = False # 是否期货期权
        self.is_foreign = False # 是否外汇期权
        self.margin_rate = 0.0 # 保证金比率，非百分比（绝对） # margin_rate * start_price 为所付保证金
        self.margin_interest = 0.0 # 保证金利率
        self.discount_payoff = False # 是否对票息等收支进行贴现，False 为不贴现，True 为做贴现
        self.discount_margin = False # 是否对保证金收支进行贴现，False 为不贴现，True 为做贴现
        self.discount_option_fee = False # 是否对期权费收支进行贴现，影响期权费后付及先付时交易占用资金，False 为不贴现，True 为做贴现
        self.compound_option_fee = False # 是否对期权费收支进行复利，影响期权费先付及后付时垫付占用资金，False 为不复利，True 为做复利
        self.extend_end_days = 0 # 产品结束时延后清算天数(交易日)，期间票息和保证金等照算
        self.market_close = False # 是否已经收盘，会影响交易和估值，False 为未收盘，True 为已收盘
        
        self.prefix_rebate_ann_rate = 0.0 # 前端返息比率，非百分比（年化） # xxx_rate * start_price 为所付返息金额
        self.prefix_rebate_ann_need = False # 是否支付前端返息（年化）
        self.prefix_rebate_abs_rate = 0.0 # 前端返息比率，非百分比（绝对） # xxx_rate * start_price 为所付返息金额
        self.prefix_rebate_abs_need = False # 是否支付前端返息（绝对）
        self.suffix_rebate_ann_rate = 0.0 # 后端返息比率，非百分比（年化） # xxx_rate * start_price 为所付返息金额
        self.suffix_rebate_ann_need = False # 是否支付后端返息（年化）
        self.suffix_rebate_abs_rate = 0.0 # 后端返息比率，非百分比（绝对） # xxx_rate * start_price 为所付返息金额
        self.suffix_rebate_abs_need = False # 是否支付后端返息（绝对）
        self.discount_rebate = False # 是否对返息进行贴现，影响后端返息，False 为不贴现，True 为做贴现
        self.compound_rebate = False # 是否对返息进行复利，影响前端返息，False 为不复利，True 为做复利
        
        self.payoff_calc_method = 0 # 资金流计算方式
        
        self.calc_price = [] # 计算价格序列
        self.run_from = 0 # 起始天数，第一天为零 # 含已实现的天数
        self.run_days = 0 # 运行天数
        
        # 用户不传入则默认与 runs_step、year_days 一致
        self.runs_step_n = 0 # 产品自然日数(含延后清算) (可选)
        self.year_days_n = 0 # 年自然日数量 (可选)
        self.trading_days_n = [] # 交易日期序列(自然日) (可选)
        
        self.calc_greek = "" # 要计算的希腊值标识

    def ToJson(self):
        return json.dumps(self.__dict__)
        #return json.dumps(self.__dict__, sort_keys = False, indent = 4, separators = (",", ": "))

def FigureResult(config, result):
    figure = plt.figure()
    ax = Axes3D(figure)
    #ax = Axes3D(figure, auto_add_to_figure = False)
    figure.add_axes(ax)
    x = np.arange(0, config.runs_step, 1)
    y = np.array(config.calc_price)
    X, Y = np.meshgrid(x, y)
    ax.plot_surface(X, Y, result, rstride = 1, cstride = 1, cmap = plt.get_cmap("rainbow"))
    plt.show()

def ExportResult(config, result, file_path):
    df_result = pd.DataFrame(result[:, config.run_from : (config.run_from + config.run_days)]).iloc[::-1] # 上下倒下顺序
    df_result.index = np.array(config.calc_price)[::-1]
    df_result.columns = ["day_%d" % (days + 1) for days in np.arange(config.run_from, config.run_from + config.run_days, 1)]
    df_result.to_excel(file_path, sheet_name = "result")
    print("导出结果：%s" % file_path)

def OnResult_Price(result):
    try:
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

def Test_DerivX_Barrier_Accrual():
    kernel = cyberx.Kernel(syscfg.SysCfg().ToArgs()) # 全局唯一

    config = Config()
    config.rand_rows = 50000 # 随机数据行数 # InitRand
    config.rand_cols = 250 # 随机数据列数 # InitRand
    config.rand_quasi = False # 随机数据类型 # InitRand # 目前 quasi 随机数据只能使用单核处理
    config.rand_seed = [0, 1, 2, 3, 4, 5, 6, 7] # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量，目前 quasi 仅第一位有效
    
    config.dual_smooth = True # 对偶平滑路径 # InitPath
    config.runs_size = 100000 # 模拟路径数量 # InitPath
    config.runs_step = 60 # 价格变动步数 # InitPath
    config.year_days = 244 # 年交易日数量 # InitPath
    config.sigma = 0.2 # 波动率 # InitPath
    config.basis_rate = 0.03 # 股息或贴水 # InitPath
    config.risk_free_rate = 0.03 # 无风险利率 # InitPath
    config.price_limit_ratio = 0.1 # 涨跌停限制幅度 # InitPath
    config.price_limit_style = 0 # 涨跌停限制方式，0 不限制，1 超限部分移至下日，2 超限部分直接削掉 # InitPath
    
    config.notional = 100000.0 # 名义本金，目前未使用
    config.trade_long = False # 交易方向
    config.option_type = g_option_accrual_cash # 期权类型，现金、实物、混合
    config.barrier_type = g_barrier_accrual_uc # 障碍类型，看涨、看跌
    config.start_price = 100.0 # 标的价格，具体价格点位
    config.strike_price = 95.0 # 执行价格，具体价格点位（敲入价格）
    config.knock_o_price = 105.0 # 敲出价格，具体价格点位（熔断价格）# 设为极大数或极小数即为无障碍型
    config.knock_o_valid = True # 是否允许熔断即敲出终止 # 设为否即为向上或向下敲出型，也即敲出不终止
    config.knock_o_boost = False # 是否允许敲出增强 # 设为是即为增强型
    config.p_knock_i = 2.0 # 参与率，敲入，杠杆系数
    config.p_knock_i_end = 1.0 # 参与率，敲入，期末额外倍数 # 设置可为末日加倍型
    config.p_knock_n = 1.0 # 参与率，未敲入未敲出
    config.p_knock_o = 1.0 # 参与率，敲出
    config.multiplier = 10.0 # 头寸乘数，每日规模
    config.ukiuko_fix_pay = 0.0 # 对于未敲入未敲出情况，使用绝对补偿，而不是挂钩收盘价（实物模式此参无效）# 设置即为区间固定赔付型
    config.ukiuko_fix_pay_use = False # 对于未敲入未敲出情况，是否使用绝对补偿（实物模式此参无效）# 设置即为区间固定赔付型
    
    config.option_fee = 0.0 # 期权费费率，非百分比（年化），CalcPrice 时此入参不参与计算 # option_fee * start_price 为所付期权费
    config.option_fee_interest = 0.03 # 期权费利率
    config.back_end_load = False # 期权费支付方式，False 为前端，True 为后端
    config.is_kop_delay = False # 敲出后是立即还是延期支付资金，False 为立即，True 为延期
    config.is_futures = True # 是否期货期权
    config.is_foreign = False # 是否外汇期权
    config.margin_rate = 0.0 # 保证金比率，非百分比（绝对） # margin_rate * start_price 为所付保证金
    config.margin_interest = 0.03 # 保证金利率
    config.discount_payoff = True # 是否对票息等收支进行贴现，False 为不贴现，True 为做贴现
    config.discount_margin = True # 是否对保证金收支进行贴现，False 为不贴现，True 为做贴现
    config.discount_option_fee = True # 是否对期权费收支进行贴现，影响期权费后付及先付时交易占用资金，False 为不贴现，True 为做贴现
    config.compound_option_fee = True # 是否对期权费收支进行复利，影响期权费先付及后付时垫付占用资金，False 为不复利，True 为做复利
    config.extend_end_days = 0 # 产品结束时延后清算天数(交易日)，期间票息和保证金等照算
    config.market_close = False # 是否已经收盘，会影响交易和估值，False 为未收盘，True 为已收盘
    
    config.prefix_rebate_ann_rate = 0.0 # 前端返息比率，非百分比（年化） # xxx_rate * start_price 为所付返息金额
    config.prefix_rebate_ann_need = False # 是否支付前端返息（年化）
    config.prefix_rebate_abs_rate = 0.0 # 前端返息比率，非百分比（绝对） # xxx_rate * start_price 为所付返息金额
    config.prefix_rebate_abs_need = False # 是否支付前端返息（绝对）
    config.suffix_rebate_ann_rate = 0.0 # 后端返息比率，非百分比（年化） # xxx_rate * start_price 为所付返息金额
    config.suffix_rebate_ann_need = False # 是否支付后端返息（年化）
    config.suffix_rebate_abs_rate = 0.0 # 后端返息比率，非百分比（绝对） # xxx_rate * start_price 为所付返息金额
    config.suffix_rebate_abs_need = False # 是否支付后端返息（绝对）
    config.discount_rebate = False # 是否对返息进行贴现，影响后端返息，False 为不贴现，True 为做贴现
    config.compound_rebate = False # 是否对返息进行复利，影响前端返息，False 为不复利，True 为做复利
    
    config.payoff_calc_method = 0 # 资金流计算方式
    
    calc_price_u = 110.0 # 价格点上界
    calc_price_d = 90.0 # 价格点下界
    calc_price_g = 1.0 # 价格点间隔
    #config.calc_price = np.array([90.0, 92.0, 94.0, 96.0, 98.0, 100.0, 102.0, 104.0, 106.0, 108.0, 110.0]).tolist() # 计算价格序列
    config.calc_price = np.arange(calc_price_d, calc_price_u + calc_price_g, calc_price_g).tolist() # 含价格点上下界
    
    # 用户不传入则默认与 runs_step、year_days 一致
    #config.runs_step_n = 360 # 产品自然日数(含延后清算) (可选)
    #config.year_days_n = 365 # 年自然日数量 (可选)
    #config.trading_days_n = [1, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 18, 19, 20, ..., 341, 342, 343, 344, 347, 348, 349, 350, 357, 360] # 交易日期序列(自然日) (可选)
    
    config.run_from = 0 # 起始天数，第一天为零
    config.run_days = 1 # 运行天数
    
    ret_cols = config.runs_step
    ret_rows = len(config.calc_price)
    
    #print(config.ToJson())
    
    result = None
    
    tasker_test = tasker.Tasker()
    tasker_test.plugin_id = "derivx_barrier_accrual"
    tasker_test.timeout_wait = 3600 # 秒
    tasker_test.distribute_type = 0 # 本地计算任务
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
    #    ExportResult(config, np.array(result), "/export_payoff.xlsx")
    
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
        #    ExportResult(config, np.array(result), "/export_greeks_%s.xlsx" % name)
        
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
    Test_DerivX_Barrier_Accrual()
