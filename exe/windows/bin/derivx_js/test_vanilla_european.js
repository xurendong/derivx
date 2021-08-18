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

function CalcPrice_Spread_Bull_Call(vanilla, model, s, k_l_c_l, k_h_c_s, r, q, sigma, t) {
    let price_low_call_long = vanilla.CalcPrice(model, s, k_l_c_l, r, q, sigma, t, true)
    let price_high_call_short = -vanilla.CalcPrice(model, s, k_h_c_s, r, q, sigma, t, true) // -
    return price_low_call_long + price_high_call_short
}

function CalcPrice_Spread_Bull_Put(vanilla, model, s, k_l_p_l, k_h_p_s, r, q, sigma, t) {
    let price_low_put_long = vanilla.CalcPrice(model, s, k_l_p_l, r, q, sigma, t, false)
    let price_high_put_short = -vanilla.CalcPrice(model, s, k_h_p_s, r, q, sigma, t, false) // -
    return price_low_put_long + price_high_put_short
}

function CalcPrice_Spread_Bear_Call(vanilla, model, s, k_l_c_s, k_h_c_l, r, q, sigma, t) {
    let price_low_call_short = -vanilla.CalcPrice(model, s, k_l_c_s, r, q, sigma, t, true) // -
    let price_high_call_long = vanilla.CalcPrice(model, s, k_h_c_l, r, q, sigma, t, true)
    return price_low_call_short + price_high_call_long
}

function CalcPrice_Spread_Bear_Put(vanilla, model, s, k_l_p_s, k_h_p_l, r, q, sigma, t) {
    let price_low_put_short = -vanilla.CalcPrice(model, s, k_l_p_s, r, q, sigma, t, false) // -
    let price_high_put_long = vanilla.CalcPrice(model, s, k_h_p_l, r, q, sigma, t, false)
    return price_low_put_short + price_high_put_long
}

function CalcPrice_Spread_Butterfly_Call(vanilla, model, s, k_l_c_l, k_m_c_s, k_h_c_l, r, q, sigma, t) {
    let price_low_call_long = vanilla.CalcPrice(model, s, k_l_c_l, r, q, sigma, t, true)
    let price_middle_call_short = -vanilla.CalcPrice(model, s, k_m_c_s, r, q, sigma, t, true) * 2 // - // * 2
    let price_high_call_long = vanilla.CalcPrice(model, s, k_h_c_l, r, q, sigma, t, true)
    return price_low_call_long + price_middle_call_short + price_high_call_long
}

function CalcPrice_Spread_Butterfly_Put(vanilla, model, s, k_l_p_l, k_m_p_s, k_h_p_l, r, q, sigma, t) {
    let price_low_put_long = vanilla.CalcPrice(model, s, k_l_p_l, r, q, sigma, t, false)
    let price_middle_put_short = -vanilla.CalcPrice(model, s, k_m_p_s, r, q, sigma, t, false) * 2 // - // * 2
    let price_high_put_long = vanilla.CalcPrice(model, s, k_h_p_l, r, q, sigma, t, false)
    return price_low_put_long + price_middle_put_short + price_high_put_long
}

function CalcPrice_Spread_Box_Bull_Call_Bear_Put(vanilla, model, s, k_l_cp_ls, k_h_cp_sl, r, q, sigma, t) {
    let price_bull_call = CalcPrice_Spread_Bull_Call(vanilla, model, s, k_l_cp_ls, k_h_cp_sl, r, q, sigma, t)
    let price_bear_put = CalcPrice_Spread_Bear_Put(vanilla, model, s, k_l_cp_ls, k_h_cp_sl, r, q, sigma, t)
    return price_bull_call + price_bear_put
}

function CalcPrice_Spread_Box_Bull_Put_Bear_Call(vanilla, model, s, k_l_pc_ls, k_h_pc_sl, r, q, sigma, t) {
    let price_bull_put = CalcPrice_Spread_Bull_Put(vanilla, model, s, k_l_pc_ls, k_h_pc_sl, r, q, sigma, t)
    let price_bear_call = CalcPrice_Spread_Bear_Call(vanilla, model, s, k_l_pc_ls, k_h_pc_sl, r, q, sigma, t)
    return price_bull_put + price_bear_call
}

