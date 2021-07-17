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

const derivx = require('./derivx')

class Config {
    constructor() {
        this.runs_seed = false // 动态路径种子
        this.runs_size = 0 // 模拟路径数量
        this.runs_step = 0 // 价格变动步数
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
    config.runs_size = 100000 // 模拟路径数量
    config.runs_step = 488 // 价格变动步数
    config.year_days = 244 // 年交易日数量
    
    config.notional = 100000.0 // 名义本金
    config.start_price = 100.0 // 初始价格
    config.strike_rice = 100.0 // 敲入后执行价格
    config.knock_o_ratio = 1.02 // 敲出比率，非百分比
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
    
    config.knock_o_days = [61, 81, 101, 122, 142, 162, 183, 203, 223, 244, 264, 284, 305, 325, 345, 366, 386, 406, 427, 447, 467, 488] // 敲出日期序列
    config.knock_o_rate = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0] // 敲出比率序列
    config.knock_o_rate = config.knock_o_rate.map((rate, index) => { return rate * config.knock_o_ratio })
    
    config.calc_price = [65.0, 66.0, 67.0, 68.0, 69.0, 70.0, 71.0, 72.0, 73.0, 74.0, 75.0, 76.0, 77.0, 78.0, 79.0, 80.0, 81.0, 82.0, 83.0, 84.0, 85.0, 
                         86.0, 87.0, 88.0, 89.0, 90.0, 91.0, 92.0, 93.0, 94.0, 95.0, 96.0, 97.0, 98.0, 99.0, 100.0, 101.0, 102.0, 103.0, 104.0, 105.0] // 计算价格序列
    
    config.run_from = 0 // 起始天数，第一天为零
    config.run_days = 1 // 运行天数
    
    let ret_cols = config.runs_step
    let ret_rows = config.calc_price.length
    
    let snowball = new derivx.Snowball()
    
    if(snowball.InitArgs(config) < 0) {
        console.log(snowball.GetError())
        return
    }
    
    if(snowball.LoadPath("./path_data.path") < 0) {
        console.log(snowball.GetError())
        console.log("尝试 生成 路径数据 ...")
        if(snowball.InitPath() < 0) {
            console.log(snowball.GetError())
            return
        } else {
            console.log("生成 路径数据 完成。")
            if(snowball.SavePath("./path_data.path") < 0) {
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
    
}

Test_Snowball()
