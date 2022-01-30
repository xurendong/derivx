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

const syscfg = require('./syscfg')
const cyberx = require('cyberx') // cyberx-js

let func_calc_price = 1
let func_calc_greek = 2
let func_calc_greek_surface = 3

function CalcPrice(module, model, s, k, r, q, v, t, is_call) {
    let inputs = {'model':model, 's':s, 'k':k, 'r':r, 'q':q, 'v':v, 't':t, 'is_call':is_call}
    let result = JSON.parse(module.DirectCalc(func_calc_price, 0, JSON.stringify(inputs)))
    if(result['ret_code'] !== 0) {
        console.log(result['ret_code'], result['ret_info'])
    }
    return result['ret_data']
}

function CalcGreek(module, model, greek, s, k, r, q, v, t, is_long = true, is_call = true, is_futures = false, is_foreign = false) {
    let inputs = {'model':model, 'greek':greek, 's':s, 'k':k, 'r':r, 'q':q, 'v':v, 't':t, 'is_long':is_long, 'is_call':is_call, 'is_futures':is_futures, 'is_foreign':is_foreign}
    let result = JSON.parse(module.DirectCalc(func_calc_greek, 0, JSON.stringify(inputs)))
    if(result['ret_code'] !== 0) {
        console.log(result['ret_code'], result['ret_info'])
    }
    return result['ret_data']
}

function CalcGreekSurface(module, model, greek, array_s, k, r, q, v, array_t, is_long = true, is_call = true, is_futures = false, is_foreign = false) {
    let inputs = {'model':model, 'greek':greek, 'array_s':array_s, 'k':k, 'r':r, 'q':q, 'v':v, 'array_t':array_t, 'is_long':is_long, 'is_call':is_call, 'is_futures':is_futures, 'is_foreign':is_foreign}
    let result = JSON.parse(module.DirectCalc(func_calc_greek_surface, 0, JSON.stringify(inputs)))
    if(result['ret_code'] !== 0) {
        console.log(result['ret_code'], result['ret_info'])
    }
    return result['ret_data']
}

function CalcPrice_Spread_Bull_Call(module, model, s, k_l_c_l, k_h_c_s, r, q, v_l_c_l, v_h_c_s, t) {
    let price_low_call_long = CalcPrice(module, model, s, k_l_c_l, r, q, v_l_c_l, t, true)
    let price_high_call_short = -CalcPrice(module, model, s, k_h_c_s, r, q, v_h_c_s, t, true) // -
    return price_low_call_long + price_high_call_short
}

function CalcPrice_Spread_Bull_Put(module, model, s, k_l_p_l, k_h_p_s, r, q, v_l_p_l, v_h_p_s, t) {
    let price_low_put_long = CalcPrice(module, model, s, k_l_p_l, r, q, v_l_p_l, t, false)
    let price_high_put_short = -CalcPrice(module, model, s, k_h_p_s, r, q, v_h_p_s, t, false) // -
    return price_low_put_long + price_high_put_short
}

function CalcPrice_Spread_Bear_Call(module, model, s, k_l_c_s, k_h_c_l, r, q, v_l_c_s, v_h_c_l, t) {
    let price_low_call_short = -CalcPrice(module, model, s, k_l_c_s, r, q, v_l_c_s, t, true) // -
    let price_high_call_long = CalcPrice(module, model, s, k_h_c_l, r, q, v_h_c_l, t, true)
    return price_low_call_short + price_high_call_long
}

function CalcPrice_Spread_Bear_Put(module, model, s, k_l_p_s, k_h_p_l, r, q, v_l_p_s, v_h_p_l, t) {
    let price_low_put_short = -CalcPrice(module, model, s, k_l_p_s, r, q, v_l_p_s, t, false) // -
    let price_high_put_long = CalcPrice(module, model, s, k_h_p_l, r, q, v_h_p_l, t, false)
    return price_low_put_short + price_high_put_long
}

