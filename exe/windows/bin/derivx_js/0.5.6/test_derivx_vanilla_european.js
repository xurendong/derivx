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
// 1、演示欧式香草期权隐含波动率、理论价格、希腊值、希腊值曲面等的计算（基于 BS 公式）；
// 2、演示欧式香草期权隐含波动率、理论价格、希腊值、希腊值曲面等的计算（基于二叉树方法）；
// 3、演示欧式香草期权组合理论价格、希腊值、希腊值曲面等的计算；
// 4、演示通过 Create 方法获取执行模块实例；
// 5、演示 直接模式 DirectCalc 任务执行调用；
// 6、演示任务参数序列化和任务结果反序列化的封装；

'use strict'

const nj = require('numjs')

const syscfg = require('./syscfg')
const cyberx = require('cyberx') // cyberx-js

let func_calc_iv             = 1
let func_calc_price          = 2
let func_calc_greeks         = 3
let func_calc_greeks_surface = 4

function CalcIV(module, model, method, p, s, k, r, q, t, is_call, tree_step = 10000) {
    let inputs = {'model':model, 'method':method, 'p':p, 's':s, 'k':k, 'r':r, 'q':q, 't':t, 'is_call':is_call, 'tree_step':tree_step}
    let result = JSON.parse(module.DirectCalc(func_calc_iv, 0, JSON.stringify(inputs)))
    if(result['return_code'] !== 0) {
        console.log(result['return_code'], result['return_info'])
    }
    return result['result_data']
}

function CalcPrice(module, model, s, k, r, q, v, t, is_call, tree_step = 10000) {
    let inputs = {'model':model, 's':s, 'k':k, 'r':r, 'q':q, 'v':v, 't':t, 'is_call':is_call, 'tree_step':tree_step}
    let result = JSON.parse(module.DirectCalc(func_calc_price, 0, JSON.stringify(inputs)))
    if(result['return_code'] !== 0) {
        console.log(result['return_code'], result['return_info'])
    }
    return result['result_data']
}

function CalcGreeks(module, model, greek, s, k, r, q, v, t, is_long = true, is_call = true, is_futures = false, is_foreign = false, tree_step = 10000) {
    let inputs = {'model':model, 'greek':greek, 's':s, 'k':k, 'r':r, 'q':q, 'v':v, 't':t, 'is_long':is_long, 'is_call':is_call, 'is_futures':is_futures, 'is_foreign':is_foreign, 'tree_step':tree_step}
    let result = JSON.parse(module.DirectCalc(func_calc_greeks, 0, JSON.stringify(inputs)))
    if(result['return_code'] !== 0) {
        console.log(result['return_code'], result['return_info'])
    }
    return result['result_data']
}

