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
// 1、演示单障碍奇异期权理论价格、收益情况、希腊值等的计算；
// 2、演示通过 Create 方法获取执行模块实例；
// 3、演示 直接模式 DirectCalc 任务执行调用；
// 4、演示任务参数序列化和任务结果反序列化的封装；

'use strict'

const nj = require('numjs')

const syscfg = require('./syscfg')
const cyberx = require('cyberx') // cyberx-js

let func_calc_price  = 1
let func_calc_payoff = 2
let func_calc_greeks = 3

let g_up_in    = 1 // 向上敲入
let g_down_in  = 2 // 向下敲入
let g_up_out   = 3 // 向上敲出 // 看涨情况下，与同为一年期敲出收益为零的欧式看涨单鲨区别蛮大，后者与万得的同期欧式认购出局单向障碍验证一致
let g_down_out = 4 // 向下敲出 // 看跌情况下，与同为一年期敲出收益为零的欧式看跌单鲨区别蛮大，后者与万得的同期欧式认沽出局单向障碍验证一致

// s // 标的价格
// h // 障碍价格
// k // 行权价格
// x // 未触及障碍所需支付资金
// v // 波动率
// r // 无风险利率
// q // 年化分红率
// t // 年化到期期限
// p // 参与率，未敲出情况下客户对收益的占比要求
// is_call // 看涨看跌
// is_futures // 是否期货期权
// is_foreign // 是否外汇期权
// is_kop_delay // 敲出后是立即还是延期支付资金，false 为立即，true 为延期
// barrier_type // 障碍类型
// calc_price // 计算价格序列
// runs_step // 价格变动步数
// year_days // 年交易日数量
// run_from // 起始天数，第一天为零
// run_days // 运行天数

function CalcPrice(module, s, h, k, x, v, r, q, t, p, is_call, is_kop_delay, barrier_type) {
    let inputs = {'s':s, 'h':h, 'k':k, 'x':x, 'v':v, 'r':r, 'q':q, 't':t, 'p':p, 'is_call':is_call, 'is_kop_delay':is_kop_delay, 'barrier_type':barrier_type}
    let result = JSON.parse(module.DirectCalc(func_calc_price, 0, JSON.stringify(inputs)))
    if(result['return_code'] !== 0) {
        console.log(result['return_code'], result['return_info'])
    }
    return result['result_data']
}

function CalcPayoff(module, s, h, k, x, v, r, q, t, p, is_call, is_kop_delay, barrier_type) {
    let inputs = {'s':s, 'h':h, 'k':k, 'x':x, 'v':v, 'r':r, 'q':q, 't':t, 'p':p, 'is_call':is_call, 'is_kop_delay':is_kop_delay, 'barrier_type':barrier_type}
    let result = JSON.parse(module.DirectCalc(func_calc_payoff, 0, JSON.stringify(inputs)))
    if(result['return_code'] !== 0) {
        console.log(result['return_code'], result['return_info'])
    }
    return result['result_data']
}

function CalcGreeks(module, calc_greek, s, h, k, x, v, r, q, t, p, is_call, is_futures, is_foreign, is_kop_delay, barrier_type, calc_price, runs_step, year_days, run_from, run_days) {
    let inputs = {'calc_greek':calc_greek, 's':s, 'h':h, 'k':k, 'x':x, 'v':v, 'r':r, 'q':q, 't':t, 'p':p, 'is_call':is_call, "is_futures":is_futures, "is_foreign":is_foreign, 
                  'is_kop_delay':is_kop_delay, 'barrier_type':barrier_type, 'calc_price':calc_price, 'runs_step':runs_step, 'year_days':year_days, 'run_from':run_from, 'run_days':run_days}
    let result = JSON.parse(module.DirectCalc(func_calc_greeks, 0, JSON.stringify(inputs)))
    if(result['return_code'] !== 0) {
        console.log(result['return_code'], result['return_info'])
    }
    return result['result_data']
}

