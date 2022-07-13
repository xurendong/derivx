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

// 示例说明：
// 1、演示雪球结构参数设置；
// 2、演示雪球结构客户票息、收益曲面、希腊值曲面等的计算；
// 3、演示 tasker 任务信息创建；
// 4、演示 同步模式 和 异步模式 的 AssignTask 任务执行调用；
// 5、演示异步回调函数的编写和使用；

'use strict'

// 使用 timers/promises 的 setTimeout 要求 Node 版本为 15.0.0 及以上
// 以后可以用 timers/promises 的 scheduler.wait 代替，要求 Node 版本为 17.3.0 及以上
const promises = require('timers/promises')

const nj = require('numjs')

const syscfg = require('./syscfg')
const tasker = require('./tasker')
const cyberx = require('cyberx') // cyberx-js

let func_calc_coupon = 1
let func_calc_payoff = 2
let func_calc_greeks = 3

let event_task_finish = null // AbortController

class Config {
    constructor() {
        this.rand_rows = 0 // 随机数据行数
        this.rand_cols = 0 // 随机数据列数
        this.rand_quasi = false // 随机数据类型 // 目前 quasi 随机数据只能使用单核处理
        this.rand_seed = [] // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量，目前 quasi 仅第一位有效
        
        this.dual_smooth = true // 对偶平滑路径
        this.runs_size = 0 // 模拟路径数量
        this.runs_step = 0 // 价格变动步数
        this.year_days = 0 // 年交易日数量
        this.sigma = 0.0 // 波动率
        this.risk_free_rate = 0.0 // 无风险利率
        this.basis_rate = 0.0 // 股息或贴水
        this.price_limit_ratio = 0.0 // 涨跌停限制幅度
        this.price_limit_style = 0 // 涨跌停限制方式，0 不限制，1 超限部分移至下日，2 超限部分直接削掉
        
        this.notional = 0.0 // 名义本金，目前未使用
        this.trade_long = true // 交易方向
        this.start_price = 0.0 // 初始价格
        this.strike_price = 0.0 // 敲入后执行价格
        this.knock_o_ratio = 0.0 // 敲出比率，非百分比
        this.knock_i_ratio = 0.0 // 敲入比率，非百分比
        this.knock_o_steps = 0.0 // 敲出比例逐月递减率
        this.knock_i_valid = true // 是否有下方敲入障碍，置为 false 则变成保本小雪球
        this.knock_i_occur = false // 是否已经发生敲入
        this.knock_i_margin_call = true // 是否敲入后可追加保证金，置为 false 则变成不追保雪球
        this.coupon_rate = [] // 客户年化收益率（阶段票息），CalcCoupon 时此入参不参与计算
        this.margin_rate = 0.0 // 保证金比例
        this.margin_interest = 0.0 // 保证金利率
        this.use_option_fee = false // 使用期权费方式而非保证金方式
        this.option_fee = 0.0 // 期权费费率
        this.option_fee_interest = 0.0 // 期权费利率
        this.back_end_load = false // 期权费支付方式，false 为前端，true 为后端
        this.prefix_coupon = 0.0 // 不管敲入敲出和到期时间，客户都要求得到固定收益，相当于前端扣费的意思
        this.prefix_coupon_ann = false // false 为绝对收益率，true 为年化收益率
        this.prefix_coupon_use = false // 是否支付 prefix 收益
        this.ukiuko_coupon = 0.0 // 对于无敲出无敲入的情况，客户只要求得到固定收益
        this.ukiuko_coupon_ann = false // false 为绝对收益率，true 为年化收益率
        this.ukiuko_coupon_use = false // 是否支付 ukiuko 收益，false 为红利票息等同敲出票息，true 为单独指定红利票息
        this.calc_price = [] // 计算价格序列
        this.run_from = 0 // 起始天数，第一天为零
        this.run_days = 0 // 运行天数
        this.knock_o_days = [] // 敲出日期序列(交易日)
        this.knock_o_rate = [] // 敲出比率序列
        
        // 只影响 func_calc_coupon 票息计算，用户不传入则默认与 runs_step、year_days、knock_o_days 一致
        this.runs_step_n = 0 // 产品自然日数 (可选)
        this.year_days_n = 0 // 年自然日数量 (可选)
        this.knock_o_days_n = [] // 敲出日期序列(自然日) (可选)
        
        this.calc_greek = '' // 要计算的希腊值标识
    }
    
    ToJson() {
        return JSON.stringify(this)
        //return JSON.stringify(this, null, 4)
    }
}

function OnResult_Coupon() {
    try {
        let [result] = Array.from(arguments)
        console.log("Callback OnResult_Coupon:", result)
        if(result['return_code'] !== 0) {
            console.log(result['return_code'], result['return_info'])
        }
        else {
            result = JSON.parse(result['result_data'])
            console.log('coupon:', result)
        }
    }
    catch(error) {
        console.log('OnResult_Coupon 异常！' + error)
    }
    event_task_finish.abort() //
}

