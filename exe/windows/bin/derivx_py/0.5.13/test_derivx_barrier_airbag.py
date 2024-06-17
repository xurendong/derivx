
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
# 1、演示安全气囊结构参数设置；
# 2、演示安全气囊结构价格、收益曲面、希腊值曲面等的计算；
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

g_airbag_uc = 1 # 向上看涨，安全气囊看涨
g_airbag_dp = 2 # 向下看跌，安全气囊看跌

func_calc_price  = 1
func_calc_payoff = 2
func_calc_greeks = 3

event_task_finish = threading.Event()

class Config(object):
    def __init__(self):
        self.rand_rows = 0 # 随机数据行数
        self.rand_cols = 0 # 随机数据列数
        self.rand_quasi = False # 随机数据类型 # 目前 quasi 随机数据只能使用单核处理
        self.rand_seed = [] # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量，目前 quasi 仅第一位有效
        
        self.dual_smooth = True # 对偶平滑路径
        self.runs_size = 0 # 模拟路径数量
        self.runs_step = 0 # 价格变动步数
        self.year_days = 0 # 年交易日数量
        self.sigma = 0.0 # 波动率
        self.basis_rate = 0.0 # 股息或贴水
        self.risk_free_rate = 0.0 # 无风险利率
        self.price_limit_ratio = 0.0 # 涨跌停限制幅度
        self.price_limit_style = 0 # 涨跌停限制方式，0 不限制，1 超限部分移至下日，2 超限部分直接削掉
        
        self.notional = 0.0 # 名义本金，目前未使用
        self.trade_long = False # 交易方向
        self.barrier_type = 0 # 障碍类型，g_airbag_uc 看涨，g_airbag_dp 看跌
        self.start_price = 0.0 # 初始价格，具体价格点位
        self.k_earn_cap = 0.0 # 行权价比率，非百分比，未敲入，收益封顶，大数则无封顶
        self.k_earn_get = 0.0 # 行权价比率，非百分比，未敲入，获得收益
        self.k_loss_cap = 0.0 # 行权价比率，非百分比，有敲入，收益封顶，大数则无封顶
        self.k_loss_get = 0.0 # 行权价比率，非百分比，有敲入，产生损失
        self.k_loss_flo = 0.0 # 行权价比率，非百分比，有敲入，损失保底，为零则无保底，也即不追保比率
        self.knock_i_ratio = 0.0 # 敲入比率，非百分比
        self.knock_i_occur = False # 是否已经发生敲入
        self.p_earn_ki_not = 0.0 # 参与率，没有敲入，获得收益
        self.p_earn_ki_yes = 0.0 # 参与率，发生敲入，获得收益
        self.p_loss_ki_yes = 0.0 # 参与率，发生敲入，产生损失，一般与 p_earn_ki_yes 相同
        
        self.option_fee = 0.0 # 期权费费率，年化，目前未使用
        self.option_fee_interest = 0.0 # 期权费利率
        self.back_end_load = False # 期权费支付方式，False 为前端，True 为后端
        self.is_kop_delay = False # 行权时是立即还是到期支付资金，False 为立即，True 为延期
        self.is_futures = False # 是否期货期权
        self.is_foreign = False # 是否外汇期权
        self.margin_rate = 0.0 # 保证金比例，1 为收取全额保证金，0 为不收保证金
        self.margin_interest = 0.0 # 保证金利率
        self.discount_payoff = False # 是否对票息等收支进行贴现，False 为不贴现，True 为做贴现
        self.discount_margin = False # 是否对保证金收支进行贴现，False 为不贴现，True 为做贴现
        self.discount_option_fee = False # 是否对期权费收支进行贴现，影响期权费后付，False 为不贴现，True 为做贴现
        self.compound_option_fee = False # 是否对期权费收支进行复利，影响期权费先付，False 为不复利，True 为做复利
        self.extend_end_days = 0 # 产品结束时延后清算天数(交易日)，期间票息和保证金等照算
        self.market_close = False # 是否已经收盘，会影响交易和估值，False 为未收盘，True 为已收盘
        
        self.ukiueg_rebate = 0.0 # 对于无收益无敲入的情况，客户只要求得到固定收益，类似红利票息
        self.ukiueg_rebate_ann = False # False 为绝对收益率，True 为年化收益率
        self.ukiueg_rebate_use = False # 是否支付 ukiueg 收益，False 为类似红利票息为零，True 为单独指定类似红利票息
        
        self.prefix_rebate_ann_rate = 0.0 # 前端返息比率，非百分比（年化）
        self.prefix_rebate_ann_need = False # 是否支付前端返息（年化）
        self.prefix_rebate_abs_rate = 0.0 # 前端返息比率，非百分比（绝对）
        self.prefix_rebate_abs_need = False # 是否支付前端返息（绝对）
        self.suffix_rebate_ann_rate = 0.0 # 后端返息比率，非百分比（年化）
        self.suffix_rebate_ann_need = False # 是否支付后端返息（年化）
        self.suffix_rebate_abs_rate = 0.0 # 后端返息比率，非百分比（绝对）
        self.suffix_rebate_abs_need = False # 是否支付后端返息（绝对）
        self.discount_rebate = False # 是否对返息进行贴现，影响后端返息，False 为不贴现，True 为做贴现
        self.compound_rebate = False # 是否对返息进行复利，影响前端返息，False 为不复利，True 为做复利
        
        self.payoff_calc_method = 0 # 资金流计算方式
        
        self.calc_price = [] # 计算价格序列
        self.run_from = 0 # 起始天数，第一天为零
        self.run_days = 0 # 运行天数
        self.knock_o_days = [] # 敲出日期序列(交易日)
        
        # 用户不传入则默认与 runs_step、year_days、knock_o_days 一致
        self.runs_step_n = 0 # 产品自然日数(含延后清算) (可选)
        self.year_days_n = 0 # 年自然日数量 (可选)
        self.knock_o_days_n = [] # 敲出日期序列(自然日) (可选)
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

