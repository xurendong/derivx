
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
# HEST：Heston 模型 Heston Model
# SABR：SABR 模型 Stochastic Alpha Beta Rho

def ShowPlot_Frequency(price, title, xlabel):
    n, bins, patches = plt.hist(price[:, -1], bins = 50, normed = True, facecolor = "blue", alpha = 0.75)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Frequency")
    plt.grid(True, alpha = 0.5)
    plt.show()

def ShowPlot_Distribution(price, path, step, title, ylabel):
    plt.figure()
    ax = plt.subplot2grid((1, 1), (0, 0), colspan = 1, rowspan = 1)
    ax.set_xlabel("Steps")
    ax.set_ylabel(ylabel)
    for i in range(path):
        ax.plot(range(step), price[i, :], color = np.random.rand(3), ls = "-", lw = 1.0)
    #ax.legend(loc = "best") # 不显示图例
    ax.margins(0, 0) # 0 ~ 1
    ax.set_title(title)
    plt.subplots_adjust(left = 0.05, bottom = 0.05, right = 0.99, top = 0.98, wspace = 0.0, hspace = 0.0)
    plt.grid(True, alpha = 0.5)
    plt.show()

class Config_GBM(object):
    def __init__(self):
        self.rand_rows = 0 # 随机数据行数
        self.rand_cols = 0 # 随机数据列数
        self.rand_seed = np.array([]) # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
        self.runs_size = 0 # 模拟路径数量
        self.runs_step = 0 # 价格变动步数
        self.year_days = 0 # 年交易日数量
        self.price = 0.0 # 初始价格
        self.sigma = 0.0 # 波动率
        self.risk_free_rate = 0.0 # 无风险利率
        self.basis_rate = 0.0 # 股息率或贴水率

    def ToArgs(self):
        return self.__dict__

class Config_CIR(object):
    def __init__(self):
        self.rand_rows = 0 # 随机数据行数
        self.rand_cols = 0 # 随机数据列数
        self.rand_seed = np.array([]) # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
        self.runs_size = 0 # 模拟路径数量
        self.runs_step = 0 # 价格变动步数
        self.year_days = 0 # 年交易日数量
        self.price = 0.0 # 初始价格
        self.sigma = 0.0 # 波动率
        self.kappa = 0.0 # 均值回归系数
        self.theta = 0.0 # 长期均值项

    def ToArgs(self):
        return self.__dict__

class Config_JDP(object):
    def __init__(self):
        self.rand_rows = 0 # 随机数据行数
        self.rand_cols = 0 # 随机数据列数
        self.rand_seed = np.array([]) # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
        self.runs_size = 0 # 模拟路径数量
        self.runs_step = 0 # 价格变动步数
        self.year_days = 0 # 年交易日数量
        self.price = 0.0 # 初始价格
        self.sigma = 0.0 # 波动率
        self.risk_free_rate = 0.0 # 无风险利率
        self.mu = 0.0 # 预期跳跃均值，正负决定跳跃方向
        self.lamb = 0.0 # 跳跃强度
        self.delta = 0.0 # 跳跃强度标准差

    def ToArgs(self):
        return self.__dict__

class Config_HEST(object):
    def __init__(self):
        self.rand_rows = 0 # 随机数据行数
        self.rand_cols = 0 # 随机数据列数
        self.rand_seed = np.array([]) # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
        self.runs_size = 0 # 模拟路径数量
        self.runs_step = 0 # 价格变动步数
        self.year_days = 0 # 年交易日数量
        self.price = 0.0 # 初始价格
        self.sigma = 0.0 # 初始波动率
        self.risk_free_rate = 0.0 # 无风险利率
        self.kappa = 0.0 # 波动率均值回归系数
        self.theta = 0.0 # 波动率长期均值项
        self.sigma_sigma = 0.0 # 波动率的波动率
        self.rho = 0.0 # 两个随机过程的相关系数

    def ToArgs(self):
        return self.__dict__

class Config_SABR(object):
    def __init__(self):
        self.rand_rows = 0 # 随机数据行数
        self.rand_cols = 0 # 随机数据列数
        self.rand_seed = np.array([]) # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
        self.runs_size = 0 # 模拟路径数量
        self.runs_step = 0 # 价格变动步数
        self.year_days = 0 # 年交易日数量
        self.price = 0.0 # 初始价格
        self.sigma = 0.0 # 初始波动率
        self.beta = 0.0 # 价格分布力度
        self.sigma_sigma = 0.0 # 波动率的波动率
        self.rho = 0.0 # 两个随机过程的相关系数

    def ToArgs(self):
        return self.__dict__

def Test_Stochastic_Model_GBM():
    stochastic = derivx.Stochastic("GBM")
    
    config = Config_GBM()
    config.rand_rows = 10000 # 随机数据行数
    config.rand_cols = 250 # 随机数据列数
    config.rand_seed = np.array([0, 1, 2, 3, 4, 5, 6, 7]) # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
    config.runs_size = 10000 # 模拟路径数量
    config.runs_step = 250 # 价格变动步数
    config.year_days = 244 # 年交易日数量
    config.price = 1.0 # 初始价格
    config.sigma = 0.24 # 波动率
    config.risk_free_rate = 0.03 # 无风险利率
    config.basis_rate = 0.0 # 股息率或贴水率
    
    if stochastic.InitArgs(config.ToArgs()) < 0:
        print(stochastic.GetError())
        return
    
    result = np.zeros((config.runs_size, config.runs_step))
    if stochastic.MakeData(result) < 0:
        print(stochastic.GetError())
        return
    #print(result)
    ShowPlot_Frequency(result, "Final-Price-Frequency", "Final-Price")
    ShowPlot_Distribution(result, 1000, config.runs_step, "Price - Steps", "Price")