function OnResult_Payoff() {
    try {
        let [result] = Array.from(arguments)
        if(result['return_code'] !== 0) {
            console.log(result['return_code'], result['return_info'])
        }
        else {
            result = JSON.parse(result['result_data'])
            console.log('payoff:', result)
        }
    }
    catch(error) {
        console.log('OnResult_Payoff 异常！' + error)
    }
    event_task_finish.abort() //
}

function OnResult_Greeks() {
    try {
        let [result] = Array.from(arguments)
        if(result['return_code'] !== 0) {
            console.log(result['return_code'], result['return_info'])
        }
        else {
            result = JSON.parse(result['result_data'])
            console.log('greeks:', result)
        }
    }
    catch(error) {
        console.log('OnResult_Greeks 异常！' + error)
    }
    event_task_finish.abort() //
}

async function Test_DerivX_Autocall_Snowball_Stage_Coupon() {
    let kernel = new cyberx.Kernel(new syscfg.SysCfg()) // 全局唯一
    
    let config = new Config()
    config.rand_rows = 50000 // 随机数据行数
    config.rand_cols = 500 // 随机数据列数
    config.rand_quasi = false // 随机数据类型 // 目前 quasi 随机数据只能使用单核处理
    config.rand_seed = nj.array([0, 1, 2, 3, 4, 5, 6, 7]).tolist() // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量，目前 quasi 仅第一位有效
    
    config.dual_smooth = true // 对偶平滑路径
    config.runs_size = 100000 // 模拟路径数量
    config.runs_step = 488 // 价格变动步数
    config.year_days = 244 // 年交易日数量
    config.sigma = 0.16 // 波动率
    config.risk_free_rate = 0.03 // 无风险利率
    config.basis_rate = 0.05 // 股息或贴水
    config.price_limit_ratio = 0.1 // 涨跌停限制幅度
    config.price_limit_style = 0 // 涨跌停限制方式，0 不限制，1 超限部分移至下日，2 超限部分直接削掉
    
    config.notional = 100000.0 // 名义本金，目前未使用
    config.trade_long = false // 交易方向
    config.start_price = 100.0 // 初始价格
    config.strike_price = 100.0 // 敲入后执行价格
    config.knock_o_ratio = 1.0 // 敲出比率，非百分比
    config.knock_i_ratio = 0.7 // 敲入比率，非百分比
    config.knock_o_steps = 0.0 // 敲出比例逐月递减率
    config.knock_i_valid = true // 是否有下方敲入障碍，置为 false 则变成保本小雪球
    config.knock_i_occur = false // 是否已经发生敲入
    config.knock_i_margin_call = true // 是否敲入后可追加保证金，置为 false 则变成不追保雪球
    // config.coupon_rate = [] // 客户年化收益率（阶段票息），CalcCoupon 时此入参不参与计算
    config.margin_rate = 1.0 // 保证金比例
    config.margin_interest = 0.03 // 保证金利率
    config.use_option_fee = false // 使用期权费方式而非保证金方式
    config.option_fee = 0.0 // 期权费费率
    config.option_fee_interest = 0.03 // 期权费利率
    config.back_end_load = false // 期权费支付方式，false 为前端，true 为后端
    
    config.prefix_coupon = 0.0 // 不管敲入敲出和到期时间，客户都要求得到固定收益，相当于前端扣费的意思
    config.prefix_coupon_ann = false // false 为绝对收益率，true 为年化收益率
    config.prefix_coupon_use = false // 是否支付 prefix 收益
    config.ukiuko_coupon = 0.0 // 对于无敲出无敲入的情况，客户只要求得到固定收益
    config.ukiuko_coupon_ann = false // false 为绝对收益率，true 为年化收益率
    config.ukiuko_coupon_use = false // 是否支付 ukiuko 收益，false 为红利票息等同敲出票息，true 为单独指定红利票息
    
    //   1    2    3    4    5    6    7    8    9   10   11   12   13   14   15   16   17   18   19   20   21   22   23   24   25   26   27   28   29   30   31   32   33   34   35   36  
    //  20,  40,  61,  81, 101, 122, 142, 162, 183, 203, 223, 244, 264, 284, 305, 325, 345, 366, 386, 406, 427, 447, 467, 488, 508, 528, 549, 569, 589, 610, 630, 650, 671, 691, 711, 732
    // 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0
    
    config.coupon_rate = nj.array([0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]).tolist() // 客户年化收益率（阶段票息），CalcCoupon 时此入参不参与计算
    
    //config.knock_o_days = [61, 81, 101, 122, 142, 162, 183, 203, 223, 244, 264, 284, 305, 325, 345, 366, 386, 406, 427, 447, 467, 488] // 敲出日期序列(交易日)
    config.knock_o_days = nj.array([61, 81, 101, 122, 142, 162, 183, 203, 223, 244, 264, 284, 305, 325, 345, 366, 386, 406, 427, 447, 467, 488]).tolist() // 敲出日期序列(交易日)
    
    //config.knock_o_rate = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0] // 敲出比率序列
    //config.knock_o_rate = config.knock_o_rate.map((rate, index) => { return rate * config.knock_o_ratio })
    config.knock_o_rate = nj.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]) // 敲出比率序列
    config.knock_o_rate = config.knock_o_rate.multiply(config.knock_o_ratio).tolist()
    
    let calc_price_u = 105.0 // 价格点上界
    let calc_price_d = 65.0 // 价格点下界
    let calc_price_g = 1.0 // 价格点间隔
    //config.calc_price = [65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0, 100.0, 105.0] // 计算价格序列
    config.calc_price = nj.arange(calc_price_d, calc_price_u + calc_price_g, calc_price_g).tolist() // 含价格点上下界
    
    // 只影响 func_calc_coupon 票息计算，用户不传入则默认与 runs_step、year_days、knock_o_days 一致
    //config.runs_step_n = 720 // 产品自然日数 (可选)
    //config.year_days_n = 365 // 年自然日数量 (可选)
    //config.knock_o_days_n = nj.array([90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 480, 510, 540, 570, 600, 630, 660, 690, 720]).tolist() // 敲出日期序列(自然日) (可选)
    
    config.run_from = 0 // 起始天数，第一天为零
    config.run_days = 1 // 运行天数
    
    let ret_cols = config.runs_step
    let ret_rows = config.calc_price.length
    
    //console.log(config.ToJson())
    
    let result = null
    
    let tasker_test = new tasker.Tasker()
    tasker_test.plugin_id = 'derivx_autocall_snowball_stage_coupon'
    tasker_test.timeout_wait = 3600 // 秒
    tasker_test.common_args = config.ToJson()
    
    tasker_test.method_id = func_calc_coupon
    
    //result = kernel.AssignTask(tasker_test) // 同步
    //console.log('同步:', result)
    //if(result['return_code'] !== 0) {
    //    console.log(result['return_code'], result['return_info'])
    //}
    //else {
    //    result = JSON.parse(result['result_data'])
    //    console.log('coupon:', result)
    //}
    
    //event_task_finish = new AbortController()
    //result = kernel.AssignTask(tasker_test, OnResult_Coupon) // 异步
    //console.log('异步:', result)
    //if(result['return_code'] !== 0) {
    //    console.log(result['return_code'], result['return_info'])
    //}
    //else {
    //    let tasker_id = result['tasker_id']
    //    const ret_wait = await promises.setTimeout(tasker_test.timeout_wait * 1000, '', { signal:event_task_finish.signal }).then(() => false, err => true) // 等待任务结果
    //    if(ret_wait != true) {
    //        console.log('等待任务结果超时！' + tasker_id)
    //    }
    //}
    
    tasker_test.method_id = func_calc_payoff
    
    //result = kernel.AssignTask(tasker_test) // 同步
    //if(result['return_code'] !== 0) {
    //    console.log(result['return_code'], result['return_info'])
    //}
    //else {
    //    result = JSON.parse(result['result_data'])
    //    console.log('payoff:', result)
    //}
    
    //event_task_finish = new AbortController()
    //result = kernel.AssignTask(tasker_test, OnResult_Payoff) // 异步
    //console.log('异步:', result)
    //if(result['return_code'] !== 0) {
    //    console.log(result['return_code'], result['return_info'])
    //}
    //else {
    //    let tasker_id = result['tasker_id']
    //    const ret_wait = await promises.setTimeout(tasker_test.timeout_wait * 1000, '', { signal:event_task_finish.signal }).then(() => false, err => true) // 等待任务结果
    //    if(ret_wait != true) {
    //        console.log('等待任务结果超时！' + tasker_id)
    //    }
    //}
    
    tasker_test.method_id = func_calc_greeks
    
    //let greek_flags = {"delta":"d"}
    let greek_flags = {"delta":"d", "gamma":"g", "vega":"v", "theta":"t", "rho":"r"}
    for(let [name, flag] of Object.entries(greek_flags)) {
        config.calc_greek = flag
        tasker_test.common_args = config.ToJson()
        
        //result = kernel.AssignTask(tasker_test) // 同步
        //if(result['return_code'] !== 0) {
        //    console.log(result['return_code'], result['return_info'])
        //}
        //else {
        //    result = JSON.parse(result['result_data'])
        //    console.log('greeks:', result)
        //}
        
        //event_task_finish = new AbortController()
        //result = kernel.AssignTask(tasker_test, OnResult_Greeks) // 异步
        //console.log('异步:', result)
        //if(result['return_code'] !== 0) {
        //    console.log(result['return_code'], result['return_info'])
        //}
        //else {
        //    let tasker_id = result['tasker_id']
        //    const ret_wait = await promises.setTimeout(tasker_test.timeout_wait * 1000, '', { signal:event_task_finish.signal }).then(() => false, err => true) // 等待任务结果
        //    if(ret_wait != true) {
        //        console.log('等待任务结果超时！' + tasker_id)
        //    }
        //}
    }
}

Test_DerivX_Autocall_Snowball_Stage_Coupon()