function Test_DerivX_Barrier_Single() {
    let result = 0.0
    let greeks = []
    let kernel = new cyberx.Kernel(new syscfg.SysCfg()) // 全局唯一
    let module = new cyberx.Create('derivx_barrier_single')
    
    //let array_s = [80.0, 82.0, 84.0, 86.0, 88.0, 90.0, 92.0, 94.0, 96.0, 98.0, 100.0, 102.0, 104.0]
    //for(let i = 0; i < array_s.length; i++) {
    //    result = CalcPrice(module, array_s[i], 80.0, 100.0, 0.0, 0.3, 0.03, 0.02, 1.0, 1.0, true, false, g_down_in)
    //    //result = CalcPrice(module, array_s[i], 80.0, 100.0, 0.0, 0.3, 0.03, 0.02, 1.0, 1.0, true, false, g_down_out)
    //    //result = CalcPrice(module, array_s[i], 80.0, 100.0, 0.0, 0.3, 0.03, 0.02, 1.0, 1.0, false, false, g_down_in)
    //    //result = CalcPrice(module, array_s[i], 80.0, 100.0, 0.0, 0.3, 0.03, 0.02, 1.0, 1.0, false, false, g_down_out)
    //    console.log(result)
    //}
    
    /*
    let args_cdo = [[90.0, 95.0, 0.25], [100.0, 95.0, 0.25], [110.0, 95.0, 0.25], [90.0, 100.0, 0.25], [100.0, 100.0, 0.25], [110.0, 100.0, 0.25],
                    [90.0, 95.0, 0.30], [100.0, 95.0, 0.30], [110.0, 95.0, 0.30], [90.0, 100.0, 0.30], [100.0, 100.0, 0.30], [110.0, 100.0, 0.30]] // k, h, v
    for(let i = 0; i < args_cdo.length; i++) {
        let args = args_cdo[i]
        result = CalcPrice(module, 100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, true, false, g_down_out)
        console.log(result)
    }
    
    let args_cuo = [[90.0, 105.0, 0.25], [100.0, 105.0, 0.25], [110.0, 105.0, 0.25], [90.0, 105.0, 0.30], [100.0, 105.0, 0.30], [110.0, 105.0, 0.30]] // k, h, v
    for(let i = 0; i < args_cuo.length; i++) {
        let args = args_cuo[i]
        result = CalcPrice(module, 100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, true, false, g_up_out)
        console.log(result)
    }
    
    let args_cdi = [[90.0, 95.0, 0.25], [100.0, 95.0, 0.25], [110.0, 95.0, 0.25], [90.0, 100.0, 0.25], [100.0, 100.0, 0.25], [110.0, 100.0, 0.25],
                    [90.0, 95.0, 0.30], [100.0, 95.0, 0.30], [110.0, 95.0, 0.30], [90.0, 100.0, 0.30], [100.0, 100.0, 0.30], [110.0, 100.0, 0.30]] // k, h, v
    for(let i = 0; i < args_cdi.length; i++) {
        let args = args_cdi[i]
        result = CalcPrice(module, 100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, true, false, g_down_in)
        console.log(result)
    }
    
    let args_cui = [[90.0, 105.0, 0.25], [100.0, 105.0, 0.25], [110.0, 105.0, 0.25], [90.0, 105.0, 0.30], [100.0, 105.0, 0.30], [110.0, 105.0, 0.30]] // k, h, v
    for(let i = 0; i < args_cui.length; i++) {
        let args = args_cui[i]
        result = CalcPrice(module, 100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, true, false, g_up_in)
        console.log(result)
    }
    
    let args_pdo = [[90.0, 95.0, 0.25], [100.0, 95.0, 0.25], [110.0, 95.0, 0.25], [90.0, 100.0, 0.25], [100.0, 100.0, 0.25], [110.0, 100.0, 0.25],
                    [90.0, 95.0, 0.30], [100.0, 95.0, 0.30], [110.0, 95.0, 0.30], [90.0, 100.0, 0.30], [100.0, 100.0, 0.30], [110.0, 100.0, 0.30]] // k, h, v
    for(let i = 0; i < args_pdo.length; i++) {
        let args = args_pdo[i]
        result = CalcPrice(module, 100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, false, false, g_down_out)
        console.log(result)
    }
    
    let args_puo = [[90.0, 105.0, 0.25], [100.0, 105.0, 0.25], [110.0, 105.0, 0.25], [90.0, 105.0, 0.30], [100.0, 105.0, 0.30], [110.0, 105.0, 0.30]] // k, h, v
    for(let i = 0; i < args_puo.length; i++) {
        let args = args_puo[i]
        result = CalcPrice(module, 100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, false, false, g_up_out)
        console.log(result)
    }
    
    let args_pdi = [[90.0, 95.0, 0.25], [100.0, 95.0, 0.25], [110.0, 95.0, 0.25], [90.0, 100.0, 0.25], [100.0, 100.0, 0.25], [110.0, 100.0, 0.25],
                    [90.0, 95.0, 0.30], [100.0, 95.0, 0.30], [110.0, 95.0, 0.30], [90.0, 100.0, 0.30], [100.0, 100.0, 0.30], [110.0, 100.0, 0.30]] // k, h, v
    for(let i = 0; i < args_pdi.length; i++) {
        let args = args_pdi[i]
        result = CalcPrice(module, 100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, false, false, g_down_in)
        console.log(result)
    }
    
    let args_pui = [[90.0, 105.0, 0.25], [100.0, 105.0, 0.25], [110.0, 105.0, 0.25], [90.0, 105.0, 0.30], [100.0, 105.0, 0.30], [110.0, 105.0, 0.30]] // k, h, v
    for(let i = 0; i < args_pui.length; i++) {
        let args = args_pui[i]
        result = CalcPrice(module, 100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, 1.0, false, false, g_up_in)
        console.log(result)
    }
    */
    
    /*
    let array_args = []
    
    array_args.push([100.0, 80.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, true, false, g_down_out]) // 未敲出 s - k = 10.0
    array_args.push([100.0, 120.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, true, false, g_down_out]) // 已敲出 x = 3.0
    array_args.push([100.0, 80.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, false, false, g_down_out]) // 未敲出 k - s = 15.0
    array_args.push([100.0, 120.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, false, false, g_down_out]) // 已敲出 x = 3.0
    
    array_args.push([100.0, 120.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, true, false, g_up_out]) // 未敲出 s - k = 10.0
    array_args.push([100.0, 80.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, true, false, g_up_out]) // 已敲出 x = 3.0
    array_args.push([100.0, 120.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, false, false, g_up_out]) // 未敲出 k - s = 15.0
    array_args.push([100.0, 80.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, false, false, g_up_out]) // 已敲出 x = 3.0
    
    array_args.push([100.0, 80.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, true, false, g_down_in]) // 未敲入 x = 3.0
    array_args.push([100.0, 120.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, true, false, g_down_in]) // 已敲入 s - k = 10.0
    array_args.push([100.0, 80.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, false, false, g_down_in]) // 未敲入 x = 3.0
    array_args.push([100.0, 120.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, false, false, g_down_in]) // 已敲入 k - s = 15.0
    
    array_args.push([100.0, 120.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, true, false, g_up_in]) // 未敲入 x = 3.0
    array_args.push([100.0, 80.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, true, false, g_up_in]) // 已敲入 s - k = 10.0
    array_args.push([100.0, 120.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, false, false, g_up_in]) // 未敲入 x = 3.0
    array_args.push([100.0, 80.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, false, false, g_up_in]) // 已敲入 k - s = 15.0
    
    for(let i = 0; i < array_args.length; i++) {
        let args = array_args[i]
        result = CalcPayoff(module, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], args[9], args[10], args[11])
        console.log(result)
    }
    */
    
    let calc_price_u = 115.0 // 价格点上界
    let calc_price_d = 75.0 // 价格点下界
    let calc_price_g = 1.0 // 价格点间隔
    //let calc_price = [65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0, 100.0, 105.0] // 计算价格序列
    let calc_price = nj.arange(calc_price_d, calc_price_u + calc_price_g, calc_price_g).tolist() // 含价格点上下界
    
    let runs_step = 244 // 价格变动步数
    let year_days = 244 // 年交易日数量
    let run_from = 0 // 起始天数，第一天为零
    let run_days = 244 // 运行天数
    
    //let greek_flags = {"delta":"d"}
    let greek_flags = {"delta":"d", "gamma":"g", "vega":"v", "theta":"t", "rho":"r"}
    for(let [name, flag] of Object.entries(greek_flags)) {
        //greeks = CalcGreeks(module, flag, 100.0, 105.0, 101.0, 3.0, 0.2, 0.03, 0.05, 1.0, 1.0, true, false, false, true, g_up_out, calc_price, runs_step, year_days, run_from, run_days)
        greeks = CalcGreeks(module, flag, 100.0, 95.0, 99.0, 3.0, 0.2, 0.03, 0.05, 1.0, 1.0, false, false, false, true, g_down_out, calc_price, runs_step, year_days, run_from, run_days)
        console.log(greeks)
    }
}

Test_DerivX_Barrier_Single()