def Test_Stochastic_Model_CIR():
    stochastic = derivx.Stochastic("CIR")
    
    config = Config_CIR()
    config.rand_rows = 10000 # 随机数据行数
    config.rand_cols = 250 # 随机数据列数
    config.rand_seed = np.array([0, 1, 2, 3, 4, 5, 6, 7]) # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
    config.runs_size = 10000 # 模拟路径数量
    config.runs_step = 250 # 价格变动步数
    config.year_days = 244 # 年交易日数量
    config.price = 0.05 # 初始价格
    config.sigma = 0.1 # 波动率
    config.kappa = 3.0 # 均值回归系数
    config.theta = 0.02 # 长期均值项
    
    if stochastic.InitArgs(config.ToArgs()) < 0:
        print(stochastic.GetError())
        return
    
    result = np.zeros((config.runs_size, config.runs_step))
    if stochastic.MakeData(result) < 0:
        print(stochastic.GetError())
        return
    #print(result)
    ShowPlot_Frequency(result, "Final-Price-Frequency", "Final-Price")
    ShowPlot_Distribution(result, 1000, config.runs_step, "Price - Steps", "Price")

def Test_Stochastic_Model_JDP():
    stochastic = derivx.Stochastic("JDP")
    
    config = Config_JDP()
    config.rand_rows = 10000 # 随机数据行数
    config.rand_cols = 250 # 随机数据列数
    config.rand_seed = np.array([0, 1, 2, 3, 4, 5, 6, 7]) # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
    config.runs_size = 10000 # 模拟路径数量
    config.runs_step = 250 # 价格变动步数
    config.year_days = 244 # 年交易日数量
    config.price = 1.0 # 初始价格
    config.sigma = 0.2 # 波动率
    config.risk_free_rate = 0.05 # 无风险利率
    config.mu = -0.6 # 预期跳跃均值，正负决定跳跃方向
    config.lamb = 0.75 # 跳跃强度
    config.delta = 0.25 # 跳跃强度标准差
    
    if stochastic.InitArgs(config.ToArgs()) < 0:
        print(stochastic.GetError())
        return
    
    result = np.zeros((config.runs_size, config.runs_step))
    if stochastic.MakeData(result) < 0:
        print(stochastic.GetError())
        return
    #print(result)
    ShowPlot_Frequency(result, "Final-Price-Frequency", "Final-Price")
    ShowPlot_Distribution(result, 1000, config.runs_step, "Price - Steps", "Price")

def Test_Stochastic_Model_HEST():
    stochastic = derivx.Stochastic("HEST")
    
    config = Config_HEST()
    config.rand_rows = 10000 # 随机数据行数
    config.rand_cols = 250 # 随机数据列数
    config.rand_seed = np.array([0, 1, 2, 3, 4, 5, 6, 7]) # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
    config.runs_size = 10000 # 模拟路径数量
    config.runs_step = 250 # 价格变动步数
    config.year_days = 244 # 年交易日数量
    config.price = 1.0 # 初始价格
    config.sigma = 0.1 # 初始波动率
    config.risk_free_rate = 0.03 # 无风险利率
    config.kappa = 3.0 # 波动率均值回归系数
    config.theta = 0.25 # 波动率长期均值项
    config.sigma_sigma = 0.1 # 波动率的波动率
    config.rho = 0.6 # 两个随机过程的相关系数
    
    if stochastic.InitArgs(config.ToArgs()) < 0:
        print(stochastic.GetError())
        return
    
    result = np.zeros((config.runs_size, config.runs_step))
    if stochastic.MakeData(result) < 0:
        print(stochastic.GetError())
        return
    #print(result)
    ShowPlot_Frequency(result, "Final-Price-Frequency", "Final-Price")
    ShowPlot_Distribution(result, 1000, config.runs_step, "Price - Steps", "Price")

def Test_Stochastic_Model_SABR():
    stochastic = derivx.Stochastic("SABR")
    
    config = Config_SABR()
    config.rand_rows = 10000 # 随机数据行数
    config.rand_cols = 250 # 随机数据列数
    config.rand_seed = np.array([0, 1, 2, 3, 4, 5, 6, 7]) # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
    config.runs_size = 10000 # 模拟路径数量
    config.runs_step = 250 # 价格变动步数
    config.year_days = 244 # 年交易日数量
    config.price = 0.06 # 初始价格
    config.sigma = 0.2 # 初始波动率
    config.beta = 0.5 # 价格分布力度
    config.sigma_sigma = 0.2 # 波动率的波动率
    config.rho = 0.6 # 两个随机过程的相关系数
    
    if stochastic.InitArgs(config.ToArgs()) < 0:
        print(stochastic.GetError())
        return
    
    result = np.zeros((config.runs_size, config.runs_step))
    if stochastic.MakeData(result) < 0:
        print(stochastic.GetError())
        return
    #print(result)
    ShowPlot_Frequency(result, "Final-Price-Frequency", "Final-Price")
    ShowPlot_Distribution(result, 1000, config.runs_step, "Price - Steps", "Price")

if __name__ == "__main__":
    Test_Stochastic_Model_GBM()
    Test_Stochastic_Model_CIR()
    Test_Stochastic_Model_JDP()
    Test_Stochastic_Model_HEST()
    Test_Stochastic_Model_SABR()
