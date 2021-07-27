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
const util = require('util');

const derivx = require('derivx')

class Config {
    constructor() {
        this.runs_seed = false // 动态路径种子
        this.dual_smooth = true // 对偶平滑路径 // InitPath
        this.runs_size = 0 // 模拟路径数量 // InitPath
        this.runs_step = 0 // 价格变动步数 // InitPath
        this.year_days = 0 // 年交易日数量
        this.notional = 0.0 // 名义本金
        this.start_price = 0.0 // 初始价格
        this.strike_rice = 0.0 // 敲入后执行价格
        this.knock_o_ratio = 0.0 // 敲出比率，非百分比
        this.knock_i_ratio = 0.0 // 敲入比率，非百分比
        this.knock_o_steps = 0.0 // 敲出比例逐月递减率
        this.knock_i_valid = true // 是否有下方敲入障碍
        this.knock_i_occur = false // 是否已经发生敲入
        this.knock_i_margin_call = true // 是否追加保证金
        this.sigma = 0.0 // 波动率 // InitPath
        this.risk_free_rate = 0.0 // 无风险利率 // InitPath
        this.basis_rate = 0.0 // 股息或贴水 // InitPath
        this.coupon_rate = 0.0 // 客户年化收益率
        this.margin_rate = 0.0 // 保证金比例
        this.margin_interest = 0.0 // 保证金利率
        this.price_limit_ratio = 0.0 // 涨跌停限制幅度 // InitPath
        this.prefix_coupon = 0.0 // 不管敲入敲出和到期时间，客户都要求得到固定收益，相当于前端扣费的意思
        this.prefix_coupon_ann = false // false 为绝对收益率，true 为年化收益率
        this.prefix_coupon_use = false // 是否支付 prefix 收益
        this.ukiuko_coupon = 0.0 // 对于无敲出无敲入的情况，客户只要求得到固定收益
        this.ukiuko_coupon_ann = false // false 为绝对收益率，true 为年化收益率
        this.ukiuko_coupon_use = false // 是否支付 ukiuko 收益
        this.calc_price = [] // 计算价格序列
        this.run_from = 0 // 起始天数，第一天为零
        this.run_days = 0 // 运行天数
        this.knock_o_days = [] // 敲出日期序列
        this.knock_o_rate = [] // 敲出比率序列
    }
}

function Test_Snowball() {
    let config = new Config()
    config.runs_seed = false // 动态路径种子
    config.dual_smooth = true // 对偶平滑路径 // InitPath
    config.runs_size = 100000 // 模拟路径数量 // InitPath
    config.runs_step = 488 // 价格变动步数 // InitPath
    config.year_days = 244 // 年交易日数量
    
    config.notional = 100000.0 // 名义本金
    config.start_price = 100.0 // 初始价格
    config.strike_rice = 100.0 // 敲入后执行价格
    config.knock_o_ratio = 1.0 // 敲出比率，非百分比
    config.knock_i_ratio = 0.7 // 敲入比率，非百分比
    config.knock_o_steps = 0.0 // 敲出比例逐月递减率
    config.knock_i_valid = true // 是否有下方敲入障碍
    config.knock_i_occur = false // 是否已经发生敲入
    config.knock_i_margin_call = true // 是否敲入后可追加保证金
    config.sigma = 0.16 // 波动率 // InitPath
    config.risk_free_rate = 0.03 // 无风险利率 // InitPath
    config.basis_rate = 0.05 // 股息或贴水 // InitPath
    config.coupon_rate = 0.11 // 客户年化收益率
    config.margin_rate = 1.0 // 保证金比例
    config.margin_interest = 0.03 // 保证金利率
    config.price_limit_ratio = 0.1 // 涨跌停限制幅度 // InitPath
    
    config.prefix_coupon = 0.0 // 不管敲入敲出和到期时间，客户都要求得到固定收益，相当于前端扣费的意思
    config.prefix_coupon_ann = false // false 为绝对收益率，true 为年化收益率
    config.prefix_coupon_use = false // 是否支付 prefix 收益
    config.ukiuko_coupon = 0.0 // 对于无敲出无敲入的情况，客户只要求得到固定收益
    config.ukiuko_coupon_ann = false // false 为绝对收益率，true 为年化收益率
    config.ukiuko_coupon_use = false // 是否支付 ukiuko 收益
    
    //config.knock_o_days = [61, 81, 101, 122, 142, 162, 183, 203, 223, 244, 264, 284, 305, 325, 345, 366, 386, 406, 427, 447, 467, 488] // 敲出日期序列
    config.knock_o_days = nj.array([61, 81, 101, 122, 142, 162, 183, 203, 223, 244, 264, 284, 305, 325, 345, 366, 386, 406, 427, 447, 467, 488]).tolist() // 敲出日期序列
    
    //config.knock_o_rate = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0] // 敲出比率序列
    //config.knock_o_rate = config.knock_o_rate.map((rate, index) => { return rate * config.knock_o_ratio })
    config.knock_o_rate = nj.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]) // 敲出比率序列
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
    
    let snowball = new derivx.Snowball()
    
    if(snowball.InitArgs(config) < 0) {
        console.log(snowball.GetError())
        return
    }
    
    // 最好将影响路径数据的参数都包含在文件名中，避免导入的路径数据与所设参数不一致
    let path_file = util.format("./path_data_%d_%d_%d_%f_%f_%f_%f.path", 
        config.dual_smooth, config.runs_size, config.runs_step, config.sigma, config.risk_free_rate, config.basis_rate, config.price_limit_ratio)
    if(snowball.LoadPath(path_file) < 0) {
        console.log(snowball.GetError())
        console.log("尝试 生成 路径数据 ...")
        if(snowball.InitPath() < 0) {
            console.log(snowball.GetError())
            return
        } else {
            console.log("生成 路径数据 完成。")
            if(snowball.SavePath(path_file) < 0) {
                console.log(snowball.GetError())
                return
            } else {
                console.log("保存 路径数据 完成。")
            }
        }
    } else {
        console.log("加载 路径数据 完成。")
    }
    
    //if(snowball.InitPath() < 0) {
    //    console.log(snowball.GetError())
    //    return
    //}
    //if(snowball.SavePath("./path_data.path") < 0) {
    //    console.log(snowball.GetError())
    //    return
    //}
    //if(snowball.LoadPath("./path_data.path") < 0) {
    //    console.log(snowball.GetError())
    //    return
    //}
    
    let coupon = nj.zeros([1]).tolist()
    snowball.CalcCoupon(coupon)
    console.log("coupon:", coupon)
    
    //let payoff = nj.zeros([ret_rows, ret_cols]).tolist()
    //snowball.CalcPayoff(payoff)
    //console.log("payoff:", payoff)
    
    //let greek_flags = {"theta":"t"}
    //let greek_flags = {"delta":"d", "gamma":"g", "vega":"v", "theta":"t", "rho":"r"}
    //for(let [name, flag] of Object.entries(greek_flags)) {
    //    let result = nj.zeros([ret_rows, ret_cols]).tolist()
    //    snowball.CalcGreeks(flag, result)
    //    console.log("result:", result)
    //}
    
}

Test_Snowball()
