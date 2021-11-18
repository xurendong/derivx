
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

import derivx

g_uoc_dop = 1 # 向上敲出看涨，向下敲出看跌，双鲨

class Config(object):
    def __init__(self):
        self.rand_rows = 0 # 随机数据行数 # InitRand
        self.rand_cols = 0 # 随机数据列数 # InitRand
        self.rand_seed = np.array([]) # 随机数据种子 # InitRand # 非负整数，有效位数不超逻辑处理器数量
        
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
        self.x = 0.0 # 敲出后需支付的资金
        self.v = 0.0 # 波动率 # 双鲨未用
        self.r = 0.0 # 无风险利率 # 双鲨未用
        self.q = 0.0 # 年化分红率 # 双鲨未用
        self.t = 0.0 # 年化到期期限 # 双鲨未用
        self.p = 0.0 # 参与率，未敲出情况下客户对收益的占比要求
        self.is_kop_delay = False # 敲出后是立即还是延期支付资金
        self.barrier_type = 0 # 障碍类型

    def ToArgs(self):
        return self.__dict__

def Test_Barrier_Double():
    config = Config()
    config.rand_rows = 50000 # 随机数据行数 # InitRand
    config.rand_cols = 250 # 随机数据列数 # InitRand
    config.rand_seed = np.array([0, 1, 2, 3, 4, 5, 6, 7]) # 随机数据种子 # InitRand # 非负整数，有效位数不超逻辑处理器数量
    
    config.dual_smooth = True # 对偶平滑路径 # InitPath
    config.runs_size = 100000 # 模拟路径数量 # InitPath
    config.runs_step = 244 # 价格变动步数 # InitPath
    config.year_days = 244 # 年交易日数量 # InitPath
    config.sigma = 0.16 # 波动率 # InitPath
    config.risk_free_rate = 0.03 # 无风险利率 # InitPath
    config.basis_rate = 0.06 # 股息或贴水 # InitPath
    config.price_limit_ratio = 0.1 # 涨跌停限制幅度 # InitPath
    config.price_limit_style = 0 # 涨跌停限制方式，0 不限制，1 超限部分移至下日，2 超限部分直接削掉 # InitPath
    
    config.s = 100.0 # 标的价格
    config.h_l = 95.0 # 障碍价格，低
    config.h_h = 105.0 # 障碍价格，高
    config.k_l = 99.0 # 行权价格，低
    config.k_h = 101.0 # 行权价格，高
    config.x = 3.5 # 敲出后需支付的资金
    # config.v = 0.16 # 波动率 # 双鲨未用
    # config.r = 0.03 # 无风险利率 # 双鲨未用
    # config.q = 0.06 # 年化分红率 # 双鲨未用
    # config.t = 1.0 # 年化到期期限 # 双鲨未用
    config.p = 1.0 # 参与率，未敲出情况下客户对收益的占比要求
    config.is_kop_delay = True # 敲出后是立即还是延期支付资金
    config.barrier_type = g_uoc_dop # 障碍类型
    
    barrier = derivx.Barrier("Double")
    
    if barrier.InitArgs(config.ToArgs()) < 0:
        print(barrier.GetError())
        return
    
    if barrier.InitRand() < 0:
        print(barrier.GetError())
        return
    # 除非电脑性能较差，否则不推荐使用 SaveRand() 和 LoadRand() 了
    # 最好将影响随机数据的参数都包含在文件名中，避免导入的随机数据与所设参数不一致
    #rand_file = "./rand_data_%d_%d_%d.rand" % (config.rand_rows, config.rand_cols, config.rand_seed[0])
    #if barrier.SaveRand(rand_file) < 0:
    #    print(barrier.GetError())
    #    return
    #if barrier.LoadRand(rand_file) < 0:
    #    print(barrier.GetError())
    #    return
    
    if barrier.InitPath() < 0:
        print(barrier.GetError())
        return
    # 除非电脑性能较差，否则不推荐使用 SavePath() 和 LoadPath() 了
    # 最好将影响路径数据的参数都包含在文件名中，避免导入的路径数据与所设参数不一致
    #path_file = "./path_data_%d_%d_%d_%d_%.3f_%.3f_%.3f_%.3f_%d.path" % \
    #    (config.dual_smooth, config.runs_size, config.runs_step, config.year_days, 
    #     config.sigma, config.risk_free_rate, config.basis_rate, config.price_limit_ratio, config.price_limit_style)
    #if barrier.SavePath(path_file) < 0:
    #    print(barrier.GetError())
    #    return
    #if barrier.LoadPath(path_file) < 0:
    #    print(barrier.GetError())
    #    return
    
    print("price:", barrier.CalcPrice())
    print("payoff:", barrier.CalcPayoff())

if __name__ == "__main__":
    Test_Barrier_Double()