function CalcPrice_Spread_Butterfly_Call(module, model, s, k_l_c_l, k_m_c_s, k_h_c_l, r, q, v_l_c_l, v_m_c_s, v_h_c_l, t) {
    let price_low_call_long = CalcPrice(module, model, s, k_l_c_l, r, q, v_l_c_l, t, true)
    let price_middle_call_short = -CalcPrice(module, model, s, k_m_c_s, r, q, v_m_c_s, t, true) * 2 // - // * 2
    let price_high_call_long = CalcPrice(module, model, s, k_h_c_l, r, q, v_h_c_l, t, true)
    return price_low_call_long + price_middle_call_short + price_high_call_long
}

function CalcPrice_Spread_Butterfly_Put(module, model, s, k_l_p_l, k_m_p_s, k_h_p_l, r, q, v_l_p_l, v_m_p_s, v_h_p_l, t) {
    let price_low_put_long = CalcPrice(module, model, s, k_l_p_l, r, q, v_l_p_l, t, false)
    let price_middle_put_short = -CalcPrice(module, model, s, k_m_p_s, r, q, v_m_p_s, t, false) * 2 // - // * 2
    let price_high_put_long = CalcPrice(module, model, s, k_h_p_l, r, q, v_h_p_l, t, false)
    return price_low_put_long + price_middle_put_short + price_high_put_long
}

function CalcPrice_Spread_Box_Bull_Call_Bear_Put(module, model, s, k_l_cp_ls, k_h_cp_sl, r, q, v_l_cp_ls, v_h_cp_sl, t) {
    let price_bull_call = CalcPrice_Spread_Bull_Call(module, model, s, k_l_cp_ls, k_h_cp_sl, r, q, v_l_cp_ls, v_h_cp_sl, t)
    let price_bear_put = CalcPrice_Spread_Bear_Put(module, model, s, k_l_cp_ls, k_h_cp_sl, r, q, v_l_cp_ls, v_h_cp_sl, t)
    return price_bull_call + price_bear_put
}

function CalcPrice_Spread_Box_Bull_Put_Bear_Call(module, model, s, k_l_pc_ls, k_h_pc_sl, r, q, v_l_pc_ls, v_h_pc_sl, t) {
    let price_bull_put = CalcPrice_Spread_Bull_Put(module, model, s, k_l_pc_ls, k_h_pc_sl, r, q, v_l_pc_ls, v_h_pc_sl, t)
    let price_bear_call = CalcPrice_Spread_Bear_Call(module, model, s, k_l_pc_ls, k_h_pc_sl, r, q, v_l_pc_ls, v_h_pc_sl, t)
    return price_bull_put + price_bear_call
}

function CalcGreek_Spread_Bull_Call(module, model, greek, s, k_l_c_l, k_h_c_s, r, q, v_l_c_l, v_h_c_s, t, is_long) {
    let result = 0.0
    if(model === "bs") {
        if(greek === "d") {
            let delta_low_call_long = CalcGreek(module, model, greek, s, k_l_c_l, r, q, v_l_c_l, t, true, true)
            let delta_high_call_short = CalcGreek(module, model, greek, s, k_h_c_s, r, q, v_h_c_s, t, false, true)
            result = delta_low_call_long + delta_high_call_short
        }
        else if(greek === "g") {
            let gamma_low_call_long = CalcGreek(module, model, greek, s, k_l_c_l, r, q, v_l_c_l, t, true)
            let gamma_high_call_short = CalcGreek(module, model, greek, s, k_h_c_s, r, q, v_h_c_s, t, false)
            result = gamma_low_call_long + gamma_high_call_short
        }
        else if(greek === "v") {
            let vega_low_call_long = CalcGreek(module, model, greek, s, k_l_c_l, r, q, v_l_c_l, t, true)
            let vega_high_call_short = CalcGreek(module, model, greek, s, k_h_c_s, r, q, v_h_c_s, t, false)
            result = vega_low_call_long + vega_high_call_short
        }
        else if(greek === "t") {
            let theta_low_call_long = CalcGreek(module, model, greek, s, k_l_c_l, r, q, v_l_c_l, t, true, true)
            let theta_high_call_short = CalcGreek(module, model, greek, s, k_h_c_s, r, q, v_h_c_s, t, false, true)
            result = theta_low_call_long + theta_high_call_short
        }
        else if(greek === "r") {
            let rho_low_call_long = CalcGreek(module, model, greek, s, k_l_c_l, r, q, v_l_c_l, t, true, true, false, false)
            let rho_high_call_short = CalcGreek(module, model, greek, s, k_h_c_s, r, q, v_h_c_s, t, false, true, false, false)
            result = rho_low_call_long + rho_high_call_short
        }
    }
    if(is_long === true) {
        return result
    }
    else {
        return -result
    }
}

