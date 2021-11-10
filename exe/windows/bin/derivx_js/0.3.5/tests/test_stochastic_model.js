/*
* Copyright (c) 2021-2021 the DerivX authors
* All rights reserved.
*
* The project sponsor and lead author is Xu Rendong.
* E-mail: xrd@ustc.edu, QQ: 277195007, WeChat: xrd_ustc
* See the contributors file for names of other contributors.
*
* Commercial use of this code in source and binary forms is
* governed by a LGPL v3 license. You may get a copy from the
* root directory. Or else you should get a specific written
* permission from the project author.
*
* Individual and educational use of this code in source and
* binary forms is governed by a 3-clause BSD license. You may
* get a copy from the root directory. Certainly welcome you
* to contribute code of all sorts.
*
* Be sure to retain the above copyright notice and conditions.
*/

'use strict'

const nj = require('numjs')

const derivx = require('derivx')

// GBM：几何布朗运动 (指数布朗运动) Geometric Brownian Motion
// CIR：CIR 模型 (平方根扩散过程) Cox–Ingersoll–Ross model (Square-Root Diffusion)
// JDP：跳跃扩散过程 Jump Diffusion Process
// HEST：Heston 模型 Heston Model
// SABR：SABR 模型 Stochastic Alpha Beta Rho

class Config_GBM {
    constructor() {
        this.rand_rows = 0 // 随机数据行数
        this.rand_cols = 0 // 随机数据列数
        this.rand_seed = [] // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
        this.runs_size = 0 // 模拟路径数量
        this.runs_step = 0 // 价格变动步数
        this.year_days = 0 // 年交易日数量
        this.price = 0.0 // 初始价格
        this.sigma = 0.0 // 波动率
        this.risk_free_rate = 0.0 // 无风险利率
        this.basis_rate = 0.0 // 股息率或贴水率
    }
}

class Config_CIR {
    constructor() {
        this.rand_rows = 0 // 随机数据行数
        this.rand_cols = 0 // 随机数据列数
        this.rand_seed = [] // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
        this.runs_size = 0 // 模拟路径数量
        this.runs_step = 0 // 价格变动步数
        this.year_days = 0 // 年交易日数量
        this.price = 0.0 // 初始价格
        this.sigma = 0.0 // 波动率
        this.kappa = 0.0 // 均值回归系数
        this.theta = 0.0 // 长期均值项
    }
}

class Config_JDP {
    constructor() {
        this.rand_rows = 0 // 随机数据行数
        this.rand_cols = 0 // 随机数据列数
        this.rand_seed = [] // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
        this.runs_size = 0 // 模拟路径数量
        this.runs_step = 0 // 价格变动步数
        this.year_days = 0 // 年交易日数量
        this.price = 0.0 // 初始价格
        this.sigma = 0.0 // 波动率
        this.risk_free_rate = 0.0 // 无风险利率
        this.mu = 0.0 // 预期跳跃均值，正负决定跳跃方向
        this.lamb = 0.0 // 跳跃强度
        this.delta = 0.0 // 跳跃强度标准差
    }
}

class Config_HEST {
    constructor() {
        this.rand_rows = 0 // 随机数据行数
        this.rand_cols = 0 // 随机数据列数
        this.rand_seed = [] // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
        this.runs_size = 0 // 模拟路径数量
        this.runs_step = 0 // 价格变动步数
        this.year_days = 0 // 年交易日数量
        this.price = 0.0 // 初始价格
        this.sigma = 0.0 // 初始波动率
        this.risk_free_rate = 0.0 // 无风险利率
        this.kappa = 0.0 // 波动率均值回归系数
        this.theta = 0.0 // 波动率长期均值项
        this.sigma_sigma = 0.0 // 波动率的波动率
        this.rho = 0.0 // 两个随机过程的相关系数
    }
}

class Config_SABR {
    constructor() {
        this.rand_rows = 0 // 随机数据行数
        this.rand_cols = 0 // 随机数据列数
        this.rand_seed = [] // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
        this.runs_size = 0 // 模拟路径数量
        this.runs_step = 0 // 价格变动步数
        this.year_days = 0 // 年交易日数量
        this.price = 0.0 // 初始价格
        this.sigma = 0.0 // 初始波动率
        this.beta = 0.0 // 价格分布力度
        this.sigma_sigma = 0.0 // 波动率的波动率
        this.rho = 0.0 // 两个随机过程的相关系数
    }
}

function Test_Stochastic_Model_GBM() {
    let stochastic = new derivx.Stochastic("GBM")
    
    let config = new Config_GBM()
    config.rand_rows = 10000 // 随机数据行数
    config.rand_cols = 250 // 随机数据列数
    config.rand_seed = nj.array([0, 1, 2, 3, 4, 5, 6, 7]).tolist() // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
    config.runs_size = 10000 // 模拟路径数量
    config.runs_step = 250 // 价格变动步数
    config.year_days = 244 // 年交易日数量
    config.price = 1.0 // 初始价格
    config.sigma = 0.24 // 波动率
    config.risk_free_rate = 0.03 // 无风险利率
    config.basis_rate = 0.0 // 股息率或贴水率
    
    if(stochastic.InitArgs(config) < 0) {
        console.log(stochastic.GetError())
        return
    }
    
    let result = nj.zeros([config.runs_size, config.runs_step]).tolist()
    if(stochastic.MakeData(result) < 0) {
        console.log(stochastic.GetError())
        return
    }
    //console.log("result:", result)
}

