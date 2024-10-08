
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
# 1、演示几种随机过程模型和价格路径生成；
# 2、演示模型参数设置；
# 3、演示使用 GetKernel 方法获取 kernel 实例；
# 4、演示 tasker 任务信息创建；
# 5、演示 同步模式 AssignTask 任务执行调用；

# 注意：版本 >= 0.5.14 的，编译环境 Visual Studio 从 17.9.X 升级为 17.10.X 后，
#      对于 Python 3.6、3.7、3.8、3.9、3.10、3.11 存在一些兼容问题，
#      需要将 import cyberx 语句放在 import 如 pandas、PyQt5 等其他第三方库之前，
#      对于 Python 3.12 则仍然可以正常地任意放置，初始化 cyberx.Kernel 时不会异常。

import json

import cyberx

import numpy as np
import matplotlib.pyplot as plt

import syscfg
import tasker
# import cyberx

func_make_data_gbm  = 1
func_make_data_cgbm = 2
func_make_data_gbb  = 3
func_make_data_cir  = 4
func_make_data_jdp  = 5
func_make_data_hest = 6
func_make_data_sabr = 7
func_make_data_user = 8

# GBM：几何 (指数) 布朗运动 Geometric Brownian Motion
# CGBM：具有相关性的几何 (指数）布朗运动 Correlated Geometric Brownian Motion
# GBB：几何 (指数) 布朗桥 Geometric Brownian Bridge
# CIR：CIR 模型 (平方根扩散过程) Cox–Ingersoll–Ross model (Square-Root Diffusion)
# JDP：跳跃扩散过程 Jump Diffusion Process
# HEST：Heston 模型 Heston Model
# SABR：SABR 模型 Stochastic Alpha Beta Rho
# USER：仅用于随机过程数据测试

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
        self.dimension = 0 # 随机数据维度 # 未使用
        self.rand_seed = [] # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
        self.runs_size = 0 # 模拟路径数量
        self.runs_step = 0 # 价格变动步数
        self.year_days = 0 # 年交易日数量
        self.price = 0.0 # 初始价格
        self.sigma = 0.0 # 波动率
        self.risk_free_rate = 0.0 # 无风险利率
        self.basis_rate = 0.0 # 股息率或贴水率

    def ToJson(self):
        return json.dumps(self.__dict__)

class Config_CGBM(object):
    def __init__(self):
        self.rand_rows = 0 # 随机数据行数
        self.rand_cols = 0 # 随机数据列数
        self.dimension = 0 # 随机数据维度 # 未使用
        self.rand_seed = [] # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
        self.runs_size = 0 # 模拟路径数量
        self.runs_step = 0 # 价格变动步数
        self.year_days = 0 # 年交易日数量
        self.asset = 0 # 标的数量
        self.corco = [] # 相关系数矩阵
        self.price = [] # 初始价格
        self.sigma = [] # 波动率
        self.risk_free_rate = [] # 无风险利率
        self.basis_rate = [] # 股息率或贴水率

    def ToJson(self):
        return json.dumps(self.__dict__)

class Config_GBB(object):
    def __init__(self):
        self.rand_rows = 0 # 随机数据行数
        self.rand_cols = 0 # 随机数据列数
        self.dimension = 0 # 随机数据维度 # 未使用
        self.rand_seed = [] # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
        self.runs_size = 0 # 模拟路径数量
        self.runs_step = 0 # 价格变动步数
        self.year_days = 0 # 年交易日数量
        self.price = 0.0 # 初始价格
        self.sigma = 0.0 # 波动率
        self.risk_free_rate = 0.0 # 无风险利率
        self.basis_rate = 0.0 # 股息率或贴水率

    def ToJson(self):
        return json.dumps(self.__dict__)

class Config_CIR(object):
    def __init__(self):
        self.rand_rows = 0 # 随机数据行数
        self.rand_cols = 0 # 随机数据列数
        self.dimension = 0 # 随机数据维度 # 未使用
        self.rand_seed = [] # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
        self.runs_size = 0 # 模拟路径数量
        self.runs_step = 0 # 价格变动步数
        self.year_days = 0 # 年交易日数量
        self.price = 0.0 # 初始价格
        self.sigma = 0.0 # 波动率
        self.kappa = 0.0 # 均值回归系数
        self.theta = 0.0 # 长期均值项

    def ToJson(self):
        return json.dumps(self.__dict__)

