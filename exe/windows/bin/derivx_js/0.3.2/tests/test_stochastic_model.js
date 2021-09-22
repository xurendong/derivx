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
// SVM：Heston 模型 (随机波动率模型) Heston Model (Stochastic Volatility Model)
// SABR：SABR 模型 Stochastic Alpha Beta Rho

class Config_GBM {
    constructor() {
        this.rand_rows = 0 // 随机数据行数
        this.rand_cols = 0 // 随机数据列数
        this.rand_seed = [] // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
        
        this.dual_smooth = true // 对偶平滑路径
        this.runs_size = 0 // 模拟路径数量
        this.runs_step = 0 // 价格变动步数
        this.year_days = 0 // 年交易日数量
        
        this.v = 0.0 // 波动率
        this.r = 0.0 // 无风险利率
        this.q = 0.0 // 股息或贴水
    }
}

class Config_CIR {
    constructor() {
        this.rand_rows = 0 // 随机数据行数
        this.rand_cols = 0 // 随机数据列数
        this.rand_seed = [] // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
        
        this.dual_smooth = true // 对偶平滑路径
        this.runs_size = 0 // 模拟路径数量
        this.runs_step = 0 // 价格变动步数
        this.year_days = 0 // 年交易日数量
    }
}

class Config_JDP {
    constructor() {
        this.rand_rows = 0 // 随机数据行数
        this.rand_cols = 0 // 随机数据列数
        this.rand_seed = [] // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
        
        this.dual_smooth = true // 对偶平滑路径
        this.runs_size = 0 // 模拟路径数量
        this.runs_step = 0 // 价格变动步数
        this.year_days = 0 // 年交易日数量
    }
}

class Config_SVM {
    constructor() {
        this.rand_rows = 0 // 随机数据行数
        this.rand_cols = 0 // 随机数据列数
        this.rand_seed = [] // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
        
        this.dual_smooth = true // 对偶平滑路径
        this.runs_size = 0 // 模拟路径数量
        this.runs_step = 0 // 价格变动步数
        this.year_days = 0 // 年交易日数量
    }
}

class Config_SABR {
    constructor() {
        this.rand_rows = 0 // 随机数据行数
        this.rand_cols = 0 // 随机数据列数
        this.rand_seed = [] // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
        
        this.dual_smooth = true // 对偶平滑路径
        this.runs_size = 0 // 模拟路径数量
        this.runs_step = 0 // 价格变动步数
        this.year_days = 0 // 年交易日数量
    }
}

function Test_Stochastic_Model() {
    let stochastic = null, config = null
    
    stochastic = new derivx.Stochastic("GBM")
    
    config = new Config_GBM()
    config.rand_rows = 5000 // 随机数据行数
    config.rand_cols = 250 // 随机数据列数
    config.rand_seed = nj.array([0, 1, 2, 3, 4, 5, 6, 7]).tolist() // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
    config.dual_smooth = true // 对偶平滑路径
    config.runs_size = 10000 // 模拟路径数量
    config.runs_step = 244 // 价格变动步数
    config.year_days = 244 // 年交易日数量
    config.v = 0.24 // 波动率
    config.r = 0.03 // 无风险利率
    config.q = 0.0 // 股息或贴水
    
    if(stochastic.InitArgs(config) < 0) {
        console.log(stochastic.GetError())
        return
    }
    
    let result = nj.zeros([config.runs_size, config.runs_step + 1]).tolist()
    if(stochastic.MakeData(result) < 0) {
        console.log(stochastic.GetError())
        return
    }
    //console.log("result:", result)
    
    //////////////////////////////////////////////////
    
    stochastic = new derivx.Stochastic("CIR")
    
    config = new Config_CIR()
    config.rand_rows = 5000 // 随机数据行数
    config.rand_cols = 250 // 随机数据列数
    config.rand_seed = nj.array([0, 1, 2, 3, 4, 5, 6, 7]).tolist() // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
    config.dual_smooth = true // 对偶平滑路径
    config.runs_size = 10000 // 模拟路径数量
    config.runs_step = 244 // 价格变动步数
    config.year_days = 244 // 年交易日数量
    
    if(stochastic.InitArgs(config) < 0) {
        console.log(stochastic.GetError())
        return
    }
    
    //////////////////////////////////////////////////
    
    stochastic = new derivx.Stochastic("JDP")
    
    config = new Config_JDP()
    config.rand_rows = 5000 // 随机数据行数
    config.rand_cols = 250 // 随机数据列数
    config.rand_seed = nj.array([0, 1, 2, 3, 4, 5, 6, 7]).tolist() // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
    config.dual_smooth = true // 对偶平滑路径
    config.runs_size = 10000 // 模拟路径数量
    config.runs_step = 244 // 价格变动步数
    config.year_days = 244 // 年交易日数量
    
    if(stochastic.InitArgs(config) < 0) {
        console.log(stochastic.GetError())
        return
    }
    
    //////////////////////////////////////////////////
    
    stochastic = new derivx.Stochastic("SVM")
    
    config = new Config_SVM()
    config.rand_rows = 5000 // 随机数据行数
    config.rand_cols = 250 // 随机数据列数
    config.rand_seed = nj.array([0, 1, 2, 3, 4, 5, 6, 7]).tolist() // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
    config.dual_smooth = true // 对偶平滑路径
    config.runs_size = 10000 // 模拟路径数量
    config.runs_step = 244 // 价格变动步数
    config.year_days = 244 // 年交易日数量
    
    if(stochastic.InitArgs(config) < 0) {
        console.log(stochastic.GetError())
        return
    }
    
    //////////////////////////////////////////////////
    
    stochastic = new derivx.Stochastic("SABR")
    
    config = new Config_SABR()
    config.rand_rows = 5000 // 随机数据行数
    config.rand_cols = 250 // 随机数据列数
    config.rand_seed = nj.array([0, 1, 2, 3, 4, 5, 6, 7]).tolist() // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
    config.dual_smooth = true // 对偶平滑路径
    config.runs_size = 10000 // 模拟路径数量
    config.runs_step = 244 // 价格变动步数
    config.year_days = 244 // 年交易日数量
    
    if(stochastic.InitArgs(config) < 0) {
        console.log(stochastic.GetError())
        return
    }
}

Test_Stochastic_Model()
