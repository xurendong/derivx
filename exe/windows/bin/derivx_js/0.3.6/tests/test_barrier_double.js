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

let g_uoc_dop = 1 // 向上敲出看涨，向下敲出看跌，双鲨

class Config {
    constructor() {
        this.rand_rows = 0 // 随机数据行数 // InitRand
        this.rand_cols = 0 // 随机数据列数 // InitRand
        this.rand_quasi = false // 随机数据类型 // InitRand // 目前 quasi 随机数据只能使用单核处理
        this.rand_seed = [] // 随机数据种子 // InitRand // 非负整数，有效位数不超逻辑处理器数量，目前 quasi 仅第一位有效
        
        this.dual_smooth = true // 对偶平滑路径 // InitPath
        this.runs_size = 0 // 模拟路径数量 // InitPath
        this.runs_step = 0 // 价格变动步数 // InitPath
        this.year_days = 0 // 年交易日数量 // InitPath
        this.sigma = 0.0 // 波动率 // InitPath
        this.risk_free_rate = 0.0 // 无风险利率 // InitPath
        this.basis_rate = 0.0 // 股息或贴水 // InitPath
        this.price_limit_ratio = 0.0 // 涨跌停限制幅度 // InitPath
        this.price_limit_style = 0 // 涨跌停限制方式，0 不限制，1 超限部分移至下日，2 超限部分直接削掉 // InitPath
        
        this.s = 0.0 // 标的价格
        this.h_l = 0.0 // 障碍价格，低
        this.h_h = 0.0 // 障碍价格，高
        this.k_l = 0.0 // 行权价格，低
        this.k_h = 0.0 // 行权价格，高
        this.x = 0.0 // 敲出后需支付的资金
        this.v = 0.0 // 波动率 // 双鲨未用
        this.r = 0.0 // 无风险利率 // 双鲨未用
        this.q = 0.0 // 年化分红率 // 双鲨未用
        this.t = 0.0 // 年化到期期限 // 双鲨未用
        this.p = 0.0 // 参与率，未敲出情况下客户对收益的占比要求
        this.is_kop_delay = false // 敲出后是立即还是延期支付资金
        this.barrier_type = 0 // 障碍类型
        this.trade_long = true // 交易方向
        this.price_rate = 0.0 // 价格比率
        
        this.calc_price = [] // 计算价格序列
        this.run_from = 0 // 起始天数，第一天为零
        this.run_days = 0 // 运行天数
    }
}

function Test_Barrier_Double() {
    let config = new Config()
    config.rand_rows = 50000 // 随机数据行数 // InitRand
    config.rand_cols = 250 // 随机数据列数 // InitRand
    config.rand_quasi = false // 随机数据类型 // InitRand // 目前 quasi 随机数据只能使用单核处理
    config.rand_seed = nj.array([0, 1, 2, 3, 4, 5, 6, 7]).tolist() // 随机数据种子 // InitRand // 非负整数，有效位数不超逻辑处理器数量，目前 quasi 仅第一位有效
    
    config.dual_smooth = true // 对偶平滑路径 // InitPath
    config.runs_size = 100000 // 模拟路径数量 // InitPath
    config.runs_step = 244 // 价格变动步数 // InitPath
    config.year_days = 244 // 年交易日数量 // InitPath
    config.sigma = 0.16 // 波动率 // InitPath
    config.risk_free_rate = 0.03 // 无风险利率 // InitPath
    config.basis_rate = 0.06 // 股息或贴水 // InitPath
    config.price_limit_ratio = 0.1 // 涨跌停限制幅度 // InitPath
    config.price_limit_style = 0 // 涨跌停限制方式，0 不限制，1 超限部分移至下日，2 超限部分直接削掉 // InitPath
    
    config.s = 100.0 // 标的价格
    config.h_l = 95.0 // 障碍价格，低
    config.h_h = 105.0 // 障碍价格，高
    config.k_l = 99.0 // 行权价格，低
    config.k_h = 101.0 // 行权价格，高
    config.x = 3.5 // 敲出后需支付的资金
    // config.v = 0.16 // 波动率 // 双鲨未用
    // config.r = 0.03 // 无风险利率 // 双鲨未用
    // config.q = 0.06 // 年化分红率 // 双鲨未用
    // config.t = 1.0 // 年化到期期限 // 双鲨未用
    config.p = 1.0 // 参与率，未敲出情况下客户对收益的占比要求
    config.is_kop_delay = true // 敲出后是立即还是延期支付资金
    config.barrier_type = g_uoc_dop // 障碍类型
    config.trade_long = false // 交易方向
    config.price_rate = 0.035 // 价格比率
    
    let calc_price_u = 110.0 // 价格点上界
    let calc_price_d = 90.0 // 价格点下界
    let calc_price_g = 1.0 // 价格点间隔
    //config.calc_price = [65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0, 100.0, 105.0] // 计算价格序列
    config.calc_price = nj.arange(calc_price_d, calc_price_u + calc_price_g, calc_price_g).tolist() // 含价格点上下界
    
    config.run_from = 0 // 起始天数，第一天为零
    config.run_days = 1 // 运行天数
    
    let ret_cols = config.runs_step
    let ret_rows = config.calc_price.length
    
    let barrier = new derivx.Barrier("Double")
    
    if(barrier.InitArgs(config) < 0) {
        console.log(barrier.GetError())
        return
    }
    
    if(barrier.InitRand() < 0) {
        console.log(barrier.GetError())
        return
    }
    // 除非电脑性能较差，否则不推荐使用 SaveRand() 和 LoadRand() 了
    // 最好将影响随机数据的参数都包含在文件名中，避免导入的随机数据与所设参数不一致
    //let rand_file = util.format("./rand_data_%d_%d_%d.rand", config.rand_rows, config.rand_cols, config.rand_seed[0])
    //if(barrier.SaveRand(rand_file) < 0) {
    //    console.log(barrier.GetError())
    //    return
    //}
    //if(barrier.LoadRand(rand_file) < 0) {
    //    console.log(barrier.GetError())
    //    return
    //}
    
    if(barrier.InitPath() < 0) {
        console.log(barrier.GetError())
        return
    }
    // 除非电脑性能较差，否则不推荐使用 SavePath() 和 LoadPath() 了
    // 最好将影响路径数据的参数都包含在文件名中，避免导入的路径数据与所设参数不一致
    //let path_file = util.format("./path_data_%d_%d_%d_%d_%f_%f_%f_%f_%d.path", 
    //    config.dual_smooth, config.runs_size, config.runs_step, config.year_days, 
    //    config.sigma, config.risk_free_rate, config.basis_rate, config.price_limit_ratio, config.price_limit_style)
    //if(barrier.SavePath(path_file) < 0) {
    //    console.log(barrier.GetError())
    //    return
    //}
    //if(barrier.LoadPath(path_file) < 0) {
    //    console.log(barrier.GetError())
    //    return
    //}
    
    //console.log("price:", barrier.CalcPrice())
    //console.log("payoff:", barrier.CalcPayoff())
    
    let greek_flags = {"delta":"d"}
    //let greek_flags = {"delta":"d", "gamma":"g", "vega":"v", "theta":"t", "rho":"r"}
    for(let [name, flag] of Object.entries(greek_flags)) {
        let result = nj.zeros([ret_rows, ret_cols]).tolist()
        barrier.CalcGreeks(flag, result)
        console.log("result:", result)
    }
}

Test_Barrier_Double()