class Config_JDP(object):
    def __init__(self):
        self.rand_rows = 0 # 随机数据行数
        self.rand_cols = 0 # 随机数据列数
        self.dimension = 0 # 随机数据维度 # 未使用
        self.rand_seed = [] # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
        self.runs_size = 0 # 模拟路径数量
        self.runs_step = 0 # 价格变动步数
        self.year_days = 0 # 年交易日数量
        self.price = 0.0 # 初始价格
        self.sigma = 0.0 # 波动率
        self.risk_free_rate = 0.0 # 无风险利率
        self.mu = 0.0 # 预期跳跃均值，正负决定跳跃方向
        self.lamb = 0.0 # 跳跃强度
        self.delta = 0.0 # 跳跃强度标准差

    def ToJson(self):
        return json.dumps(self.__dict__)

class Config_HEST(object):
    def __init__(self):
        self.rand_rows = 0 # 随机数据行数
        self.rand_cols = 0 # 随机数据列数
        self.dimension = 0 # 随机数据维度 # 未使用
        self.rand_seed = [] # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
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

    def ToJson(self):
        return json.dumps(self.__dict__)

class Config_SABR(object):
    def __init__(self):
        self.rand_rows = 0 # 随机数据行数
        self.rand_cols = 0 # 随机数据列数
        self.dimension = 0 # 随机数据维度 # 未使用
        self.rand_seed = [] # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
        self.runs_size = 0 # 模拟路径数量
        self.runs_step = 0 # 价格变动步数
        self.year_days = 0 # 年交易日数量
        self.price = 0.0 # 初始价格
        self.sigma = 0.0 # 初始波动率
        self.beta = 0.0 # 价格分布力度
        self.sigma_sigma = 0.0 # 波动率的波动率
        self.rho = 0.0 # 两个随机过程的相关系数

    def ToJson(self):
        return json.dumps(self.__dict__)

class Config_USER(object):
    def __init__(self):
        self.rand_rows = 0 # 随机数据行数
        self.rand_cols = 0 # 随机数据列数
        self.dimension = 0 # 随机数据维度
        self.rand_seed = [] # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
        self.runs_size = 0 # 模拟路径数量
        self.runs_step = 0 # 价格变动步数
        self.year_days = 0 # 年交易日数量
        self.price = 0.0 # 初始价格
        self.sigma = 0.0 # 波动率
        self.risk_free_rate = 0.0 # 无风险利率
        self.basis_rate = 0.0 # 股息率或贴水率

    def ToJson(self):
        return json.dumps(self.__dict__)

def Test_Stochastic_Model_GBM():
    config = Config_GBM()
    config.rand_rows = 10000 # 随机数据行数
    config.rand_cols = 250 # 随机数据列数
    config.dimension = 0 # 随机数据维度 # 未使用
    config.rand_seed = [0, 1, 2, 3, 4, 5, 6, 7] # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
    config.runs_size = 10000 # 模拟路径数量 # 目前是以 rand_rows 为准
    config.runs_step = 250 # 价格变动步数 # 目前需与 rand_cols 一致
    config.year_days = 244 # 年交易日数量
    config.price = 1.0 # 初始价格
    config.sigma = 0.24 # 波动率
    config.risk_free_rate = 0.03 # 无风险利率
    config.basis_rate = 0.0 # 股息率或贴水率
    
    kernel = cyberx.GetKernel()
    
    tasker_test = tasker.Tasker()
    tasker_test.plugin_id = "derivx_stochastic_model"
    tasker_test.timeout_wait = 3600 # 秒
    tasker_test.distribute_type = 0 # 本地计算任务
    tasker_test.common_args = config.ToJson()
    
    tasker_test.method_id = func_make_data_gbm
    
    result = kernel.AssignTask(tasker_test.ToArgs()) # 同步
    if result["return_code"] != 0:
        print(result["return_code"], result["return_info"])
    else:
        result = json.loads(result["result_data"])
        ShowPlot_Frequency(np.array(result), "Final-Price-Frequency", "Final-Price")
        ShowPlot_Distribution(np.array(result), 1000, config.runs_step, "Price - Steps", "Price")

