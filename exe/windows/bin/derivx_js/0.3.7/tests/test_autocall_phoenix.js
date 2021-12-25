/*
* Copyright (c) 2021-2022 the DerivX authors
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
const util = require('util');

const derivx = require('derivx')

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
        
        this.notional = 0.0 // 名义本金
        this.trade_long = true // 交易方向
        this.start_price = 0.0 // 初始价格
        this.strike_price = 0.0 // 敲入后执行价格
        this.knock_o_ratio = 0.0 // 敲出比率，非百分比
        this.knock_i_ratio = 0.0 // 敲入比率，非百分比
        this.knock_o_steps = 0.0 // 敲出比例逐月递减率
        this.knock_i_occur = false // 是否已经发生敲入
        this.knock_i_margin_call = true // 是否敲入后可追加保证金，置为 False 则变成不追保凤凰
        this.coupon_rate = 0.0 // 客户单次票息，CalcCoupon 时此入参不参与计算
        this.margin_rate = 0.0 // 保证金比例
        this.margin_interest = 0.0 // 保证金利率
        this.calc_price = [] // 计算价格序列
        this.run_from = 0 // 起始天数，第一天为零
        this.run_days = 0 // 运行天数
        this.knock_o_days = [] // 敲出日期序列
        this.knock_o_rate = [] // 敲出比率序列
    }
}

function Test_Autocall_Phoenix() {
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
    config.basis_rate = 0.05 // 股息或贴水 // InitPath
    config.price_limit_ratio = 0.1 // 涨跌停限制幅度 // InitPath
    config.price_limit_style = 0 // 涨跌停限制方式，0 不限制，1 超限部分移至下日，2 超限部分直接削掉 // InitPath
    
    config.notional = 100000.0 // 名义本金
    config.trade_long = false // 交易方向
    config.start_price = 100.0 // 初始价格
    config.strike_price = 100.0 // 敲入后执行价格
    config.knock_o_ratio = 1.0 // 敲出比率，非百分比
    config.knock_i_ratio = 0.8 // 敲入比率，非百分比
    config.knock_o_steps = 0.0 // 敲出比例逐月递减率
    config.knock_i_occur = false // 是否已经发生敲入
    config.knock_i_margin_call = true // 是否敲入后可追加保证金，置为 False 则变成不追保凤凰
    config.coupon_rate = 0.013 // 客户单次票息，CalcCoupon 时此入参不参与计算
    config.margin_rate = 1.0 // 保证金比例
    config.margin_interest = 0.03 // 保证金利率
    
    //config.knock_o_days = [61, 81, 101, 122, 142, 162, 183, 203, 223, 244, 264, 284, 305, 325, 345, 366, 386, 406, 427, 447, 467, 488] // 敲出日期序列
    config.knock_o_days = nj.array([20, 40, 61, 81, 101, 122, 142, 162, 183, 203, 223, 244]).tolist() // 敲出日期序列
    
    //config.knock_o_rate = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0] // 敲出比率序列
    //config.knock_o_rate = config.knock_o_rate.map((rate, index) => { return rate * config.knock_o_ratio })
    config.knock_o_rate = nj.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]) // 敲出比率序列
    config.knock_o_rate = config.knock_o_rate.multiply(config.knock_o_ratio).tolist()
    
    let calc_price_u = 105.0 // 价格点上界
    let calc_price_d = 65.0 // 价格点下界
    let calc_price_g = 1.0 // 价格点间隔
    //config.calc_price = [65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0, 100.0, 105.0] // 计算价格序列
    config.calc_price = nj.arange(calc_price_d, calc_price_u + calc_price_g, calc_price_g).tolist() // 含价格点上下界
    
    config.run_from = 0 // 起始天数，第一天为零
    config.run_days = 1 // 运行天数
    
    let ret_cols = config.runs_step
    let ret_rows = config.calc_price.length
    
    let phoenix = new derivx.Autocall("Phoenix")
    
    if(phoenix.InitArgs(config) < 0) {
        console.log(phoenix.GetError())
        return
    }
    
    if(phoenix.InitRand() < 0) {
        console.log(phoenix.GetError())
        return
    }
    // 除非电脑性能较差，否则不推荐使用 SaveRand() 和 LoadRand() 了
    // 最好将影响随机数据的参数都包含在文件名中，避免导入的随机数据与所设参数不一致
    //let rand_file = util.format("./rand_data_%d_%d_%d.rand", config.rand_rows, config.rand_cols, config.rand_seed[0])
    //if(phoenix.SaveRand(rand_file) < 0) {
    //    console.log(phoenix.GetError())
    //    return
    //}
    //if(phoenix.LoadRand(rand_file) < 0) {
    //    console.log(phoenix.GetError())
    //    return
    //}
    
    if(phoenix.InitPath() < 0) {
        console.log(phoenix.GetError())
        return
    }
    // 除非电脑性能较差，否则不推荐使用 SavePath() 和 LoadPath() 了
    // 最好将影响路径数据的参数都包含在文件名中，避免导入的路径数据与所设参数不一致
    //let path_file = util.format("./path_data_%d_%d_%d_%d_%f_%f_%f_%f_%d.path", 
    //    config.dual_smooth, config.runs_size, config.runs_step, config.year_days, 
    //    config.sigma, config.risk_free_rate, config.basis_rate, config.price_limit_ratio, config.price_limit_style)
    //if(phoenix.SavePath(path_file) < 0) {
    //    console.log(phoenix.GetError())
    //    return
    //}
    //if(phoenix.LoadPath(path_file) < 0) {
    //    console.log(phoenix.GetError())
    //    return
    //}
    
    let coupon = nj.zeros([1]).tolist()
    phoenix.CalcCoupon(coupon)
    console.log("coupon:", coupon)
    
    //let payoff = nj.zeros([ret_rows, ret_cols]).tolist()
    //phoenix.CalcPayoff(payoff)
    //console.log("payoff:", payoff)
    
    //let greek_flags = {"theta":"t"}
    //let greek_flags = {"delta":"d", "gamma":"g", "vega":"v", "theta":"t", "rho":"r"}
    //for(let [name, flag] of Object.entries(greek_flags)) {
    //    let result = nj.zeros([ret_rows, ret_cols]).tolist()
    //    phoenix.CalcGreeks(flag, result)
    //    console.log("result:", result)
    //}
}

Test_Autocall_Phoenix()
