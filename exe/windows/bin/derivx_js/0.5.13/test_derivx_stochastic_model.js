/*
* Copyright (c) 2021-2023 the DerivX authors
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

// 示例说明：
// 1、演示几种随机过程模型和价格路径生成；
// 2、演示模型参数设置；
// 3、演示使用 GetKernel 方法获取 kernel 实例；
// 4、演示 tasker 任务信息创建；
// 5、演示 同步模式 AssignTask 任务执行调用；

'use strict'

const nj = require('numjs')

const syscfg = require('./syscfg')
const tasker = require('./tasker')
const cyberx = require('cyberx') // cyberx-js

let func_make_data_gbm  = 1
let func_make_data_cgbm = 2
let func_make_data_gbb  = 3
let func_make_data_cir  = 4
let func_make_data_jdp  = 5
let func_make_data_hest = 6
let func_make_data_sabr = 7
let func_make_data_user = 8

// GBM：几何 (指数) 布朗运动 Geometric Brownian Motion
// CGBM：具有相关性的几何 (指数）布朗运动 Correlated Geometric Brownian Motion
// GBB：几何 (指数) 布朗桥 Geometric Brownian Bridge
// CIR：CIR 模型 (平方根扩散过程) Cox–Ingersoll–Ross model (Square-Root Diffusion)
// JDP：跳跃扩散过程 Jump Diffusion Process
// HEST：Heston 模型 Heston Model
// SABR：SABR 模型 Stochastic Alpha Beta Rho
// USER：仅用于随机过程数据测试

class Config_GBM {
    constructor() {
        this.rand_rows = 0 // 随机数据行数
        this.rand_cols = 0 // 随机数据列数
        this.dimension = 0 // 随机数据维度 // 未使用
        this.rand_seed = [] // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
        this.runs_size = 0 // 模拟路径数量
        this.runs_step = 0 // 价格变动步数
        this.year_days = 0 // 年交易日数量
        this.price = 0.0 // 初始价格
        this.sigma = 0.0 // 波动率
        this.risk_free_rate = 0.0 // 无风险利率
        this.basis_rate = 0.0 // 股息率或贴水率
    }
    
    ToJson() {
        return JSON.stringify(this)
    }
}

class Config_CGBM {
    constructor() {
        this.rand_rows = 0 // 随机数据行数
        this.rand_cols = 0 // 随机数据列数
        this.dimension = 0 // 随机数据维度 // 未使用
        this.rand_seed = [] // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
        this.runs_size = 0 // 模拟路径数量
        this.runs_step = 0 // 价格变动步数
        this.year_days = 0 // 年交易日数量
        this.asset = 0 // 标的数量
        this.corco = [] // 相关系数矩阵
        this.price = [] // 初始价格
        this.sigma = [] // 波动率
        this.risk_free_rate = [] // 无风险利率
        this.basis_rate = [] // 股息率或贴水率
    }
    
    ToJson() {
        return JSON.stringify(this)
    }
}

class Config_GBB {
    constructor() {
        this.rand_rows = 0 // 随机数据行数
        this.rand_cols = 0 // 随机数据列数
        this.dimension = 0 // 随机数据维度 // 未使用
        this.rand_seed = [] // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
        this.runs_size = 0 // 模拟路径数量
        this.runs_step = 0 // 价格变动步数
        this.year_days = 0 // 年交易日数量
        this.price = 0.0 // 初始价格
        this.sigma = 0.0 // 波动率
        this.risk_free_rate = 0.0 // 无风险利率
        this.basis_rate = 0.0 // 股息率或贴水率
    }
    
    ToJson() {
        return JSON.stringify(this)
    }
}

class Config_CIR {
    constructor() {
        this.rand_rows = 0 // 随机数据行数
        this.rand_cols = 0 // 随机数据列数
        this.dimension = 0 // 随机数据维度 // 未使用
        this.rand_seed = [] // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
        this.runs_size = 0 // 模拟路径数量
        this.runs_step = 0 // 价格变动步数
        this.year_days = 0 // 年交易日数量
        this.price = 0.0 // 初始价格
        this.sigma = 0.0 // 波动率
        this.kappa = 0.0 // 均值回归系数
        this.theta = 0.0 // 长期均值项
    }
    
    ToJson() {
        return JSON.stringify(this)
    }
}

class Config_JDP {
    constructor() {
        this.rand_rows = 0 // 随机数据行数
        this.rand_cols = 0 // 随机数据列数
        this.dimension = 0 // 随机数据维度 // 未使用
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
    
    ToJson() {
        return JSON.stringify(this)
    }
}

class Config_HEST {
    constructor() {
        this.rand_rows = 0 // 随机数据行数
        this.rand_cols = 0 // 随机数据列数
        this.dimension = 0 // 随机数据维度 // 未使用
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
    
    ToJson() {
        return JSON.stringify(this)
    }
}

class Config_SABR {
    constructor() {
        this.rand_rows = 0 // 随机数据行数
        this.rand_cols = 0 // 随机数据列数
        this.dimension = 0 // 随机数据维度 // 未使用
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
    
    ToJson() {
        return JSON.stringify(this)
    }
}

class Config_USER {
    constructor() {
        this.rand_rows = 0 // 随机数据行数
        this.rand_cols = 0 // 随机数据列数
        this.dimension = 0 // 随机数据维度
        this.rand_seed = [] // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
        this.runs_size = 0 // 模拟路径数量
        this.runs_step = 0 // 价格变动步数
        this.year_days = 0 // 年交易日数量
        this.price = 0.0 // 初始价格
        this.sigma = 0.0 // 波动率
        this.risk_free_rate = 0.0 // 无风险利率
        this.basis_rate = 0.0 // 股息率或贴水率
    }
    
    ToJson() {
        return JSON.stringify(this)
    }
}

function Test_Stochastic_Model_GBM() {
    let config = new Config_GBM()
    config.rand_rows = 10000 // 随机数据行数
    config.rand_cols = 250 // 随机数据列数
    config.dimension = 0 // 随机数据维度 // 未使用
    config.rand_seed = nj.array([0, 1, 2, 3, 4, 5, 6, 7]).tolist() // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
    config.runs_size = 10000 // 模拟路径数量 // 目前是以 rand_rows 为准
    config.runs_step = 250 // 价格变动步数 // 目前需与 rand_cols 一致
    config.year_days = 244 // 年交易日数量
    config.price = 1.0 // 初始价格
    config.sigma = 0.24 // 波动率
    config.risk_free_rate = 0.03 // 无风险利率
    config.basis_rate = 0.0 // 股息率或贴水率
    
    let kernel = cyberx.GetKernel()
    
    let tasker_test = new tasker.Tasker()
    tasker_test.plugin_id = 'derivx_stochastic_model'
    tasker_test.timeout_wait = 3600 // 秒
    tasker_test.distribute_type = 0 // 本地计算任务
    tasker_test.common_args = config.ToJson()
    
    tasker_test.method_id = func_make_data_gbm
    
    let result = kernel.AssignTask(tasker_test) // 同步
    if(result['return_code'] !== 0) {
        console.log(result['return_code'], result['return_info'])
    }
    else {
        result = JSON.parse(result['result_data'])
        console.log('result:', result)
    }
}

function Test_Stochastic_Model_CGBM() {
    let config = new Config_CGBM()
    config.rand_rows = 5 // 随机数据行数
    config.rand_cols = 750 // 随机数据列数
    config.dimension = 0 // 随机数据维度 // 未使用
    config.rand_seed = nj.array([0, 1, 2, 3, 4]).tolist() // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
    config.runs_size = 5 // 模拟路径数量 // 目前是以 rand_rows 为准
    config.runs_step = 750 // 价格变动步数 // 目前需与 rand_cols 一致
    config.year_days = 244 // 年交易日数量
    config.asset = 3 // 标的数量
    config.corco = [[ 1.000,  0.000, -0.999],
                    [ 0.000,  1.000,  0.000],
                    [-0.999,  0.000,  1.000]] // 相关系数矩阵
    config.price = [1.0, 1.5, 2.0] // 初始价格
    config.sigma = [0.10, 0.15, 0.20] // 波动率
    config.risk_free_rate = [0.03, 0.03, 0.03] // 无风险利率
    config.basis_rate = [0.0, 0.0, 0.0] // 股息率或贴水率
    
    let kernel = cyberx.GetKernel()
    
    let tasker_test = new tasker.Tasker()
    tasker_test.plugin_id = 'derivx_stochastic_model'
    tasker_test.timeout_wait = 3600 // 秒
    tasker_test.distribute_type = 0 // 本地计算任务
    tasker_test.common_args = config.ToJson()
    
    tasker_test.method_id = func_make_data_cgbm
    
    let result = kernel.AssignTask(tasker_test) // 同步
    if(result['return_code'] !== 0) {
        console.log(result['return_code'], result['return_info'])
    }
    else {
        result = JSON.parse(result['result_data'])
        console.log('result:', result)
    }
}

function Test_Stochastic_Model_GBB() {
    let config = new Config_GBB()
    config.rand_rows = 10000 // 随机数据行数
    config.rand_cols = 250 // 随机数据列数
    config.dimension = 0 // 随机数据维度 // 未使用
    config.rand_seed = nj.array([0, 1, 2, 3, 4, 5, 6, 7]).tolist() // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
    config.runs_size = 10000 // 模拟路径数量 // 目前是以 rand_rows 为准
    config.runs_step = 250 // 价格变动步数 // 目前需与 rand_cols 一致
    config.year_days = 244 // 年交易日数量
    config.price = 1.0 // 初始价格
    config.sigma = 0.24 // 波动率
    config.risk_free_rate = 0.03 // 无风险利率
    config.basis_rate = 0.0 // 股息率或贴水率
    
    let kernel = cyberx.GetKernel()
    
    let tasker_test = new tasker.Tasker()
    tasker_test.plugin_id = 'derivx_stochastic_model'
    tasker_test.timeout_wait = 3600 // 秒
    tasker_test.distribute_type = 0 // 本地计算任务
    tasker_test.common_args = config.ToJson()
    
    tasker_test.method_id = func_make_data_gbb
    
    let result = kernel.AssignTask(tasker_test) // 同步
    if(result['return_code'] !== 0) {
        console.log(result['return_code'], result['return_info'])
    }
    else {
        result = JSON.parse(result['result_data'])
        console.log('result:', result)
    }
}

function Test_Stochastic_Model_CIR() {
    let config = new Config_CIR()
    config.rand_rows = 10000 // 随机数据行数
    config.rand_cols = 250 // 随机数据列数
    config.dimension = 0 // 随机数据维度 // 未使用
    config.rand_seed = nj.array([0, 1, 2, 3, 4, 5, 6, 7]).tolist() // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
    config.runs_size = 10000 // 模拟路径数量 // 目前是以 rand_rows 为准
    config.runs_step = 250 // 价格变动步数 // 目前需与 rand_cols 一致
    config.year_days = 244 // 年交易日数量
    config.price = 0.05 // 初始价格
    config.sigma = 0.1 // 波动率
    config.kappa = 3.0 // 均值回归系数
    config.theta = 0.02 // 长期均值项
    
    let kernel = cyberx.GetKernel()
    
    let tasker_test = new tasker.Tasker()
    tasker_test.plugin_id = 'derivx_stochastic_model'
    tasker_test.timeout_wait = 3600 // 秒
    tasker_test.distribute_type = 0 // 本地计算任务
    tasker_test.common_args = config.ToJson()
    
    tasker_test.method_id = func_make_data_cir
    
    let result = kernel.AssignTask(tasker_test) // 同步
    if(result['return_code'] !== 0) {
        console.log(result['return_code'], result['return_info'])
    }
    else {
        result = JSON.parse(result['result_data'])
        console.log('result:', result)
    }
}

function Test_Stochastic_Model_JDP() {
    let config = new Config_JDP()
    config.rand_rows = 10000 // 随机数据行数
    config.rand_cols = 250 // 随机数据列数
    config.dimension = 0 // 随机数据维度 // 未使用
    config.rand_seed = nj.array([0, 1, 2, 3, 4, 5, 6, 7]).tolist() // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
    config.runs_size = 10000 // 模拟路径数量 // 目前是以 rand_rows 为准
    config.runs_step = 250 // 价格变动步数 // 目前需与 rand_cols 一致
    config.year_days = 244 // 年交易日数量
    config.price = 1.0 // 初始价格
    config.sigma = 0.2 // 波动率
    config.risk_free_rate = 0.05 // 无风险利率
    config.mu = -0.6 // 预期跳跃均值，正负决定跳跃方向
    config.lamb = 0.75 // 跳跃强度
    config.delta = 0.25 // 跳跃强度标准差
    
    let kernel = cyberx.GetKernel()
    
    let tasker_test = new tasker.Tasker()
    tasker_test.plugin_id = 'derivx_stochastic_model'
    tasker_test.timeout_wait = 3600 // 秒
    tasker_test.distribute_type = 0 // 本地计算任务
    tasker_test.common_args = config.ToJson()
    
    tasker_test.method_id = func_make_data_jdp
    
    let result = kernel.AssignTask(tasker_test) // 同步
    if(result['return_code'] !== 0) {
        console.log(result['return_code'], result['return_info'])
    }
    else {
        result = JSON.parse(result['result_data'])
        console.log('result:', result)
    }
}

function Test_Stochastic_Model_HEST() {
    let config = new Config_HEST()
    config.rand_rows = 10000 // 随机数据行数
    config.rand_cols = 250 // 随机数据列数
    config.dimension = 0 // 随机数据维度 // 未使用
    config.rand_seed = nj.array([0, 1, 2, 3, 4, 5, 6, 7]).tolist() // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
    config.runs_size = 10000 // 模拟路径数量 // 目前是以 rand_rows 为准
    config.runs_step = 250 // 价格变动步数 // 目前需与 rand_cols 一致
    config.year_days = 244 // 年交易日数量
    config.price = 1.0 // 初始价格
    config.sigma = 0.1 // 初始波动率
    config.risk_free_rate = 0.03 // 无风险利率
    config.kappa = 3.0 // 波动率均值回归系数
    config.theta = 0.25 // 波动率长期均值项
    config.sigma_sigma = 0.1 // 波动率的波动率
    config.rho = 0.6 // 两个随机过程的相关系数
    
    let kernel = cyberx.GetKernel()
    
    let tasker_test = new tasker.Tasker()
    tasker_test.plugin_id = 'derivx_stochastic_model'
    tasker_test.timeout_wait = 3600 // 秒
    tasker_test.distribute_type = 0 // 本地计算任务
    tasker_test.common_args = config.ToJson()
    
    tasker_test.method_id = func_make_data_hest
    
    let result = kernel.AssignTask(tasker_test) // 同步
    if(result['return_code'] !== 0) {
        console.log(result['return_code'], result['return_info'])
    }
    else {
        result = JSON.parse(result['result_data'])
        console.log('result:', result)
    }
}

function Test_Stochastic_Model_SABR() {
    let config = new Config_SABR()
    config.rand_rows = 10000 // 随机数据行数
    config.rand_cols = 250 // 随机数据列数
    config.dimension = 0 // 随机数据维度 // 未使用
    config.rand_seed = nj.array([0, 1, 2, 3, 4, 5, 6, 7]).tolist() // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
    config.runs_size = 10000 // 模拟路径数量 // 目前是以 rand_rows 为准
    config.runs_step = 250 // 价格变动步数 // 目前需与 rand_cols 一致
    config.year_days = 244 // 年交易日数量
    config.price = 0.06 // 初始价格
    config.sigma = 0.2 // 初始波动率
    config.beta = 0.5 // 价格分布力度
    config.sigma_sigma = 0.2 // 波动率的波动率
    config.rho = 0.6 // 两个随机过程的相关系数
    
    let kernel = cyberx.GetKernel()
    
    let tasker_test = new tasker.Tasker()
    tasker_test.plugin_id = 'derivx_stochastic_model'
    tasker_test.timeout_wait = 3600 // 秒
    tasker_test.distribute_type = 0 // 本地计算任务
    tasker_test.common_args = config.ToJson()
    
    tasker_test.method_id = func_make_data_sabr
    
    let result = kernel.AssignTask(tasker_test) // 同步
    if(result['return_code'] !== 0) {
        console.log(result['return_code'], result['return_info'])
    }
    else {
        result = JSON.parse(result['result_data'])
        console.log('result:', result)
    }
}

// USER：仅用于随机过程数据测试
function Test_Stochastic_Model_USER() {
    let config = new Config_USER()
    config.rand_rows = 10000 // 随机数据行数
    config.rand_cols = 250 // 随机数据列数
    config.dimension = 624 // 随机数据维度
    config.rand_seed = nj.array([0, 1, 2, 3, 4, 5, 6, 7]).tolist() // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
    config.runs_size = 10000 // 模拟路径数量 // 目前是以 rand_rows 为准
    config.runs_step = 250 // 价格变动步数 // 目前需与 rand_cols 一致
    config.year_days = 244 // 年交易日数量
    config.price = 1.0 // 初始价格
    config.sigma = 0.24 // 波动率
    config.risk_free_rate = 0.03 // 无风险利率
    config.basis_rate = 0.0 // 股息率或贴水率
    
    let kernel = cyberx.GetKernel()
    
    let tasker_test = new tasker.Tasker()
    tasker_test.plugin_id = 'derivx_stochastic_model'
    tasker_test.timeout_wait = 3600 // 秒
    tasker_test.distribute_type = 0 // 本地计算任务
    tasker_test.common_args = config.ToJson()
    
    tasker_test.method_id = func_make_data_user
    
    let result = kernel.AssignTask(tasker_test) // 同步
    if(result['return_code'] !== 0) {
        console.log(result['return_code'], result['return_info'])
    }
    else {
        result = JSON.parse(result['result_data'])
        console.log('result:', result)
    }
}

let kernel = new cyberx.Kernel(new syscfg.SysCfg()) // 全局唯一
Test_Stochastic_Model_GBM()
//Test_Stochastic_Model_CGBM()
//Test_Stochastic_Model_GBB()
//Test_Stochastic_Model_CIR()
//Test_Stochastic_Model_JDP()
//Test_Stochastic_Model_HEST()
//Test_Stochastic_Model_SABR()
//Test_Stochastic_Model_USER()