def Test_Stochastic_Model_CGBM():
    config = Config_CGBM()
    config.rand_rows = 5 # 随机数据行数
    config.rand_cols = 750 # 随机数据列数
    config.dimension = 0 # 随机数据维度 # 未使用
    config.rand_seed = [0, 1, 2, 3, 4] # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
    config.runs_size = 5 # 模拟路径数量 # 目前是以 rand_rows 为准
    config.runs_step = 750 # 价格变动步数 # 目前需与 rand_cols 一致
    config.year_days = 244 # 年交易日数量
    config.asset = 3 # 标的数量
    config.corco = [[ 1.000,  0.000, -0.999],
                    [ 0.000,  1.000,  0.000],
                    [-0.999,  0.000,  1.000]] # 相关系数矩阵
    config.price = [1.0, 1.5, 2.0] # 初始价格
    config.sigma = [0.10, 0.15, 0.20] # 波动率
    config.risk_free_rate = [0.03, 0.03, 0.03] # 无风险利率
    config.basis_rate = [0.0, 0.0, 0.0] # 股息率或贴水率
    
    kernel = cyberx.GetKernel()
    
    tasker_test = tasker.Tasker()
    tasker_test.plugin_id = "derivx_stochastic_model"
    tasker_test.timeout_wait = 3600 # 秒
    tasker_test.distribute_type = 0 # 本地计算任务
    tasker_test.common_args = config.ToJson()
    
    tasker_test.method_id = func_make_data_cgbm
    
    result = kernel.AssignTask(tasker_test.ToArgs()) # 同步
    if result["return_code"] != 0:
        print(result["return_code"], result["return_info"])
    else:
        result = json.loads(result["result_data"])
        for i in range(config.rand_rows):
            result_show = np.array(result)[i * config.asset : (i + 1) * config.asset, :]
            print(np.std(result_show[:, : -1] / result_show[:, 1 :], axis = 1) * np.sqrt(config.year_days)) # 校验 rise_fall 波动率是否与输入波动率一致
            print(np.corrcoef(result_show[:, : -1] / result_show[:, 1 :])) # 校验 rise_fall 相关性是否与输入相关性一致
            #ShowPlot_Frequency(result_show, "Final-Price-Frequency", "Final-Price")
            ShowPlot_Distribution(result_show, config.asset, config.runs_step, "Price - Steps", "Price")

def Test_Stochastic_Model_GBB():
    config = Config_GBB()
    config.rand_rows = 10000 # 随机数据行数
    config.rand_cols = 250 # 随机数据列数
    config.dimension = 0 # 随机数据维度 # 未使用
    config.rand_seed = [0, 1, 2, 3, 4, 5, 6, 7] # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
    config.runs_size = 10000 # 模拟路径数量 # 目前是以 rand_rows 为准
    config.runs_step = 250 # 价格变动步数 # 目前需与 rand_cols 一致
    config.year_days = 244 # 年交易日数量
    config.price = 1.0 # 初始价格
    config.sigma = 0.24 # 波动率
    config.risk_free_rate = 0.03 # 无风险利率
    config.basis_rate = 0.0 # 股息率或贴水率
    
    kernel = cyberx.GetKernel()
    
    tasker_test = tasker.Tasker()
    tasker_test.plugin_id = "derivx_stochastic_model"
    tasker_test.timeout_wait = 3600 # 秒
    tasker_test.distribute_type = 0 # 本地计算任务
    tasker_test.common_args = config.ToJson()
    
    tasker_test.method_id = func_make_data_gbb
    
    result = kernel.AssignTask(tasker_test.ToArgs()) # 同步
    if result["return_code"] != 0:
        print(result["return_code"], result["return_info"])
    else:
        result = json.loads(result["result_data"])
        ShowPlot_Frequency(np.array(result), "Final-Price-Frequency", "Final-Price")
        ShowPlot_Distribution(np.array(result), 1000, config.runs_step, "Price - Steps", "Price")

