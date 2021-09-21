
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
import matplotlib.pyplot as plt

import derivx

# GBM：几何布朗运动 (指数布朗运动) Geometric Brownian Motion
# CIR：CIR 模型 (平方根扩散过程) Cox–Ingersoll–Ross model (Square-Root Diffusion)
# JDP：跳跃扩散过程 Jump Diffusion Process
# SVM：Heston 模型 (随机波动率模型) Heston Model (Stochastic Volatility Model)
# SABR：SABR 模型 Stochastic Alpha Beta Rho

class Config_GBM(object):
    def __init__(self):
        self.rand_rows = 0 # 随机数据行数
        self.rand_cols = 0 # 随机数据列数
        self.rand_seed = np.array([]) # 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
        
        self.dual_smooth = True # 对偶平滑路径
        self.runs_size = 0 # 模拟路径数量
        self.runs_step = 0 # 价格变动步数
        self.year_days = 0 # 年交易日数量

    def ToArgs(self):
        return self.__dict__

class Config_CIR(object):
    def __init__(self):
        self.rand_rows = 0 # 随机数据行数
        self.rand_cols = 0 # 随机数据列数
        self.rand_seed = np.array([]) # 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
        
        self.dual_smooth = True # 对偶平滑路径
        self.runs_size = 0 # 模拟路径数量
        self.runs_step = 0 # 价格变动步数
        self.year_days = 0 # 年交易日数量

    def ToArgs(self):
        return self.__dict__

class Config_JDP(object):
    def __init__(self):
        self.rand_rows = 0 # 随机数据行数
        self.rand_cols = 0 # 随机数据列数
        self.rand_seed = np.array([]) # 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
        
        self.dual_smooth = True # 对偶平滑路径
        self.runs_size = 0 # 模拟路径数量
        self.runs_step = 0 # 价格变动步数
        self.year_days = 0 # 年交易日数量

    def ToArgs(self):
        return self.__dict__

class Config_SVM(object):
    def __init__(self):
        self.rand_rows = 0 # 随机数据行数
        self.rand_cols = 0 # 随机数据列数
        self.rand_seed = np.array([]) # 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
        
        self.dual_smooth = True # 对偶平滑路径
        self.runs_size = 0 # 模拟路径数量
        self.runs_step = 0 # 价格变动步数
        self.year_days = 0 # 年交易日数量

    def ToArgs(self):
        return self.__dict__

class Config_SABR(object):
    def __init__(self):
        self.rand_rows = 0 # 随机数据行数
        self.rand_cols = 0 # 随机数据列数
        self.rand_seed = np.array([]) # 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
        
        self.dual_smooth = True # 对偶平滑路径
        self.runs_size = 0 # 模拟路径数量
        self.runs_step = 0 # 价格变动步数
        self.year_days = 0 # 年交易日数量

    def ToArgs(self):
        return self.__dict__

def Test_Stochastic_Model():
    stochastic = derivx.Stochastic("GBM")
    
    config = Config_GBM()
    config.rand_rows = 500000 # 随机数据行数
    config.rand_cols = 250 # 随机数据列数
    config.rand_seed = np.array([0, 1, 2, 3, 4, 5, 6, 7]) # 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
    config.dual_smooth = True # 对偶平滑路径
    config.runs_size = 1000000 # 模拟路径数量
    config.runs_step = 244 # 价格变动步数
    config.year_days = 244 # 年交易日数量
    
    if stochastic.InitArgs(config.ToArgs()) < 0:
        print(stochastic.GetError())
        return
    
    ##################################################
    
    stochastic = derivx.Stochastic("CIR")
    
    config = Config_CIR()
    config.rand_rows = 500000 # 随机数据行数
    config.rand_cols = 250 # 随机数据列数
    config.rand_seed = np.array([0, 1, 2, 3, 4, 5, 6, 7]) # 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
    config.dual_smooth = True # 对偶平滑路径
    config.runs_size = 1000000 # 模拟路径数量
    config.runs_step = 244 # 价格变动步数
    config.year_days = 244 # 年交易日数量
    
    if stochastic.InitArgs(config.ToArgs()) < 0:
        print(stochastic.GetError())
        return
    
    ##################################################
    
    stochastic = derivx.Stochastic("JDP")
    
    config = Config_JDP()
    config.rand_rows = 500000 # 随机数据行数
    config.rand_cols = 250 # 随机数据列数
    config.rand_seed = np.array([0, 1, 2, 3, 4, 5, 6, 7]) # 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
    config.dual_smooth = True # 对偶平滑路径
    config.runs_size = 1000000 # 模拟路径数量
    config.runs_step = 244 # 价格变动步数
    config.year_days = 244 # 年交易日数量
    
    if stochastic.InitArgs(config.ToArgs()) < 0:
        print(stochastic.GetError())
        return
    
    ##################################################
    
    stochastic = derivx.Stochastic("SVM")
    
    config = Config_SVM()
    config.rand_rows = 500000 # 随机数据行数
    config.rand_cols = 250 # 随机数据列数
    config.rand_seed = np.array([0, 1, 2, 3, 4, 5, 6, 7]) # 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
    config.dual_smooth = True # 对偶平滑路径
    config.runs_size = 1000000 # 模拟路径数量
    config.runs_step = 244 # 价格变动步数
    config.year_days = 244 # 年交易日数量
    
    if stochastic.InitArgs(config.ToArgs()) < 0:
        print(stochastic.GetError())
        return
    
    ##################################################
    
    stochastic = derivx.Stochastic("SABR")
    
    config = Config_SABR()
    config.rand_rows = 500000 # 随机数据行数
    config.rand_cols = 250 # 随机数据列数
    config.rand_seed = np.array([0, 1, 2, 3, 4, 5, 6, 7]) # 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
    config.dual_smooth = True # 对偶平滑路径
    config.runs_size = 1000000 # 模拟路径数量
    config.runs_step = 244 # 价格变动步数
    config.year_days = 244 # 年交易日数量
    
    if stochastic.InitArgs(config.ToArgs()) < 0:
        print(stochastic.GetError())
        return

if __name__ == "__main__":
    Test_Stochastic_Model()