function CalcGreeks_Spread_Bull_Call(vanilla, model, greek, s, k_l_c_l, k_h_c_s, r, q, sigma, t) {
    if(model === "bs") {
        if(greek === "d") {
            let delta_low_call_long = vanilla.CalcGreeks(model, greek, s, k_l_c_l, r, q, sigma, t, true)
            let delta_high_call_short = -vanilla.CalcGreeks(model, greek, s, k_h_c_s, r, q, sigma, t, true) // -
            return delta_low_call_long + delta_high_call_short
        }
        else if(greek === "g") {
            let gamma_low_call_long = vanilla.CalcGreeks(model, greek, s, k_l_c_l, r, q, sigma, t)
            let gamma_high_call_short = -vanilla.CalcGreeks(model, greek, s, k_h_c_s, r, q, sigma, t) // -
            return gamma_low_call_long + gamma_high_call_short
        }
        else if(greek === "v") {
            let vega_low_call_long = vanilla.CalcGreeks(model, greek, s, k_l_c_l, r, q, sigma, t)
            let vega_high_call_short = -vanilla.CalcGreeks(model, greek, s, k_h_c_s, r, q, sigma, t) // -
            return vega_low_call_long + vega_high_call_short
        }
        else if(greek === "t") {
            let theta_low_call_long = vanilla.CalcGreeks(model, greek, s, k_l_c_l, r, q, sigma, t, true)
            let theta_high_call_short = -vanilla.CalcGreeks(model, greek, s, k_h_c_s, r, q, sigma, t, true) // -
            return theta_low_call_long + theta_high_call_short
        }
        else if(greek === "r") {
            let rho_low_call_long = vanilla.CalcGreeks(model, greek, s, k_l_c_l, r, q, sigma, t, true, false, false)
            let rho_high_call_short = -vanilla.CalcGreeks(model, greek, s, k_h_c_s, r, q, sigma, t, true, false, false) // -
            return rho_low_call_long + rho_high_call_short
        }
    }
    return 0.0
}

function CalcGreeksSurface_Spread_Bull_Call(vanilla, model, greek, array_s, k_l_c_l, k_h_c_s, r, q, sigma, array_t) {
    let surface_low_call_long = nj.zeros([array_s.length, array_t.length]).tolist()
    let surface_high_call_short = nj.zeros([array_s.length, array_t.length]).tolist()
    if(model === "bs") {
        if(greek === "d") {
            vanilla.CalcGreeksSurface(surface_low_call_long, model, greek, array_s, k_l_c_l, r, q, sigma, array_t, true)
            vanilla.CalcGreeksSurface(surface_high_call_short, model, greek, array_s, k_h_c_s, r, q, sigma, array_t, true)
            surface_low_call_long = nj.array(surface_low_call_long, "float64")
            surface_high_call_short = nj.array(surface_high_call_short, "float64")
            return surface_low_call_long.subtract(surface_high_call_short, false) // -
        }
        else if(greek === "g") {
            vanilla.CalcGreeksSurface(surface_low_call_long, model, greek, array_s, k_l_c_l, r, q, sigma, array_t)
            vanilla.CalcGreeksSurface(surface_high_call_short, model, greek, array_s, k_h_c_s, r, q, sigma, array_t)
            surface_low_call_long = nj.array(surface_low_call_long, "float64")
            surface_high_call_short = nj.array(surface_high_call_short, "float64")
            return surface_low_call_long.subtract(surface_high_call_short, false) // -
        }
        else if(greek === "v") {
            vanilla.CalcGreeksSurface(surface_low_call_long, model, greek, array_s, k_l_c_l, r, q, sigma, array_t)
            vanilla.CalcGreeksSurface(surface_high_call_short, model, greek, array_s, k_h_c_s, r, q, sigma, array_t)
            surface_low_call_long = nj.array(surface_low_call_long, "float64")
            surface_high_call_short = nj.array(surface_high_call_short, "float64")
            return surface_low_call_long.subtract(surface_high_call_short, false) // -
        }
        else if(greek === "t") {
            vanilla.CalcGreeksSurface(surface_low_call_long, model, greek, array_s, k_l_c_l, r, q, sigma, array_t, true)
            vanilla.CalcGreeksSurface(surface_high_call_short, model, greek, array_s, k_h_c_s, r, q, sigma, array_t, true)
            surface_low_call_long = nj.array(surface_low_call_long, "float64")
            surface_high_call_short = nj.array(surface_high_call_short, "float64")
            return surface_low_call_long.subtract(surface_high_call_short, false) // -
        }
        else if(greek === "r") {
            vanilla.CalcGreeksSurface(surface_low_call_long, model, greek, array_s, k_l_c_l, r, q, sigma, array_t, true, false, false)
            vanilla.CalcGreeksSurface(surface_high_call_short, model, greek, array_s, k_h_c_s, r, q, sigma, array_t, true, false, false)
            surface_low_call_long = nj.array(surface_low_call_long, "float64")
            surface_high_call_short = nj.array(surface_high_call_short, "float64")
            return surface_low_call_long.subtract(surface_high_call_short, false) // -
        }
    }
    return nj.zeros([array_s.length, array_t.length]).tolist()
}

