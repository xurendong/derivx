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

let g_up_in    = 1 // 向上敲入
let g_down_in  = 2 // 向下敲入
let g_up_out   = 3 // 向上敲出
let g_down_out = 4 // 向下敲出

class Config {
    constructor(s, h, k, x, v, r, q, t, is_call, is_knock, barrier_type) {
        this.s = s // 标的价格
        this.h = h // 障碍价格
        this.k = k // 行权价格
        this.x = x // 未触及障碍所需支付资金
        this.v = v // 波动率
        this.r = r // 无风险利率
        this.q = q // 年化分红率
        this.t = t // 年化到期期限
        this.is_call = is_call // 看涨看跌
        this.is_knock = is_knock // 是否已经敲入敲出
        this.barrier_type = barrier_type // 障碍类型
    }
}

function Test_Barrier_Single() {
    let barrier = new derivx.Barrier("Single")
    
    // Config(s, h, k, x, v, r, q, t, is_call, is_knock, barrier_type)
    
    //let array_s = [80.0, 82.0, 84.0, 86.0, 88.0, 90.0, 92.0, 94.0, 96.0, 98.0, 100.0, 102.0, 104.0]
    //for(let i = 0; i < array_s.length; i++) {
    //    let config = new Config(array_s[i], 80.0, 100.0, 0.0, 0.3, 0.03, 0.02, 1.0, true, false, g_down_in)
    //    //let config = new Config(array_s[i], 80.0, 100.0, 0.0, 0.3, 0.03, 0.02, 1.0, true, false, g_down_out)
    //    //let config = new Config(array_s[i], 80.0, 100.0, 0.0, 0.3, 0.03, 0.02, 1.0, false, false, g_down_in)
    //    //let config = new Config(array_s[i], 80.0, 100.0, 0.0, 0.3, 0.03, 0.02, 1.0, false, false, g_down_out)
    //    if(barrier.InitArgs(config) < 0) {
    //        console.log(barrier.GetError())
    //        return
    //    }
    //    console.log("price:", barrier.CalcPrice())
    //}
    
    let args_cdo = [[90.0, 95.0, 0.25], [100.0, 95.0, 0.25], [110.0, 95.0, 0.25], [90.0, 100.0, 0.25], [100.0, 100.0, 0.25], [110.0, 100.0, 0.25],
                    [90.0, 95.0, 0.30], [100.0, 95.0, 0.30], [110.0, 95.0, 0.30], [90.0, 100.0, 0.30], [100.0, 100.0, 0.30], [110.0, 100.0, 0.30]] // k, h, v
    for(let i = 0; i < args_cdo.length; i++) {
        let args = args_cdo[i]
        let config = new Config(100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, true, false, g_down_out)
        if(barrier.InitArgs(config) < 0) {
            console.log(barrier.GetError())
            return
        }
        console.log("price:", barrier.CalcPrice())
    }
    
    let args_cuo = [[90.0, 105.0, 0.25], [100.0, 105.0, 0.25], [110.0, 105.0, 0.25], [90.0, 105.0, 0.30], [100.0, 105.0, 0.30], [110.0, 105.0, 0.30]] // k, h, v
    for(let i = 0; i < args_cuo.length; i++) {
        let args = args_cuo[i]
        let config = new Config(100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, true, false, g_up_out)
        if(barrier.InitArgs(config) < 0) {
            console.log(barrier.GetError())
            return
        }
        console.log("price:", barrier.CalcPrice())
    }
    
    let args_cdi = [[90.0, 95.0, 0.25], [100.0, 95.0, 0.25], [110.0, 95.0, 0.25], [90.0, 100.0, 0.25], [100.0, 100.0, 0.25], [110.0, 100.0, 0.25],
                    [90.0, 95.0, 0.30], [100.0, 95.0, 0.30], [110.0, 95.0, 0.30], [90.0, 100.0, 0.30], [100.0, 100.0, 0.30], [110.0, 100.0, 0.30]] // k, h, v
    for(let i = 0; i < args_cdi.length; i++) {
        let args = args_cdi[i]
        let config = new Config(100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, true, false, g_down_in)
        if(barrier.InitArgs(config) < 0) {
            console.log(barrier.GetError())
            return
        }
        console.log("price:", barrier.CalcPrice())
    }
    
    let args_cui = [[90.0, 105.0, 0.25], [100.0, 105.0, 0.25], [110.0, 105.0, 0.25], [90.0, 105.0, 0.30], [100.0, 105.0, 0.30], [110.0, 105.0, 0.30]] // k, h, v
    for(let i = 0; i < args_cui.length; i++) {
        let args = args_cui[i]
        let config = new Config(100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, true, false, g_up_in)
        if(barrier.InitArgs(config) < 0) {
            console.log(barrier.GetError())
            return
        }
        console.log("price:", barrier.CalcPrice())
    }
    
    let args_pdo = [[90.0, 95.0, 0.25], [100.0, 95.0, 0.25], [110.0, 95.0, 0.25], [90.0, 100.0, 0.25], [100.0, 100.0, 0.25], [110.0, 100.0, 0.25],
                    [90.0, 95.0, 0.30], [100.0, 95.0, 0.30], [110.0, 95.0, 0.30], [90.0, 100.0, 0.30], [100.0, 100.0, 0.30], [110.0, 100.0, 0.30]] // k, h, v
    for(let i = 0; i < args_pdo.length; i++) {
        let args = args_pdo[i]
        let config = new Config(100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, false, false, g_down_out)
        if(barrier.InitArgs(config) < 0) {
            console.log(barrier.GetError())
            return
        }
        console.log("price:", barrier.CalcPrice())
    }
    
    let args_puo = [[90.0, 105.0, 0.25], [100.0, 105.0, 0.25], [110.0, 105.0, 0.25], [90.0, 105.0, 0.30], [100.0, 105.0, 0.30], [110.0, 105.0, 0.30]] // k, h, v
    for(let i = 0; i < args_puo.length; i++) {
        let args = args_puo[i]
        let config = new Config(100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, false, false, g_up_out)
        if(barrier.InitArgs(config) < 0) {
            console.log(barrier.GetError())
            return
        }
        console.log("price:", barrier.CalcPrice())
    }
    
    let args_pdi = [[90.0, 95.0, 0.25], [100.0, 95.0, 0.25], [110.0, 95.0, 0.25], [90.0, 100.0, 0.25], [100.0, 100.0, 0.25], [110.0, 100.0, 0.25],
                    [90.0, 95.0, 0.30], [100.0, 95.0, 0.30], [110.0, 95.0, 0.30], [90.0, 100.0, 0.30], [100.0, 100.0, 0.30], [110.0, 100.0, 0.30]] // k, h, v
    for(let i = 0; i < args_pdi.length; i++) {
        let args = args_pdi[i]
        let config = new Config(100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, false, false, g_down_in)
        if(barrier.InitArgs(config) < 0) {
            console.log(barrier.GetError())
            return
        }
        console.log("price:", barrier.CalcPrice())
    }
    
    let args_pui = [[90.0, 105.0, 0.25], [100.0, 105.0, 0.25], [110.0, 105.0, 0.25], [90.0, 105.0, 0.30], [100.0, 105.0, 0.30], [110.0, 105.0, 0.30]] // k, h, v
    for(let i = 0; i < args_pui.length; i++) {
        let args = args_pui[i]
        let config = new Config(100.0, args[1], args[0], 3.0, args[2], 0.08, 0.04, 0.5, false, false, g_up_in)
        if(barrier.InitArgs(config) < 0) {
            console.log(barrier.GetError())
            return
        }
        console.log("price:", barrier.CalcPrice())
    }
    
    // Config(s, h, k, x, v, r, q, t, is_call, is_knock, barrier_type)
    
    let array_config = []
    
    array_config.push(new Config(100.0, 0.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, true, false, g_down_out)) // s - k = 10.0
    array_config.push(new Config(100.0, 0.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, true, true, g_down_out)) // x = 3.0
    array_config.push(new Config(100.0, 0.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, false, false, g_down_out)) // k - s = 15.0
    array_config.push(new Config(100.0, 0.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, false, true, g_down_out)) // x = 3.0
    
    array_config.push(new Config(100.0, 0.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, true, false, g_up_out)) // s - k = 10.0
    array_config.push(new Config(100.0, 0.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, true, true, g_up_out)) // x = 3.0
    array_config.push(new Config(100.0, 0.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, false, false, g_up_out)) // k - s = 15.0
    array_config.push(new Config(100.0, 0.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, false, true, g_up_out)) // x = 3.0
    
    array_config.push(new Config(100.0, 0.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, true, false, g_down_in)) // x = 3.0
    array_config.push(new Config(100.0, 0.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, true, true, g_down_in)) // s - k = 10.0
    array_config.push(new Config(100.0, 0.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, false, false, g_down_in)) // x = 3.0
    array_config.push(new Config(100.0, 0.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, false, true, g_down_in)) // k - s = 15.0
    
    array_config.push(new Config(100.0, 0.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, true, false, g_up_in)) // x = 3.0
    array_config.push(new Config(100.0, 0.0, 90.0, 3.0, 0.0, 0.0, 0.0, 0.0, true, true, g_up_in)) // s - k = 10.0
    array_config.push(new Config(100.0, 0.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, false, false, g_up_in)) // x = 3.0
    array_config.push(new Config(100.0, 0.0, 115.0, 3.0, 0.0, 0.0, 0.0, 0.0, false, true, g_up_in)) // k - s = 15.0
    
    for(let i = 0; i < array_config.length; i++) {
        if(barrier.InitArgs(array_config[i]) < 0) {
            console.log(barrier.GetError())
            return
        }
        console.log("payoff:", barrier.CalcPayoff())
    }
}

Test_Barrier_Single()
