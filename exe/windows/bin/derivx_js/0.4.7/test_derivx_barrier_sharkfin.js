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
// 1、演示鲨鱼鳍结构参数设置；
// 2、演示鲨鱼鳍结构价格、收益曲面、希腊值曲面等的计算；
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

let func_calc_price = 1
let func_calc_payoff = 2
let func_calc_greeks = 3

let event_task_finish = null // AbortController

let g_option_european = 1 // 欧式
let g_option_american = 2 // 美式

let g_sharkfin_uc = 1 // 向上敲出看涨，看涨鲨鱼鳍
let g_sharkfin_dp = 2 // 向下敲出看跌，看跌鲨鱼鳍
let g_sharkfin_ucdp = 3 // 向上敲出看涨 + 向下敲出看跌，双鲨鱼鳍

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
        this.x = 0.0 // 敲出后需支付的年化资金
        this.p = 0.0 // 参与率，未敲出情况下客户对收益的占比要求
        this.is_kop_delay = false // 敲出后是立即还是延期支付资金，false 为立即，true 为延期，欧式的此参数无效
        this.option_type = 0 // 期权类型
        this.barrier_type = 0 // 障碍类型
        this.trade_long = true // 交易方向
        this.option_fee = 0.0 // 期权费费率，CalcPrice 时此入参不参与计算
        this.option_fee_interest = 0.0 // 期权费利率
        this.consumed_option_fee_rate = 0.0 // 对冲交易 消耗 的期权费占比，针对 option_fee 的小数非百分比格式
        this.occupied_option_fee_rate = 0.0 // 对冲交易 占用 的期权费占比，针对 option_fee 的小数非百分比格式
        this.back_end_load = false // 期权费支付方式，false 为前端，true 为后端
        this.discount_payoff = false // 是否对票息等收支进行贴现，false 为不贴现，true 为做贴现
        this.discount_option_fee = false // 是否对期权费收支进行贴现，影响期权费后付及先付时交易占用资金，false 为不贴现，true 为做贴现
        this.compound_option_fee = false // 是否对期权费收支进行复利，影响期权费先付及后付时垫付占用资金，false 为不复利，true 为做复利
        this.market_close = false // 是否已经收盘，会影响交易和估值，false 为未收盘，true 为已收盘
        
        this.calc_price = [] // 计算价格序列
        this.run_from = 0 // 起始天数，第一天为零
        this.run_days = 0 // 运行天数
        
        this.calc_greek = '' // 要计算的希腊值标识
    }
    
    ToJson() {
        return JSON.stringify(this)
        //return JSON.stringify(this, null, 4)
    }
}

function OnResult_Price() {
    try {
        let [result] = Array.from(arguments)
        console.log("Callback OnResult_Price:", result)
        if(result['return_code'] !== 0) {
            console.log(result['return_code'], result['return_info'])
        }
        else {
            result = JSON.parse(result['result_data'])
            console.log('price:', result)
        }
    }
    catch(error) {
        console.log('OnResult_Price 异常！' + error)
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

async function Test_DerivX_Barrier_Sharkfin() {
    let kernel = new cyberx.Kernel(new syscfg.SysCfg()) // 全局唯一
    
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
    config.x = 3.5 // 敲出后需支付的年化资金
    config.p = 1.0 // 参与率，未敲出情况下客户对收益的占比要求
    config.is_kop_delay = true // 敲出后是立即还是延期支付资金，false 为立即，true 为延期，欧式的此参数无效
    config.option_type = g_option_american // 期权类型
    config.barrier_type = g_sharkfin_ucdp // 障碍类型
    config.trade_long = false // 交易方向
    config.option_fee = 0.035 // 期权费费率，CalcPrice 时此入参不参与计算
    config.option_fee_interest = 0.03 // 期权费利率
    config.consumed_option_fee_rate = 0.0 // 对冲交易 消耗 的期权费占比，针对 option_fee 的小数非百分比格式
    config.occupied_option_fee_rate = 0.0 // 对冲交易 占用 的期权费占比，针对 option_fee 的小数非百分比格式
    config.back_end_load = false // 期权费支付方式，false 为前端，true 为后端
    config.discount_payoff = false // 是否对票息等收支进行贴现，false 为不贴现，true 为做贴现
    config.discount_option_fee = false // 是否对期权费收支进行贴现，影响期权费后付及先付时交易占用资金，false 为不贴现，true 为做贴现
    config.compound_option_fee = false // 是否对期权费收支进行复利，影响期权费先付及后付时垫付占用资金，false 为不复利，true 为做复利
    config.market_close = false // 是否已经收盘，会影响交易和估值，false 为未收盘，true 为已收盘
    
    let calc_price_u = 110.0 // 价格点上界
    let calc_price_d = 90.0 // 价格点下界
    let calc_price_g = 1.0 // 价格点间隔
    //config.calc_price = [65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0, 100.0, 105.0] // 计算价格序列
    config.calc_price = nj.arange(calc_price_d, calc_price_u + calc_price_g, calc_price_g).tolist() // 含价格点上下界
    
    config.run_from = 0 // 起始天数，第一天为零
    config.run_days = 1 // 运行天数
    
    let ret_cols = config.runs_step
    let ret_rows = config.calc_price.length
    
    //console.log(config.ToJson())
    
    let result = null
    
    let tasker_test = new tasker.Tasker()
    tasker_test.plugin_id = 'derivx_barrier_sharkfin'
    tasker_test.timeout_wait = 3600 // 秒
    tasker_test.common_args = config.ToJson()
    
    tasker_test.method_id = func_calc_price
    
    //result = kernel.AssignTask(tasker_test) // 同步
    //console.log('同步:', result)
    //if(result['return_code'] !== 0) {
    //    console.log(result['return_code'], result['return_info'])
    //}
    //else {
    //    result = JSON.parse(result['result_data'])
    //    console.log('price:', result)
    //}
    
    //event_task_finish = new AbortController()
    //result = kernel.AssignTask(tasker_test, OnResult_Price) // 异步
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

Test_DerivX_Barrier_Sharkfin()