function Test_Vanilla_European() {
    let result = 0.0
    let vanilla = new derivx.Vanilla("European")
    
    // CalcPrice(model, s, k, r, q, sigma, t, is_call)
    // CalcGreeks(model, greek, s, k, r, q, sigma, t, is_call, is_futures, is_foreign)
    // CalcGreeksSurface(surface, model, greek, s, k, r, q, sigma, t, is_call, is_futures, is_foreign)
    
    //result = vanilla.CalcPrice("bs", 100.0, 100.0, 0.03, 0.085 - 0.03, 0.15, 1.0, true)
    //result = vanilla.CalcPrice("bs", 42.0, 40.0, 0.1, 0.0, 0.2, 0.5, true)
    //result = vanilla.CalcGreeks("bs", "d", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = vanilla.CalcGreeks("bs", "g", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846)
    //result = vanilla.CalcGreeks("bs", "v", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846)
    //result = vanilla.CalcGreeks("bs", "t", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = vanilla.CalcGreeks("bs", "r", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, false, false)
    //console.log(result)
    
    //result = vanilla.CalcPrice("bs", 100.0, 100.0, 0.03, 0.085 + 0.03, 0.15, 1.0, false)
    //result = vanilla.CalcPrice("bs", 42.0, 40.0, 0.1, 0.0, 0.2, 0.5, false)
    //result = vanilla.CalcGreeks("bs", "d", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, false)
    //result = vanilla.CalcGreeks("bs", "g", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846)
    //result = vanilla.CalcGreeks("bs", "v", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846)
    //result = vanilla.CalcGreeks("bs", "t", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, false)
    //result = vanilla.CalcGreeks("bs", "r", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, false, false, false)
    //console.log(result)
    
    //let array_s = nj.arange(5.0, 105.0, 5.0).tolist()
    //let array_t = nj.arange(0.004, 1.004, 1.0 / 250).tolist()
    //let surface = nj.zeros([array_s.length, array_t.length]).tolist()
    
    //vanilla.CalcGreeksSurface(surface, "bs", "d", array_s, 50.0, 0.05, 0.0, 0.2, array_t, true)
    //vanilla.CalcGreeksSurface(surface, "bs", "g", array_s, 50.0, 0.05, 0.0, 0.2, array_t)
    //vanilla.CalcGreeksSurface(surface, "bs", "v", array_s, 50.0, 0.05, 0.0, 0.2, array_t)
    //vanilla.CalcGreeksSurface(surface, "bs", "t", array_s, 50.0, 0.05, 0.0, 0.2, array_t, true)
    //vanilla.CalcGreeksSurface(surface, "bs", "r", array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, false, false)
    //console.log(surface)
    
    //vanilla.CalcGreeksSurface(surface, "bs", "d", array_s, 50.0, 0.05, 0.0, 0.2, array_t, false)
    //vanilla.CalcGreeksSurface(surface, "bs", "g", array_s, 50.0, 0.05, 0.0, 0.2, array_t)
    //vanilla.CalcGreeksSurface(surface, "bs", "v", array_s, 50.0, 0.05, 0.0, 0.2, array_t)
    //vanilla.CalcGreeksSurface(surface, "bs", "t", array_s, 50.0, 0.05, 0.0, 0.2, array_t, false)
    //vanilla.CalcGreeksSurface(surface, "bs", "r", array_s, 50.0, 0.05, 0.0, 0.2, array_t, false, false, false)
    //console.log(surface)
    
    let array_s = nj.arange(5.0, 105.0, 5.0).tolist()
    let array_t = nj.arange(0.004, 1.004, 1.0 / 250).tolist()
    let model = "bs", s = 50.0, k_l = 40.0, k_m = 50.0, k_h = 60.0, r = 0.05, q = 0.0, sigma = 0.2, t = 0.5
    //console.log(CalcPrice_Spread_Bull_Call(vanilla, model, s, k_l, k_h, r, q, sigma, t))
    //console.log(CalcPrice_Spread_Bull_Put(vanilla, model, s, k_l, k_h, r, q, sigma, t))
    //console.log(CalcPrice_Spread_Bear_Call(vanilla, model, s, k_l, k_h, r, q, sigma, t))
    //console.log(CalcPrice_Spread_Bear_Put(vanilla, model, s, k_l, k_h, r, q, sigma, t))
    //console.log(CalcPrice_Spread_Butterfly_Call(vanilla, model, s, k_l, k_m, k_h, r, q, sigma, t))
    //console.log(CalcPrice_Spread_Butterfly_Put(vanilla, model, s, k_l, k_m, k_h, r, q, sigma, t))
    //console.log(CalcPrice_Spread_Box_Bull_Call_Bear_Put(vanilla, model, s, k_l, k_h, r, q, sigma, t))
    //console.log(CalcPrice_Spread_Box_Bull_Put_Bear_Call(vanilla, model, s, k_l, k_h, r, q, sigma, t))
    //console.log(CalcGreeks_Spread_Bull_Call(vanilla, model, "d", s, k_l, k_h, r, q, sigma, t))
    //console.log(CalcGreeks_Spread_Bull_Call(vanilla, model, "g", s, k_l, k_h, r, q, sigma, t))
    //console.log(CalcGreeks_Spread_Bull_Call(vanilla, model, "v", s, k_l, k_h, r, q, sigma, t))
    //console.log(CalcGreeks_Spread_Bull_Call(vanilla, model, "t", s, k_l, k_h, r, q, sigma, t))
    //console.log(CalcGreeks_Spread_Bull_Call(vanilla, model, "r", s, k_l, k_h, r, q, sigma, t))
    //let surface = CalcGreeksSurface_Spread_Bull_Call(vanilla, model, "d", array_s, k_l, k_h, r, q, sigma, array_t)
    //let surface = CalcGreeksSurface_Spread_Bull_Call(vanilla, model, "g", array_s, k_l, k_h, r, q, sigma, array_t)
    //let surface = CalcGreeksSurface_Spread_Bull_Call(vanilla, model, "v", array_s, k_l, k_h, r, q, sigma, array_t)
    //let surface = CalcGreeksSurface_Spread_Bull_Call(vanilla, model, "t", array_s, k_l, k_h, r, q, sigma, array_t)
    let surface = CalcGreeksSurface_Spread_Bull_Call(vanilla, model, "r", array_s, k_l, k_h, r, q, sigma, array_t)
    console.log(surface)
    
    console.log(vanilla.GetError())
}

Test_Vanilla_European()