function CalcGreekSurface_Spread_Bull_Call(module, model, greek, array_s, k_l_c_l, k_h_c_s, r, q, v_l_c_l, v_h_c_s, array_t, is_long) {
    let surface_low_call_long = nj.zeros([array_s.length, array_t.length]).tolist()
    let surface_high_call_short = nj.zeros([array_s.length, array_t.length]).tolist()
    if(model === "bs") {
        if(greek === "d") {
            surface_low_call_long = CalcGreekSurface(module, model, greek, array_s, k_l_c_l, r, q, v_l_c_l, array_t, true, true)
            surface_high_call_short = CalcGreekSurface(module, model, greek, array_s, k_h_c_s, r, q, v_h_c_s, array_t, false, true)
        }
        else if(greek === "g") {
            surface_low_call_long = CalcGreekSurface(module, model, greek, array_s, k_l_c_l, r, q, v_l_c_l, array_t, true)
            surface_high_call_short = CalcGreekSurface(module, model, greek, array_s, k_h_c_s, r, q, v_h_c_s, array_t, false)
        }
        else if(greek === "v") {
            surface_low_call_long = CalcGreekSurface(module, model, greek, array_s, k_l_c_l, r, q, v_l_c_l, array_t, true)
            surface_high_call_short = CalcGreekSurface(module, model, greek, array_s, k_h_c_s, r, q, v_h_c_s, array_t, false)
        }
        else if(greek === "t") {
            surface_low_call_long = CalcGreekSurface(module, model, greek, array_s, k_l_c_l, r, q, v_l_c_l, array_t, true, true)
            surface_high_call_short = CalcGreekSurface(module, model, greek, array_s, k_h_c_s, r, q, v_h_c_s, array_t, false, true)
        }
        else if(greek === "r") {
            surface_low_call_long = CalcGreekSurface(module, model, greek, array_s, k_l_c_l, r, q, v_l_c_l, array_t, true, true, false, false)
            surface_high_call_short = CalcGreekSurface(module, model, greek, array_s, k_h_c_s, r, q, v_h_c_s, array_t, false, true, false, false)
        }
    }
    surface_low_call_long = nj.array(surface_low_call_long, "float64")
    surface_high_call_short = nj.array(surface_high_call_short, "float64")
    let result = surface_low_call_long.add(surface_high_call_short, false)
    if(is_long === true) {
        return result.tolist()
    }
    else {
        return nj.zeros([array_s.length, array_t.length]).subtract(result, false).tolist()
    }
}

