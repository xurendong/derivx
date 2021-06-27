
# -*- coding: utf-8 -*-

# Copyright (c) 2021-2021 the DerivX authors
# All rights reserved.
#
# The project sponsor and lead author is Xu Rendong.
# E-mail: xrd@ustc.edu, QQ: 277195007, WeChat: ustc_xrd
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
        self.runs_size = 0 # 模拟路径数量
        self.runs_step = 0 # 价格变动步数
        self.year_days = 0 # 年交易日数量
        self.start_price = 0.0 # 初始价格
        self.strike_rice = 0.0 # 敲入后执行价格
        self.knock_o_ratio = 0.0 # 敲出比率，非百分比
        self.knock_i_ratio = 0.0 # 敲入比率，非百分比
        self.sigma = 0.0 # 波动率
        self.risk_free_rate = 0.0 # 无风险利率
        self.basis_rate = 0.0 # 股息或贴水
        self.coupon_rate = 0.0 # 客户年化收益率
        self.margin_rate = 0.0 # 保证金比例
        self.margin_interest = 0.0 # 保证金利率
        self.price_limit_ratio = 0.0 # 涨跌停限制幅度
        self.calc_price_u = 0.0 # 价格点上界
        self.calc_price_d = 0.0 # 价格点下界
        self.calc_price_g = 0.0 # 价格点间隔
        self.run_from = 0 # 起始天数，第一天为零
        self.run_days = 0 # 运行天数
        self.knock_o_days = np.array([]) # 敲出日期序列

    def ToArgs(self):
        return self.__dict__

def FigureResult(config, result):
    figure = plt.figure()
    ax = Axes3D(figure)
    x = np.arange(0, config.runs_step, 1)
    y = np.arange(config.calc_price_d - config.calc_price_g, config.calc_price_u, config.calc_price_g)
    X, Y = np.meshgrid(x, y)
    ax.plot_surface(X, Y, result, rstride = 1, cstride = 1, cmap = plt.get_cmap("rainbow"))
    plt.show()

def ExportResult(config, result, file_path):
    export_days = config.run_days
    if export_days > 255: # Excel 最大 256 列，首列显示价格，剩余可用 255 列
        export_days = 255
        print("提示：Excel 最大 256 列，剩余 %d 列数据未作导出！" % (config.run_days - 255))
    df_result = pd.DataFrame(result[:, config.run_from : (config.run_from + export_days)]).iloc[::-1] # 上下倒下顺序
    df_result.index = np.arange(config.calc_price_u, config.calc_price_d - config.calc_price_g, -config.calc_price_g)
    df_result.columns = ["day_%d" % (days + 1) for days in np.arange(config.run_from, config.run_from + export_days, 1)]
    df_result.to_excel(file_path, sheet_name = "result")
    print("导出结果：%s" % file_path)

def Test_Snowball():
    config = Config()
    config.runs_size = 10000 # 模拟路径数量
    config.runs_step = 491 # 价格变动步数
    config.year_days = 244 # 年交易日数量
    config.start_price = 100.0 # 初始价格
    config.strike_rice = 100.0 # 敲入后执行价格
    config.knock_o_ratio = 1.0 # 敲出比率，非百分比
    config.knock_i_ratio = 0.7 # 敲入比率，非百分比
    config.sigma = 0.16 # 波动率
    config.risk_free_rate = 0.03 # 无风险利率
    config.basis_rate = 0.05 # 股息或贴水
    config.coupon_rate = 0.11 # 客户年化收益率
    config.margin_rate = 1.0 # 保证金比例
    config.margin_interest = 0.03 # 保证金利率
    config.price_limit_ratio = 0.1 # 涨跌停限制幅度
    #config.knock_o_days = np.array([20, 40, 60]) # 敲出观察日
    config.knock_o_days = np.array([66, 82, 103, 124, 147, 163, 183, 204, 223, 243, 265, 287, 309, 327, 347, 369, 391, 407, 427, 449, 469, 491]) # 敲出观察日
    config.calc_price_u = 105.0 # 价格点上界
    config.calc_price_d = 65.0 # 价格点下界
    config.calc_price_g = 1.0 # 价格点间隔
    config.run_from = 0 # 起始天数，第一天为零
    config.run_days = 1 # 运行天数
    
    ret_rows = int( ( config.calc_price_u - config.calc_price_d ) / config.calc_price_g ) + 1
    ret_cols = config.runs_step
    
    #print(derivx.Version())
    
    snowball = derivx.Snowball()
    
    if snowball.InitArgs(config.ToArgs()) < 0:
        print(snowball.GetMsg())
        return
    if snowball.InitPath() < 0:
        print(snowball.GetMsg())
        return
    if snowball.SavePath("./path_data.path") < 0:
        print(snowball.GetMsg())
        return
    if snowball.LoadPath("./path_data.path") < 0:
        print(snowball.GetMsg())
        return
    
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
    #    snowball.CalcGreeks(result, flag)
    #    FigureResult(config, result)
    #    ExportResult(config, result, "/export_greeks_%s.xls" % name)

if __name__ == "__main__":
    Test_Snowball()
