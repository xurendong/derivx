
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

class Config(object):
    def __init__(self):
        self.runs_seed = False # 动态路径种子
        self.runs_size = 0 # 模拟路径数量
        self.runs_step = 0 # 价格变动步数
        self.year_days = 0 # 年交易日数量
        self.notional = 0.0 # 名义本金
        self.start_price = 0.0 # 初始价格
        self.strike_rice = 0.0 # 敲入后执行价格
        self.knock_o_ratio = 0.0 # 敲出比率，非百分比
        self.knock_i_ratio = 0.0 # 敲入比率，非百分比
        self.knock_o_steps = 0.0 # 敲出比例逐月递减率
        self.knock_i_valid = True # 是否有下方敲入障碍
        self.knock_i_occur = False # 是否已经发生敲入
        self.knock_i_margin_call = True # 是否追加保证金
        self.sigma = 0.0 # 波动率 # InitPath
        self.risk_free_rate = 0.0 # 无风险利率 # InitPath
        self.basis_rate = 0.0 # 股息或贴水 # InitPath
        self.coupon_rate = 0.0 # 客户年化收益率
        self.margin_rate = 0.0 # 保证金比例
        self.margin_interest = 0.0 # 保证金利率
        self.price_limit_ratio = 0.0 # 涨跌停限制幅度 # InitPath
        self.prefix_coupon = 0.0 # 不管敲入敲出和到期时间，客户都要求得到固定收益，相当于前端扣费的意思
        self.prefix_coupon_ann = False # False 为绝对收益率，True 为年化收益率
        self.prefix_coupon_use = False # 是否支付 prefix 收益
        self.ukiuko_coupon = 0.0 # 对于无敲出无敲入的情况，客户只要求得到固定收益
        self.ukiuko_coupon_ann = False # False 为绝对收益率，True 为年化收益率
        self.ukiuko_coupon_use = False # 是否支付 ukiuko 收益
        self.calc_price = np.array([]) # 计算价格序列
        self.run_from = 0 # 起始天数，第一天为零
        self.run_days = 0 # 运行天数
        self.knock_o_days = np.array([]) # 敲出日期序列
        self.knock_o_rate = np.array([]) # 敲出比率序列

    def ToArgs(self):
        return self.__dict__

def FigureResult(config, result):
    figure = plt.figure()
    ax = Axes3D(figure)
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

def MakeStepDown(duration, observe_start, default_ratio, stepdown_start, stepdown_ratio):
    stepdown = np.array([])
    stepdown_times = duration - stepdown_start + 2
    for i in range(stepdown_start - observe_start - 1):
        stepdown = np.append(stepdown, default_ratio)
    for i in range(stepdown_times):
        stepdown = np.append(stepdown, default_ratio - stepdown_ratio * i)
    print(stepdown)
    return stepdown