def Test_Stochastic_Model_CIR():
    config = Config_CIR()
    config.rand_rows = 10000 # 随机数据行数
    config.rand_cols = 250 # 随机数据列数
    config.dimension = 0 # 随机数据维度 # 未使用
    config.rand_seed = [0, 1, 2, 3, 4, 5, 6, 7] # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
    config.runs_size = 10000 # 模拟路径数量 # 目前是以 rand_rows 为准
    config.runs_step = 250 # 价格变动步数 # 目前需与 rand_cols 一致
    config.year_days = 244 # 年交易日数量
    config.price = 0.05 # 初始价格
    config.sigma = 0.1 # 波动率
    config.kappa = 3.0 # 均值回归系数
    config.theta = 0.02 # 长期均值项
    
    kernel = cyberx.GetKernel()
    
    tasker_test = tasker.Tasker()
    tasker_test.plugin_id = "derivx_stochastic_model"
    tasker_test.timeout_wait = 3600 # 秒
    tasker_test.distribute_type = 0 # 本地计算任务
    tasker_test.common_args = config.ToJson()
    
    tasker_test.method_id = func_make_data_cir
    
    result = kernel.AssignTask(tasker_test.ToArgs()) # 同步
    if result["return_code"] != 0:
        print(result["return_code"], result["return_info"])
    else:
        result = json.loads(result["result_data"])
        ShowPlot_Frequency(np.array(result), "Final-Price-Frequency", "Final-Price")
        ShowPlot_Distribution(np.array(result), 1000, config.runs_step, "Price - Steps", "Price")

def Test_Stochastic_Model_JDP():
    config = Config_JDP()
    config.rand_rows = 10000 # 随机数据行数
    config.rand_cols = 250 # 随机数据列数
    config.dimension = 0 # 随机数据维度 # 未使用
    config.rand_seed = [0, 1, 2, 3, 4, 5, 6, 7] # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
    config.runs_size = 10000 # 模拟路径数量 # 目前是以 rand_rows 为准
    config.runs_step = 250 # 价格变动步数 # 目前需与 rand_cols 一致
    config.year_days = 244 # 年交易日数量
    config.price = 1.0 # 初始价格
    config.sigma = 0.2 # 波动率
    config.risk_free_rate = 0.05 # 无风险利率
    config.mu = -0.6 # 预期跳跃均值，正负决定跳跃方向
    config.lamb = 0.75 # 跳跃强度
    config.delta = 0.25 # 跳跃强度标准差
    
    kernel = cyberx.GetKernel()
    
    tasker_test = tasker.Tasker()
    tasker_test.plugin_id = "derivx_stochastic_model"
    tasker_test.timeout_wait = 3600 # 秒
    tasker_test.distribute_type = 0 # 本地计算任务
    tasker_test.common_args = config.ToJson()
    
    tasker_test.method_id = func_make_data_jdp
    
    result = kernel.AssignTask(tasker_test.ToArgs()) # 同步
    if result["return_code"] != 0:
        print(result["return_code"], result["return_info"])
    else:
        result = json.loads(result["result_data"])
        ShowPlot_Frequency(np.array(result), "Final-Price-Frequency", "Final-Price")
        ShowPlot_Distribution(np.array(result), 1000, config.runs_step, "Price - Steps", "Price")

def Test_Stochastic_Model_HEST():
    config = Config_HEST()
    config.rand_rows = 10000 # 随机数据行数
    config.rand_cols = 250 # 随机数据列数
    config.dimension = 0 # 随机数据维度 # 未使用
    config.rand_seed = [0, 1, 2, 3, 4, 5, 6, 7] # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
    config.runs_size = 10000 # 模拟路径数量 # 目前是以 rand_rows 为准
    config.runs_step = 250 # 价格变动步数 # 目前需与 rand_cols 一致
    config.year_days = 244 # 年交易日数量
    config.price = 1.0 # 初始价格
    config.sigma = 0.1 # 初始波动率
    config.risk_free_rate = 0.03 # 无风险利率
    config.kappa = 3.0 # 波动率均值回归系数
    config.theta = 0.25 # 波动率长期均值项
    config.sigma_sigma = 0.1 # 波动率的波动率
    config.rho = 0.6 # 两个随机过程的相关系数
    
    kernel = cyberx.GetKernel()
    
    tasker_test = tasker.Tasker()
    tasker_test.plugin_id = "derivx_stochastic_model"
    tasker_test.timeout_wait = 3600 # 秒
    tasker_test.distribute_type = 0 # 本地计算任务
    tasker_test.common_args = config.ToJson()
    
    tasker_test.method_id = func_make_data_hest
    
    result = kernel.AssignTask(tasker_test.ToArgs()) # 同步
    if result["return_code"] != 0:
        print(result["return_code"], result["return_info"])
    else:
        result = json.loads(result["result_data"])
        ShowPlot_Frequency(np.array(result), "Final-Price-Frequency", "Final-Price")
        ShowPlot_Distribution(np.array(result), 1000, config.runs_step, "Price - Steps", "Price")