function CalcGreeksSurface(module, model, greek, array_s, k, r, q, v, array_t, is_long = true, is_call = true, is_futures = false, is_foreign = false, tree_step = 10000) {
    let inputs = {'model':model, 'greek':greek, 'array_s':array_s, 'k':k, 'r':r, 'q':q, 'v':v, 'array_t':array_t, 'is_long':is_long, 'is_call':is_call, 'is_futures':is_futures, 'is_foreign':is_foreign, 'tree_step':tree_step}
    let result = JSON.parse(module.DirectCalc(func_calc_greeks_surface, 0, JSON.stringify(inputs)))
    if(result['return_code'] !== 0) {
        console.log(result['return_code'], result['return_info'])
    }
    return result['result_data']
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

function CalcGreeks_Spread_Bull_Call(module, model, greek, s, k_l_c_l, k_h_c_s, r, q, v_l_c_l, v_h_c_s, t, is_long) {
    let result = 0.0
    if(model === "bs") {
        if(greek === "d") {
            let delta_low_call_long = CalcGreeks(module, model, greek, s, k_l_c_l, r, q, v_l_c_l, t, true, true)
            let delta_high_call_short = CalcGreeks(module, model, greek, s, k_h_c_s, r, q, v_h_c_s, t, false, true)
            result = delta_low_call_long + delta_high_call_short
        }
        else if(greek === "g") {
            let gamma_low_call_long = CalcGreeks(module, model, greek, s, k_l_c_l, r, q, v_l_c_l, t, true)
            let gamma_high_call_short = CalcGreeks(module, model, greek, s, k_h_c_s, r, q, v_h_c_s, t, false)
            result = gamma_low_call_long + gamma_high_call_short
        }
        else if(greek === "v") {
            let vega_low_call_long = CalcGreeks(module, model, greek, s, k_l_c_l, r, q, v_l_c_l, t, true)
            let vega_high_call_short = CalcGreeks(module, model, greek, s, k_h_c_s, r, q, v_h_c_s, t, false)
            result = vega_low_call_long + vega_high_call_short
        }
        else if(greek === "t") {
            let theta_low_call_long = CalcGreeks(module, model, greek, s, k_l_c_l, r, q, v_l_c_l, t, true, true)
            let theta_high_call_short = CalcGreeks(module, model, greek, s, k_h_c_s, r, q, v_h_c_s, t, false, true)
            result = theta_low_call_long + theta_high_call_short
        }
        else if(greek === "r") {
            let rho_low_call_long = CalcGreeks(module, model, greek, s, k_l_c_l, r, q, v_l_c_l, t, true, true, false, false)
            let rho_high_call_short = CalcGreeks(module, model, greek, s, k_h_c_s, r, q, v_h_c_s, t, false, true, false, false)
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

function CalcGreeksSurface_Spread_Bull_Call(module, model, greek, array_s, k_l_c_l, k_h_c_s, r, q, v_l_c_l, v_h_c_s, array_t, is_long) {
    let surface_low_call_long = nj.zeros([array_s.length, array_t.length]).tolist()
    let surface_high_call_short = nj.zeros([array_s.length, array_t.length]).tolist()
    if(model === "bs") {
        if(greek === "d") {
            surface_low_call_long = CalcGreeksSurface(module, model, greek, array_s, k_l_c_l, r, q, v_l_c_l, array_t, true, true)
            surface_high_call_short = CalcGreeksSurface(module, model, greek, array_s, k_h_c_s, r, q, v_h_c_s, array_t, false, true)
        }
        else if(greek === "g") {
            surface_low_call_long = CalcGreeksSurface(module, model, greek, array_s, k_l_c_l, r, q, v_l_c_l, array_t, true)
            surface_high_call_short = CalcGreeksSurface(module, model, greek, array_s, k_h_c_s, r, q, v_h_c_s, array_t, false)
        }
        else if(greek === "v") {
            surface_low_call_long = CalcGreeksSurface(module, model, greek, array_s, k_l_c_l, r, q, v_l_c_l, array_t, true)
            surface_high_call_short = CalcGreeksSurface(module, model, greek, array_s, k_h_c_s, r, q, v_h_c_s, array_t, false)
        }
        else if(greek === "t") {
            surface_low_call_long = CalcGreeksSurface(module, model, greek, array_s, k_l_c_l, r, q, v_l_c_l, array_t, true, true)
            surface_high_call_short = CalcGreeksSurface(module, model, greek, array_s, k_h_c_s, r, q, v_h_c_s, array_t, false, true)
        }
        else if(greek === "r") {
            surface_low_call_long = CalcGreeksSurface(module, model, greek, array_s, k_l_c_l, r, q, v_l_c_l, array_t, true, true, false, false)
            surface_high_call_short = CalcGreeksSurface(module, model, greek, array_s, k_h_c_s, r, q, v_h_c_s, array_t, false, true, false, false)
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
    
    //result = CalcIV(module, 'bs', 'v', 0.1566, 5.29, 6.0, 0.04, 0.0, 0.5, true) // Vega 法
    //result = CalcIV(module, 'bs', 'v', 0.7503, 5.29, 6.0, 0.04, 0.0, 0.5, false) // Vega 法
    //result = CalcIV(module, 'bs', 'b', 0.1566, 5.29, 6.0, 0.04, 0.0, 0.5, true) // Binary 法
    //result = CalcIV(module, 'bs', 'b', 0.7503, 5.29, 6.0, 0.04, 0.0, 0.5, false) // Binary 法
    //result = CalcIV(module, 'bs', 'n', 0.1566, 5.29, 6.0, 0.04, 0.0, 0.5, true) // Newton 法
    //result = CalcIV(module, 'bs', 'n', 0.7503, 5.29, 6.0, 0.04, 0.0, 0.5, false) // Newton 法
    //console.log(result)
    
    //result = CalcPrice(module, 'bs', 100.0, 100.0, 0.03, 0.085 - 0.03, 0.15, 1.0, true)
    //result = CalcPrice(module, 'bs', 42.0, 40.0, 0.1, 0.0, 0.2, 0.5, true)
    //result = CalcGreeks(module, 'bs', 'd', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, true)
    //result = CalcGreeks(module, 'bs', 'g', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreeks(module, 'bs', 'v', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreeks(module, 'bs', 't', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, true)
    //result = CalcGreeks(module, 'bs', 'r', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, true, false, false)
    //console.log(result)
    
    //result = CalcPrice(module, 'bs', 100.0, 100.0, 0.03, 0.085 + 0.03, 0.15, 1.0, false)
    //result = CalcPrice(module, 'bs', 42.0, 40.0, 0.1, 0.0, 0.2, 0.5, false)
    //result = CalcGreeks(module, 'bs', 'd', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, false)
    //result = CalcGreeks(module, 'bs', 'g', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreeks(module, 'bs', 'v', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreeks(module, 'bs', 't', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, false)
    //result = CalcGreeks(module, 'bs', 'r', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, false, false, false)
    //console.log(result)
    
    // 为使代码美观参数清晰，示例中二叉树节点层数通过 CalcIV、CalcPrice、CalcGreeks、CalcGreeksSurface 等函数的入参默认值设置
    
    //result = CalcIV(module, 'bt', 'v', 0.1566, 5.29, 6.0, 0.04, 0.0, 0.5, true) // Vega 法
    //result = CalcIV(module, 'bt', 'v', 0.7503, 5.29, 6.0, 0.04, 0.0, 0.5, false) // Vega 法
    //result = CalcIV(module, 'bt', 'b', 0.1566, 5.29, 6.0, 0.04, 0.0, 0.5, true) // Binary 法
    //result = CalcIV(module, 'bt', 'b', 0.7503, 5.29, 6.0, 0.04, 0.0, 0.5, false) // Binary 法
    //result = CalcIV(module, 'bt', 'n', 0.1566, 5.29, 6.0, 0.04, 0.0, 0.5, true) // Newton 法
    //result = CalcIV(module, 'bt', 'n', 0.7503, 5.29, 6.0, 0.04, 0.0, 0.5, false) // Newton 法
    //console.log(result)
    
    //result = CalcPrice(module, 'bs', 50.0, 50.0, 0.1, 0.03, 0.4, 0.4167, true)
    //console.log(result)
    //result = CalcPrice(module, 'bt', 50.0, 50.0, 0.1, 0.03, 0.4, 0.4167, true)
    //console.log(result)
    
    //result = CalcPrice(module, 'bs', 50.0, 50.0, 0.1, 0.03, 0.4, 0.4167, false)
    //console.log(result)
    //result = CalcPrice(module, 'bt', 50.0, 50.0, 0.1, 0.03, 0.4, 0.4167, false)
    //console.log(result)
    
    //result = CalcGreeks(module, 'bs', 'd', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, true)
    //result = CalcGreeks(module, 'bs', 'g', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreeks(module, 'bs', 'v', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreeks(module, 'bs', 't', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, true)
    //result = CalcGreeks(module, 'bs', 'r', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, true, false, false)
    //console.log(result)
    //result = CalcGreeks(module, 'bt', 'd', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, true)
    //result = CalcGreeks(module, 'bt', 'g', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreeks(module, 'bt', 'v', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreeks(module, 'bt', 't', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, true)
    //result = CalcGreeks(module, 'bt', 'r', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, true, false, false) // 目前对 futures 和 foreign 无效
    //console.log(result)
    
    //result = CalcGreeks(module, 'bs', 'd', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, false)
    //result = CalcGreeks(module, 'bs', 'g', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreeks(module, 'bs', 'v', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreeks(module, 'bs', 't', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, false)
    //result = CalcGreeks(module, 'bs', 'r', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, false, false, false)
    //console.log(result)
    //result = CalcGreeks(module, 'bt', 'd', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, false)
    //result = CalcGreeks(module, 'bt', 'g', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreeks(module, 'bt', 'v', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreeks(module, 'bt', 't', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, false)
    //result = CalcGreeks(module, 'bt', 'r', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, false, false, false) // 目前对 futures 和 foreign 无效
    //console.log(result)
    
    //let array_s = nj.arange(5.0, 105.0, 5.0).tolist()
    //let array_t = nj.arange(0.004, 1.004, 1.0 / 250).tolist()
    //let array_t = nj.arange(0.020, 1.020, 5.0 / 250).tolist() // 测试二叉树时建议减少计算时间点
    
    //surface = CalcGreeksSurface(module, 'bs', 'd', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, true)
    //surface = CalcGreeksSurface(module, 'bs', 'g', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true)
    //surface = CalcGreeksSurface(module, 'bs', 'v', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true)
    //surface = CalcGreeksSurface(module, 'bs', 't', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, true)
    //surface = CalcGreeksSurface(module, 'bs', 'r', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, true, false, false)
    //console.log(surface)
    //surface = CalcGreeksSurface(module, 'bt', 'd', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, true)
    //surface = CalcGreeksSurface(module, 'bt', 'g', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true)
    //surface = CalcGreeksSurface(module, 'bt', 'v', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true)
    //surface = CalcGreeksSurface(module, 'bt', 't', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, true)
    //surface = CalcGreeksSurface(module, 'bt', 'r', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, true, false, false)
    //console.log(surface)
    
    //surface = CalcGreeksSurface(module, 'bs', 'd', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, false)
    //surface = CalcGreeksSurface(module, 'bs', 'g', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true)
    //surface = CalcGreeksSurface(module, 'bs', 'v', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true)
    //surface = CalcGreeksSurface(module, 'bs', 't', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, false)
    //surface = CalcGreeksSurface(module, 'bs', 'r', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, false, false, false)
    //console.log(surface)
    //surface = CalcGreeksSurface(module, 'bt', 'd', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, false)
    //surface = CalcGreeksSurface(module, 'bt', 'g', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true)
    //surface = CalcGreeksSurface(module, 'bt', 'v', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true)
    //surface = CalcGreeksSurface(module, 'bt', 't', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, false)
    //surface = CalcGreeksSurface(module, 'bt', 'r', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, false, false, false)
    //console.log(surface)
    
    //let array_s = nj.arange(5.0, 105.0, 5.0).tolist()
    //let array_t = nj.arange(0.004, 1.004, 1.0 / 250).tolist()
    //let model = "bs", s = 50.0, k_l = 40.0, k_m = 50.0, k_h = 60.0, r = 0.05, q = 0.0, v_l = 0.2, v_m = 0.2, v_h = 0.2, t = 0.5, is_long = true
    //console.log(CalcPrice_Spread_Bull_Call(module, model, s, k_l, k_h, r, q, v_l, v_h, t))
    //console.log(CalcPrice_Spread_Bull_Put(module, model, s, k_l, k_h, r, q, v_l, v_h, t))
    //console.log(CalcPrice_Spread_Bear_Call(module, model, s, k_l, k_h, r, q, v_l, v_h, t))
    //console.log(CalcPrice_Spread_Bear_Put(module, model, s, k_l, k_h, r, q, v_l, v_h, t))
    //console.log(CalcPrice_Spread_Butterfly_Call(module, model, s, k_l, k_m, k_h, r, q, v_l, v_m, v_h, t))
    //console.log(CalcPrice_Spread_Butterfly_Put(module, model, s, k_l, k_m, k_h, r, q, v_l, v_m, v_h, t))
    //console.log(CalcPrice_Spread_Box_Bull_Call_Bear_Put(module, model, s, k_l, k_h, r, q, v_l, v_h, t))
    //console.log(CalcPrice_Spread_Box_Bull_Put_Bear_Call(module, model, s, k_l, k_h, r, q, v_l, v_h, t))
    //console.log(CalcGreeks_Spread_Bull_Call(module, model, "d", s, k_l, k_h, r, q, v_l, v_h, t, is_long))
    //console.log(CalcGreeks_Spread_Bull_Call(module, model, "g", s, k_l, k_h, r, q, v_l, v_h, t, is_long))
    //console.log(CalcGreeks_Spread_Bull_Call(module, model, "v", s, k_l, k_h, r, q, v_l, v_h, t, is_long))
    //console.log(CalcGreeks_Spread_Bull_Call(module, model, "t", s, k_l, k_h, r, q, v_l, v_h, t, is_long))
    //console.log(CalcGreeks_Spread_Bull_Call(module, model, "r", s, k_l, k_h, r, q, v_l, v_h, t, is_long))
    //surface = CalcGreeksSurface_Spread_Bull_Call(module, model, "d", array_s, k_l, k_h, r, q, v_l, v_h, array_t, is_long)
    //surface = CalcGreeksSurface_Spread_Bull_Call(module, model, "g", array_s, k_l, k_h, r, q, v_l, v_h, array_t, is_long)
    //surface = CalcGreeksSurface_Spread_Bull_Call(module, model, "v", array_s, k_l, k_h, r, q, v_l, v_h, array_t, is_long)
    //surface = CalcGreeksSurface_Spread_Bull_Call(module, model, "t", array_s, k_l, k_h, r, q, v_l, v_h, array_t, is_long)
    //surface = CalcGreeksSurface_Spread_Bull_Call(module, model, "r", array_s, k_l, k_h, r, q, v_l, v_h, array_t, is_long)
    //console.log(surface)
}

Test_DerivX_Vanilla_European()