function Test_Stochastic_Model_CIR() {
    let stochastic = new derivx.Stochastic("CIR")
    
    let config = new Config_CIR()
    config.rand_rows = 10000 // 随机数据行数
    config.rand_cols = 250 // 随机数据列数
    config.rand_seed = nj.array([0, 1, 2, 3, 4, 5, 6, 7]).tolist() // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
    config.runs_size = 10000 // 模拟路径数量
    config.runs_step = 250 // 价格变动步数
    config.year_days = 244 // 年交易日数量
    config.price = 0.05 // 初始价格
    config.sigma = 0.1 // 波动率
    config.kappa = 3.0 // 均值回归系数
    config.theta = 0.02 // 长期均值项
    
    if(stochastic.InitArgs(config) < 0) {
        console.log(stochastic.GetError())
        return
    }
    
    let result = nj.zeros([config.runs_size, config.runs_step]).tolist()
    if(stochastic.MakeData(result) < 0) {
        console.log(stochastic.GetError())
        return
    }
    //console.log("result:", result)
}

function Test_Stochastic_Model_JDP() {
    let stochastic = new derivx.Stochastic("JDP")
    
    let config = new Config_JDP()
    config.rand_rows = 10000 // 随机数据行数
    config.rand_cols = 250 // 随机数据列数
    config.rand_seed = nj.array([0, 1, 2, 3, 4, 5, 6, 7]).tolist() // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
    config.runs_size = 10000 // 模拟路径数量
    config.runs_step = 250 // 价格变动步数
    config.year_days = 244 // 年交易日数量
    config.price = 1.0 // 初始价格
    config.sigma = 0.2 // 波动率
    config.risk_free_rate = 0.05 // 无风险利率
    config.mu = -0.6 // 预期跳跃均值，正负决定跳跃方向
    config.lamb = 0.75 // 跳跃强度
    config.delta = 0.25 // 跳跃强度标准差
    
    if(stochastic.InitArgs(config) < 0) {
        console.log(stochastic.GetError())
        return
    }
    
    let result = nj.zeros([config.runs_size, config.runs_step]).tolist()
    if(stochastic.MakeData(result) < 0) {
        console.log(stochastic.GetError())
        return
    }
    //console.log("result:", result)
}

function Test_Stochastic_Model_HEST() {
    let stochastic = new derivx.Stochastic("HEST")
    
    let config = new Config_HEST()
    config.rand_rows = 10000 // 随机数据行数
    config.rand_cols = 250 // 随机数据列数
    config.rand_seed = nj.array([0, 1, 2, 3, 4, 5, 6, 7]).tolist() // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
    config.runs_size = 10000 // 模拟路径数量
    config.runs_step = 250 // 价格变动步数
    config.year_days = 244 // 年交易日数量
    config.price = 1.0 // 初始价格
    config.sigma = 0.1 // 初始波动率
    config.risk_free_rate = 0.03 // 无风险利率
    config.kappa = 3.0 // 波动率均值回归系数
    config.theta = 0.25 // 波动率长期均值项
    config.sigma_sigma = 0.1 // 波动率的波动率
    config.rho = 0.6 // 两个随机过程的相关系数
    
    if(stochastic.InitArgs(config) < 0) {
        console.log(stochastic.GetError())
        return
    }
    
    let result = nj.zeros([config.runs_size, config.runs_step]).tolist()
    if(stochastic.MakeData(result) < 0) {
        console.log(stochastic.GetError())
        return
    }
    //console.log("result:", result)
}

function Test_Stochastic_Model_SABR() {
    let stochastic = new derivx.Stochastic("SABR")
    
    let config = new Config_SABR()
    config.rand_rows = 10000 // 随机数据行数
    config.rand_cols = 250 // 随机数据列数
    config.rand_seed = nj.array([0, 1, 2, 3, 4, 5, 6, 7]).tolist() // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
    config.runs_size = 10000 // 模拟路径数量
    config.runs_step = 250 // 价格变动步数
    config.year_days = 244 // 年交易日数量
    config.price = 0.06 // 初始价格
    config.sigma = 0.2 // 初始波动率
    config.beta = 0.5 // 价格分布力度
    config.sigma_sigma = 0.2 // 波动率的波动率
    config.rho = 0.6 // 两个随机过程的相关系数
    
    if(stochastic.InitArgs(config) < 0) {
        console.log(stochastic.GetError())
        return
    }
    
    let result = nj.zeros([config.runs_size, config.runs_step]).tolist()
    if(stochastic.MakeData(result) < 0) {
        console.log(stochastic.GetError())
        return
    }
    //console.log("result:", result)
}

Test_Stochastic_Model_GBM()
Test_Stochastic_Model_CIR()
Test_Stochastic_Model_JDP()
Test_Stochastic_Model_HEST()
Test_Stochastic_Model_SABR()