def Test_DerivX_Barrier_Airbag():
    kernel = cyberx.Kernel(syscfg.SysCfg().ToArgs()) # 全局唯一

    config = Config()
    config.rand_rows = 50000 # 随机数据行数
    config.rand_cols = 500 # 随机数据列数
    config.rand_quasi = False # 随机数据类型 # 目前 quasi 随机数据只能使用单核处理
    config.rand_seed = [0, 1, 2, 3, 4, 5, 6, 7] # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量，目前 quasi 仅第一位有效
    
    config.dual_smooth = True # 对偶平滑路径
    config.runs_size = 100000 # 模拟路径数量
    config.runs_step = 488 # 价格变动步数
    config.year_days = 244 # 年交易日数量
    config.sigma = 0.16 # 波动率
    config.basis_rate = 0.05 # 股息或贴水
    config.risk_free_rate = 0.03 # 无风险利率
    config.price_limit_ratio = 0.1 # 涨跌停限制幅度
    config.price_limit_style = 0 # 涨跌停限制方式，0 不限制，1 超限部分移至下日，2 超限部分直接削掉
    
    config.notional = 100000.0 # 名义本金，目前未使用
    config.trade_long = False # 交易方向
    config.barrier_type = g_airbag_uc # 障碍类型，g_airbag_uc 看涨，g_airbag_dp 看跌
    config.start_price = 100.0 # 初始价格，具体价格点位
    
    config.k_earn_cap = 1.2 # 行权价比率，非百分比，未敲入，收益封顶，大数值则无封顶
    config.k_earn_get = 1.0 # 行权价比率，非百分比，未敲入，获得收益
    config.k_loss_cap = 1.2 # 行权价比率，非百分比，有敲入，收益封顶，大数值则无封顶
    config.k_loss_get = 1.0 # 行权价比率，非百分比，有敲入，产生损失
    config.k_loss_flo = 0.6 # 行权价比率，非百分比，有敲入，损失保底，为零则无保底，也即不追保比率
    config.knock_i_ratio = 0.8 # 敲入比率，非百分比
    
    #config.k_earn_cap = 0.8 # 行权价比率，非百分比，未敲入，收益封顶，小数值则无封顶
    #config.k_earn_get = 1.0 # 行权价比率，非百分比，未敲入，获得收益
    #config.k_loss_cap = 0.8 # 行权价比率，非百分比，有敲入，收益封顶，小数值则无封顶
    #config.k_loss_get = 1.0 # 行权价比率，非百分比，有敲入，产生损失
    #config.k_loss_flo = 1.4 # 行权价比率，非百分比，有敲入，损失保底，大数值则无保底，也即不追保比率
    #config.knock_i_ratio = 1.2 # 敲入比率，非百分比
    
    config.knock_i_occur = False # 是否已经发生敲入
    config.p_earn_ki_not = 1.0 # 参与率，没有敲入，获得收益
    config.p_earn_ki_yes = 1.0 # 参与率，发生敲入，获得收益
    config.p_loss_ki_yes = 1.0 # 参与率，发生敲入，产生损失，一般与 p_earn_ki_yes 相同
    
    config.option_fee = 0.05 # 期权费费率，年化，CalcPrice 时此入参不参与计算
    config.option_fee_interest = 0.03 # 期权费利率
    config.back_end_load = False # 期权费支付方式，False 为前端，True 为后端
    config.is_kop_delay = False # 行权时是立即还是到期支付资金，False 为立即，True 为延期
    config.is_futures = False # 是否期货期权
    config.is_foreign = False # 是否外汇期权
    config.margin_rate = 1.0 # 保证金比例，1 为收取全额保证金，0 为不收保证金
    config.margin_interest = 0.03 # 保证金利率
    config.discount_payoff = False # 是否对票息等收支进行贴现，False 为不贴现，True 为做贴现
    config.discount_margin = False # 是否对保证金收支进行贴现，False 为不贴现，True 为做贴现
    config.discount_option_fee = False # 是否对期权费收支进行贴现，影响期权费后付，False 为不贴现，True 为做贴现
    config.compound_option_fee = False # 是否对期权费收支进行复利，影响期权费先付，False 为不复利，True 为做复利
    config.extend_end_days = 0 # 产品结束时延后清算天数(交易日)，期间票息和保证金等照算
    config.market_close = False # 是否已经收盘，会影响交易和估值，False 为未收盘，True 为已收盘
    
    config.ukiueg_rebate = 0.0 # 对于无收益无敲入的情况，客户只要求得到固定收益，类似红利票息
    config.ukiueg_rebate_ann = False # False 为绝对收益率，True 为年化收益率
    config.ukiueg_rebate_use = False # 是否支付 ukiueg 收益，False 为类似红利票息为零，True 为单独指定类似红利票息
    
    config.prefix_rebate_ann_rate = 0.0 # 前端返息比率，非百分比（年化）
    config.prefix_rebate_ann_need = False # 是否支付前端返息（年化）
    config.prefix_rebate_abs_rate = 0.0 # 前端返息比率，非百分比（绝对）
    config.prefix_rebate_abs_need = False # 是否支付前端返息（绝对）
    config.suffix_rebate_ann_rate = 0.0 # 后端返息比率，非百分比（年化）
    config.suffix_rebate_ann_need = False # 是否支付后端返息（年化）
    config.suffix_rebate_abs_rate = 0.0 # 后端返息比率，非百分比（绝对）
    config.suffix_rebate_abs_need = False # 是否支付后端返息（绝对）
    config.discount_rebate = False # 是否对返息进行贴现，影响后端返息，False 为不贴现，True 为做贴现
    config.compound_rebate = False # 是否对返息进行复利，影响前端返息，False 为不复利，True 为做复利
    
    config.payoff_calc_method = 0 # 资金流计算方式
    
    #   1    2    3    4    5    6    7    8    9   10   11   12   13   14   15   16   17   18   19   20   21   22   23   24   25   26   27   28   29   30   31   32   33   34   35   36
    #  20,  40,  61,  81, 101, 122, 142, 162, 183, 203, 223, 244, 264, 284, 305, 325, 345, 366, 386, 406, 427, 447, 467, 488, 508, 528, 549, 569, 589, 610, 630, 650, 671, 691, 711, 732
    
    #config.knock_o_days = np.array([20, 40, 60]).tolist() # 敲出观察日(交易日)
    config.knock_o_days = np.array([61, 81, 101, 122, 142, 162, 183, 203, 223, 244, 264, 284, 305, 325, 345, 366, 386, 406, 427, 447, 467, 488]).tolist() # 敲出观察日(交易日)
    #config.knock_o_days = np.array([61, 71, 81, 91, 101, 112, 122, 132, 142, 152, 162, 173, 183, 193, 203, 213, 223, 234, 244, 254, 264, 274, 284, 295, 305, 315, 325, 335, 345, 356, 366, 376, 386, 396, 406, 417, 427, 437, 447, 457, 467, 478, 488]).tolist() # 敲出观察日(交易日)
    #config.knock_o_days = np.array([66, 82, 103, 124, 147, 163, 183, 204, 223, 243, 265, 287, 309, 327, 347, 369, 391, 407, 427, 449, 469, 491]).tolist() # 敲出观察日(交易日)
    #config.knock_o_days = np.array([61, 81, 101, 122, 142, 162, 183, 203, 223, 244, 264, 284, 305, 325, 345, 366, 386, 406, 427, 447, 467, 488, 508, 528, 549, 569, 589, 610, 630, 650, 671, 691, 711, 732]).tolist() # 敲出观察日(交易日)
    
    calc_price_u = 105.0 # 价格点上界
    calc_price_d = 65.0 # 价格点下界
    calc_price_g = 1.0 # 价格点间隔
    #config.calc_price = np.array([65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0, 100.0, 105.0]).tolist() # 计算价格序列
    config.calc_price = np.arange(calc_price_d, calc_price_u + calc_price_g, calc_price_g).tolist() # 含价格点上下界
    
    # 用户不传入则默认与 runs_step、year_days、knock_o_days 一致
    #config.runs_step_n = 720 # 产品自然日数(含延后清算) (可选)
    #config.year_days_n = 365 # 年自然日数量 (可选)
    #config.knock_o_days_n = np.array([90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 480, 510, 540, 570, 600, 630, 660, 690, 720]).tolist() # 敲出日期序列(自然日) (可选)
    #config.trading_days_n = [1, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 18, 19, 20, ..., 701, 704, 705, 706, 707, 708, 711, 712, 713, 714, 715, 718, 719, 720] # 交易日期序列(自然日) (可选)
    
    config.run_from = 0 # 起始天数，第一天为零
    config.run_days = 1 # 运行天数
    
    ret_cols = config.runs_step
    ret_rows = len(config.calc_price)
    
    #print(config.ToJson())
    
    result = None
    
    tasker_test = tasker.Tasker()
    tasker_test.plugin_id = "derivx_barrier_airbag"
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
    Test_DerivX_Barrier_Airbag()