def Test_Snowball():
    config = Config()
    config.runs_seed = False # 动态路径种子
    config.runs_size = 100000 # 模拟路径数量
    config.runs_step = 488 # 价格变动步数
    config.year_days = 244 # 年交易日数量
    
    config.notional = 100000.0 # 名义本金
    config.start_price = 100.0 # 初始价格
    config.strike_rice = 100.0 # 敲入后执行价格
    config.knock_o_ratio = 1.0 # 敲出比率，非百分比
    config.knock_i_ratio = 0.7 # 敲入比率，非百分比
    config.knock_o_steps = 0.0 # 敲出比例逐月递减率
    config.knock_i_valid = True # 是否有下方敲入障碍
    config.knock_i_occur = False # 是否已经发生敲入
    config.knock_i_margin_call = True # 是否敲入后可追加保证金
    config.sigma = 0.16 # 波动率 # InitPath
    config.risk_free_rate = 0.03 # 无风险利率 # InitPath
    config.basis_rate = 0.05 # 股息或贴水 # InitPath
    config.coupon_rate = 0.11 # 客户年化收益率
    config.margin_rate = 1.0 # 保证金比例
    config.margin_interest = 0.03 # 保证金利率
    config.price_limit_ratio = 0.1 # 涨跌停限制幅度 # InitPath
    
    config.prefix_coupon = 0.0 # 不管敲入敲出和到期时间，客户都要求得到固定收益，相当于前端扣费的意思
    config.prefix_coupon_ann = False # False 为绝对收益率，True 为年化收益率
    config.prefix_coupon_use = False # 是否支付 prefix 收益
    config.ukiuko_coupon = 0.0 # 对于无敲出无敲入的情况，客户只要求得到固定收益
    config.ukiuko_coupon_ann = False # False 为绝对收益率，True 为年化收益率
    config.ukiuko_coupon_use = False # 是否支付 ukiuko 收益
    
    #  1   2   3   4    5    6    7    8    9   10   11   12   13   14   15   16   17   18   19   20   21   22   23   24   25   26   27   28   29   30   31   32   33   34   35   36  
    # 20, 40, 61, 81, 101, 122, 142, 162, 183, 203, 223, 244, 264, 284, 305, 325, 345, 366, 386, 406, 427, 447, 467, 488, 508, 528, 549, 569, 589, 610, 630, 650, 671, 691, 711, 732]
    
    #config.knock_o_days = np.array([20, 40, 60]) # 敲出观察日
    config.knock_o_days = np.array([61, 81, 101, 122, 142, 162, 183, 203, 223, 244, 264, 284, 305, 325, 345, 366, 386, 406, 427, 447, 467, 488]) # 敲出观察日
    #config.knock_o_days = np.array([61, 71, 81, 91, 101, 112, 122, 132, 142, 152, 162, 173, 183, 193, 203, 213, 223, 234, 244, 254, 264, 274, 284, 295, 305, 315, 325, 335, 345, 356, 366, 376, 386, 396, 406, 417, 427, 437, 447, 457, 467, 478, 488]) # 敲出观察日
    #config.knock_o_days = np.array([66, 82, 103, 124, 147, 163, 183, 204, 223, 243, 265, 287, 309, 327, 347, 369, 391, 407, 427, 449, 469, 491]) # 敲出观察日
    #config.knock_o_days = np.array([61, 81, 101, 122, 142, 162, 183, 203, 223, 244, 264, 284, 305, 325, 345, 366, 386, 406, 427, 447, 467, 488, 508, 528, 549, 569, 589, 610, 630, 650, 671, 691, 711, 732]) # 敲出观察日
    
    #config.knock_o_rate = MakeStepDown(duration = 24, observe_start = 3, default_ratio = config.knock_o_ratio, stepdown_start = 4, stepdown_ratio = 0.01)
    #   1     2     3     4     5     6     7     8     9    10    11    12    13    14    15    16    17    18    19    20    21    22    23    24
    # 1.0, 0.99, 0.98, 0.97, 0.96, 0.95, 0.94, 0.93, 0.92, 0.91, 0.90, 0.89, 0.88, 0.87, 0.86, 0.85, 0.84, 0.83, 0.82, 0.81, 0.80, 0.79, 0.78, 0.77
    
    #config.knock_o_rate = MakeStepDown(duration = 36, observe_start = 6, default_ratio = config.knock_o_ratio, stepdown_start = 9, stepdown_ratio = 0.005)
    #   1      2     3      4     5      6     7      8     9     10    11     12    13     14    15     16    17     18    19     20   21     22    23     24    25     26    27     28    29     30    31     32
    # 1.0, 0.995, 0.99, 0.985, 0.98, 0.975, 0.97, 0.965, 0.96, 0.955, 0.95, 0.945, 0.94, 0.935, 0.93, 0.925, 0.92, 0.915, 0.91, 0.905, 0.9, 0.895, 0.89, 0.885, 0.88, 0.875, 0.87, 0.865, 0.86, 0.855, 0.85, 0.845
    
    config.knock_o_rate = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]) * config.knock_o_ratio # 敲出观察率
    #config.knock_o_rate = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]) * config.knock_o_ratio # 敲出观察率
    for i in range(len(config.knock_o_rate)):
        config.knock_o_rate[i] = config.knock_o_rate[i] - i * config.knock_o_steps
    #config.knock_o_rate = np.array([(1.0 - i * config.knock_o_steps) for i in range(len(config.knock_o_days))]) # 敲出观察率
    #config.knock_o_rate = np.array([1.0, 0.995, 0.99, 0.985, 0.98, 0.975, 0.97, 0.965, 0.96, 0.955, 0.95, 0.945, 0.94, 0.935, 0.93, 0.925, 0.92, 0.915, 0.91, 0.905, 0.9, 0.895]) # 敲出观察率
    #config.knock_o_rate = np.array([1.0, 0.99, 0.98, 0.97, 0.96, 0.95, 0.94, 0.93, 0.92, 0.91, 0.9, 0.89, 0.88, 0.87, 0.86, 0.85, 0.84, 0.83, 0.82, 0.81, 0.8, 0.79]) # 敲出观察率
    #config.knock_o_rate = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]) # 敲出观察率
    print(config.knock_o_rate)
    
    calc_price_u = 105.0 # 价格点上界
    calc_price_d = 65.0 # 价格点下界
    calc_price_g = 1.0 # 价格点间隔
    #config.calc_price = np.array([65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0, 100.0, 105.0]) # 计算价格序列
    config.calc_price = np.arange(calc_price_d, calc_price_u + calc_price_g, calc_price_g) # 含价格点上下界
    
    config.run_from = 0 # 起始天数，第一天为零
    config.run_days = 1 # 运行天数
    
    ret_cols = config.runs_step
    ret_rows = len(config.calc_price)
    
    snowball = derivx.Snowball()
    
    if snowball.InitArgs(config.ToArgs()) < 0:
        print(snowball.GetMsg())
        return
    
    if snowball.LoadPath("./path_data.path") < 0:
        print(snowball.GetMsg())
        print("尝试 生成 路径数据 ...")
        if snowball.InitPath() < 0:
            print(snowball.GetMsg())
            return
        else:
            print("生成 路径数据 完成。")
            if snowball.SavePath("./path_data.path") < 0:
                print(snowball.GetMsg())
                return
            else:
                print("保存 路径数据 完成。")
    else:
        print("加载 路径数据 完成。")
    
    #if snowball.InitPath() < 0:
    #    print(snowball.GetMsg())
    #    return
    #if snowball.SavePath("./path_data.path") < 0:
    #    print(snowball.GetMsg())
    #    return
    #if snowball.LoadPath("./path_data.path") < 0:
    #    print(snowball.GetMsg())
    #    return
    
    coupon = np.zeros(1)
    snowball.CalcCoupon(coupon)
    print("coupon:", coupon)
    
    #payoff = np.zeros((ret_rows, ret_cols))
    #snowball.CalcPayoff(payoff)
    #FigureResult(config, payoff)
    #ExportResult(config, payoff, "/export_payoff.xls")
    
    #greek_flags = {"theta":"t"}
    #greek_flags = {"delta":"d", "gamma":"g", "vega":"v", "theta":"t", "rho":"r"}
    #for name, flag in greek_flags.items():
    #    result = np.zeros((ret_rows, ret_cols))
    #    snowball.CalcGreeks(flag, result)
    #    FigureResult(config, result)
    #    ExportResult(config, result, "/export_greeks_%s.xls" % name)

if __name__ == "__main__":
    Test_Snowball()