function Test_DerivX_Vanilla_European() {
    let result = 0.0
    let surface = []
    let kernel = new cyberx.Kernel(new syscfg.SysCfg()) // 全局唯一
    let module = new cyberx.Create('derivx_vanilla_european')
    
    //result = CalcPrice(module, 'bs', 100.0, 100.0, 0.03, 0.085 - 0.03, 0.15, 1.0, true)
    //result = CalcPrice(module, 'bs', 42.0, 40.0, 0.1, 0.0, 0.2, 0.5, true)
    //result = CalcGreek(module, 'bs', 'd', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, true)
    //result = CalcGreek(module, 'bs', 'g', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreek(module, 'bs', 'v', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreek(module, 'bs', 't', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, true)
    //result = CalcGreek(module, 'bs', 'r', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, true, false, false)
    //console.log(result)
    
    //result = CalcPrice(module, 'bs', 100.0, 100.0, 0.03, 0.085 + 0.03, 0.15, 1.0, false)
    //result = CalcPrice(module, 'bs', 42.0, 40.0, 0.1, 0.0, 0.2, 0.5, false)
    //result = CalcGreek(module, 'bs', 'd', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, false)
    //result = CalcGreek(module, 'bs', 'g', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreek(module, 'bs', 'v', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreek(module, 'bs', 't', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, false)
    //result = CalcGreek(module, 'bs', 'r', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, false, false, false)
    //console.log(result)
    
    //let array_s = nj.arange(5.0, 105.0, 5.0).tolist()
    //let array_t = nj.arange(0.004, 1.004, 1.0 / 250).tolist()
    
    //surface = CalcGreekSurface(module, 'bs', 'd', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, true)
    //surface = CalcGreekSurface(module, 'bs', 'g', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true)
    //surface = CalcGreekSurface(module, 'bs', 'v', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true)
    //surface = CalcGreekSurface(module, 'bs', 't', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, true)
    //surface = CalcGreekSurface(module, 'bs', 'r', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, true, false, false)
    //console.log(surface)
    
    //surface = CalcGreekSurface(module, 'bs', 'd', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, false)
    //surface = CalcGreekSurface(module, 'bs', 'g', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true)
    //surface = CalcGreekSurface(module, 'bs', 'v', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true)
    //surface = CalcGreekSurface(module, 'bs', 't', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, false)
    //surface = CalcGreekSurface(module, 'bs', 'r', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, false, false, false)
    //console.log(surface)
    
    let array_s = nj.arange(5.0, 105.0, 5.0).tolist()
    let array_t = nj.arange(0.004, 1.004, 1.0 / 250).tolist()
    let model = "bs", s = 50.0, k_l = 40.0, k_m = 50.0, k_h = 60.0, r = 0.05, q = 0.0, v_l = 0.2, v_m = 0.2, v_h = 0.2, t = 0.5, is_long = true
    //console.log(CalcPrice_Spread_Bull_Call(module, model, s, k_l, k_h, r, q, v_l, v_h, t))
    //console.log(CalcPrice_Spread_Bull_Put(module, model, s, k_l, k_h, r, q, v_l, v_h, t))
    //console.log(CalcPrice_Spread_Bear_Call(module, model, s, k_l, k_h, r, q, v_l, v_h, t))
    //console.log(CalcPrice_Spread_Bear_Put(module, model, s, k_l, k_h, r, q, v_l, v_h, t))
    //console.log(CalcPrice_Spread_Butterfly_Call(module, model, s, k_l, k_m, k_h, r, q, v_l, v_m, v_h, t))
    //console.log(CalcPrice_Spread_Butterfly_Put(module, model, s, k_l, k_m, k_h, r, q, v_l, v_m, v_h, t))
    //console.log(CalcPrice_Spread_Box_Bull_Call_Bear_Put(module, model, s, k_l, k_h, r, q, v_l, v_h, t))
    //console.log(CalcPrice_Spread_Box_Bull_Put_Bear_Call(module, model, s, k_l, k_h, r, q, v_l, v_h, t))
    //console.log(CalcGreek_Spread_Bull_Call(module, model, "d", s, k_l, k_h, r, q, v_l, v_h, t, is_long))
    //console.log(CalcGreek_Spread_Bull_Call(module, model, "g", s, k_l, k_h, r, q, v_l, v_h, t, is_long))
    //console.log(CalcGreek_Spread_Bull_Call(module, model, "v", s, k_l, k_h, r, q, v_l, v_h, t, is_long))
    //console.log(CalcGreek_Spread_Bull_Call(module, model, "t", s, k_l, k_h, r, q, v_l, v_h, t, is_long))
    //console.log(CalcGreek_Spread_Bull_Call(module, model, "r", s, k_l, k_h, r, q, v_l, v_h, t, is_long))
    //surface = CalcGreekSurface_Spread_Bull_Call(module, model, "d", array_s, k_l, k_h, r, q, v_l, v_h, array_t, is_long)
    //surface = CalcGreekSurface_Spread_Bull_Call(module, model, "g", array_s, k_l, k_h, r, q, v_l, v_h, array_t, is_long)
    //surface = CalcGreekSurface_Spread_Bull_Call(module, model, "v", array_s, k_l, k_h, r, q, v_l, v_h, array_t, is_long)
    //surface = CalcGreekSurface_Spread_Bull_Call(module, model, "t", array_s, k_l, k_h, r, q, v_l, v_h, array_t, is_long)
    surface = CalcGreekSurface_Spread_Bull_Call(module, model, "r", array_s, k_l, k_h, r, q, v_l, v_h, array_t, is_long)
    console.log(surface)
}

Test_DerivX_Vanilla_European()