def Test_Stochastic_Model_SABR():
    config = Config_SABR()
    config.rand_rows = 10000 # 随机数据行数
    config.rand_cols = 250 # 随机数据列数
    config.dimension = 0 # 随机数据维度 # 未使用
    config.rand_seed = [0, 1, 2, 3, 4, 5, 6, 7] # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
    config.runs_size = 10000 # 模拟路径数量 # 目前是以 rand_rows 为准
    config.runs_step = 250 # 价格变动步数 # 目前需与 rand_cols 一致
    config.year_days = 244 # 年交易日数量
    config.price = 0.06 # 初始价格
    config.sigma = 0.2 # 初始波动率
    config.beta = 0.5 # 价格分布力度
    config.sigma_sigma = 0.2 # 波动率的波动率
    config.rho = 0.6 # 两个随机过程的相关系数
    
    kernel = cyberx.GetKernel()
    
    tasker_test = tasker.Tasker()
    tasker_test.plugin_id = "derivx_stochastic_model"
    tasker_test.timeout_wait = 3600 # 秒
    tasker_test.distribute_type = 0 # 本地计算任务
    tasker_test.common_args = config.ToJson()
    
    tasker_test.method_id = func_make_data_sabr
    
    result = kernel.AssignTask(tasker_test.ToArgs()) # 同步
    if result["return_code"] != 0:
        print(result["return_code"], result["return_info"])
    else:
        result = json.loads(result["result_data"])
        ShowPlot_Frequency(np.array(result), "Final-Price-Frequency", "Final-Price")
        ShowPlot_Distribution(np.array(result), 1000, config.runs_step, "Price - Steps", "Price")

# USER：仅用于随机过程数据测试
def Test_Stochastic_Model_USER():
    config = Config_USER()
    config.rand_rows = 10000 # 随机数据行数
    config.rand_cols = 250 # 随机数据列数
    config.dimension = 624 # 随机数据维度
    config.rand_seed = [0, 1, 2, 3, 4, 5, 6, 7] # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
    config.runs_size = 10000 # 模拟路径数量 # 目前是以 rand_rows 为准
    config.runs_step = 250 # 价格变动步数 # 目前需与 rand_cols 一致
    config.year_days = 244 # 年交易日数量
    config.price = 1.0 # 初始价格
    config.sigma = 0.24 # 波动率
    config.risk_free_rate = 0.03 # 无风险利率
    config.basis_rate = 0.0 # 股息率或贴水率
    
    kernel = cyberx.GetKernel()
    
    tasker_test = tasker.Tasker()
    tasker_test.plugin_id = "derivx_stochastic_model"
    tasker_test.timeout_wait = 3600 # 秒
    tasker_test.distribute_type = 0 # 本地计算任务
    tasker_test.common_args = config.ToJson()
    
    tasker_test.method_id = func_make_data_user
    
    result = kernel.AssignTask(tasker_test.ToArgs()) # 同步
    if result["return_code"] != 0:
        print(result["return_code"], result["return_info"])
    else:
        result = json.loads(result["result_data"])
        ShowPlot_Frequency(np.array(result), "Final-Price-Frequency", "Final-Price")
        ShowPlot_Distribution(np.array(result), 1000, config.runs_step, "Price - Steps", "Price")

if __name__ == "__main__":
    kernel = cyberx.Kernel(syscfg.SysCfg().ToArgs()) # 全局唯一
    Test_Stochastic_Model_GBM()
    #Test_Stochastic_Model_CGBM()
    #Test_Stochastic_Model_GBB()
    #Test_Stochastic_Model_CIR()
    #Test_Stochastic_Model_JDP()
    #Test_Stochastic_Model_HEST()
    #Test_Stochastic_Model_SABR()
    #Test_Stochastic_Model_USER()
    del kernel # 主动析构
