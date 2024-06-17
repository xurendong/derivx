/*
* Copyright (c) 2021-2024 the DerivX authors
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
// 1、演示美式香草期权隐含波动率、理论价格、希腊值、希腊值曲面等的计算（基于 BAW 公式）；
// 2、演示美式香草期权隐含波动率、理论价格、希腊值、希腊值曲面等的计算（基于二叉树方法）；
// 3、演示通过 Create 方法获取执行模块实例；
// 4、演示 直接模式 DirectCalc 任务执行调用；
// 5、演示任务参数序列化和任务结果反序列化的封装；

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

function Test_DerivX_Vanilla_American() {
    let result = 0.0
    let surface = []
    let kernel = new cyberx.Kernel(new syscfg.SysCfg()) // 全局唯一
    let module = new cyberx.Create('derivx_vanilla_american')
    
    //result = CalcIV(module, 'ba', 'v', 0.1566, 5.29, 6.0, 0.04, 0.0, 0.5, true) // Vega 法
    //result = CalcIV(module, 'ba', 'v', 0.7503, 5.29, 6.0, 0.04, 0.0, 0.5, false) // Vega 法
    //result = CalcIV(module, 'ba', 'b', 0.1566, 5.29, 6.0, 0.04, 0.0, 0.5, true) // Binary 法
    //result = CalcIV(module, 'ba', 'b', 0.7503, 5.29, 6.0, 0.04, 0.0, 0.5, false) // Binary 法
    //result = CalcIV(module, 'ba', 'n', 0.1566, 5.29, 6.0, 0.04, 0.0, 0.5, true) // Newton 法
    //result = CalcIV(module, 'ba', 'n', 0.7503, 5.29, 6.0, 0.04, 0.0, 0.5, false) // Newton 法
    //console.log(result)
    
    //result = CalcPrice(module, 'ba', 100.0, 100.0, 0.03, 0.08 - 0.03, 0.2, 1.0, true)
    //result = CalcPrice(module, 'ba', 42.0, 40.0, 0.1, 0.0, 0.2, 0.5, true)
    //result = CalcPrice(module, 'ba', 42.0, 40.0, 0.1, -0.01, 0.2, 0.5, true) // b >= r
    //result = CalcGreeks(module, 'ba', 'd', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, true)
    //result = CalcGreeks(module, 'ba', 'g', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreeks(module, 'ba', 'v', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreeks(module, 'ba', 't', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, true)
    //result = CalcGreeks(module, 'ba', 'r', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, true, false, false)
    //console.log(result)
    
    //result = CalcPrice(module, 'ba', 100.0, 100.0, 0.03, 0.08 + 0.03, 0.2, 1.0, false)
    //result = CalcPrice(module, 'ba', 42.0, 40.0, 0.1, 0.0, 0.2, 0.5, false)
    //result = CalcPrice(module, 'ba', 42.0, 40.0, 0.1, -0.01, 0.2, 0.5, false) // b >= r
    //result = CalcGreeks(module, 'ba', 'd', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, false)
    //result = CalcGreeks(module, 'ba', 'g', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreeks(module, 'ba', 'v', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreeks(module, 'ba', 't', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, false)
    //result = CalcGreeks(module, 'ba', 'r', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, false, false, false)
    //console.log(result)
    
    // 为使代码美观参数清晰，示例中二叉树节点层数通过 CalcIV、CalcPrice、CalcGreeks、CalcGreeksSurface 等函数的入参默认值设置
    
    //result = CalcIV(module, 'bt', 'v', 0.1566, 5.29, 6.0, 0.04, 0.0, 0.5, true) // Vega 法
    //result = CalcIV(module, 'bt', 'v', 0.7503, 5.29, 6.0, 0.04, 0.0, 0.5, false) // Vega 法
    //result = CalcIV(module, 'bt', 'b', 0.1566, 5.29, 6.0, 0.04, 0.0, 0.5, true) // Binary 法
    //result = CalcIV(module, 'bt', 'b', 0.7503, 5.29, 6.0, 0.04, 0.0, 0.5, false) // Binary 法
    //result = CalcIV(module, 'bt', 'n', 0.1566, 5.29, 6.0, 0.04, 0.0, 0.5, true) // Newton 法
    //result = CalcIV(module, 'bt', 'n', 0.7503, 5.29, 6.0, 0.04, 0.0, 0.5, false) // Newton 法
    //console.log(result)
    
    //result = CalcPrice(module, 'ba', 50.0, 50.0, 0.1, 0.03, 0.4, 0.4167, true)
    //console.log(result)
    //result = CalcPrice(module, 'bt', 50.0, 50.0, 0.1, 0.03, 0.4, 0.4167, true)
    //console.log(result)
    
    //result = CalcPrice(module, 'ba', 50.0, 50.0, 0.1, 0.03, 0.4, 0.4167, false)
    //console.log(result)
    //result = CalcPrice(module, 'bt', 50.0, 50.0, 0.1, 0.03, 0.4, 0.4167, false)
    //console.log(result)
    
    //result = CalcGreeks(module, 'ba', 'd', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, true)
    //result = CalcGreeks(module, 'ba', 'g', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreeks(module, 'ba', 'v', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreeks(module, 'ba', 't', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, true)
    //result = CalcGreeks(module, 'ba', 'r', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, true, false, false)
    //console.log(result)
    //result = CalcGreeks(module, 'bt', 'd', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, true)
    //result = CalcGreeks(module, 'bt', 'g', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreeks(module, 'bt', 'v', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreeks(module, 'bt', 't', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, true)
    //result = CalcGreeks(module, 'bt', 'r', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, true, false, false)
    //console.log(result)
    
    //result = CalcGreeks(module, 'ba', 'd', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, false)
    //result = CalcGreeks(module, 'ba', 'g', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreeks(module, 'ba', 'v', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreeks(module, 'ba', 't', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, false)
    //result = CalcGreeks(module, 'ba', 'r', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, false, false, false)
    //console.log(result)
    //result = CalcGreeks(module, 'bt', 'd', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, false)
    //result = CalcGreeks(module, 'bt', 'g', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreeks(module, 'bt', 'v', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true)
    //result = CalcGreeks(module, 'bt', 't', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, false)
    //result = CalcGreeks(module, 'bt', 'r', 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, true, false, false, false)
    //console.log(result)
    
    //let array_s = nj.arange(5.0, 105.0, 5.0).tolist()
    //let array_t = nj.arange(0.004, 1.004, 1.0 / 250).tolist()
    //let array_t = nj.arange(0.020, 1.020, 5.0 / 250).tolist() // 测试二叉树时建议减少计算时间点
    
    //surface = CalcGreeksSurface(module, 'ba', 'd', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, true)
    //surface = CalcGreeksSurface(module, 'ba', 'g', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true)
    //surface = CalcGreeksSurface(module, 'ba', 'v', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true)
    //surface = CalcGreeksSurface(module, 'ba', 't', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, true)
    //surface = CalcGreeksSurface(module, 'ba', 'r', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, true, false, false)
    //console.log(surface)
    //surface = CalcGreeksSurface(module, 'bt', 'd', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, true)
    //surface = CalcGreeksSurface(module, 'bt', 'g', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true)
    //surface = CalcGreeksSurface(module, 'bt', 'v', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true)
    //surface = CalcGreeksSurface(module, 'bt', 't', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, true)
    //surface = CalcGreeksSurface(module, 'bt', 'r', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, true, false, false)
    //console.log(surface)

    //surface = CalcGreeksSurface(module, 'ba', 'd', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, false)
    //surface = CalcGreeksSurface(module, 'ba', 'g', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true)
    //surface = CalcGreeksSurface(module, 'ba', 'v', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true)
    //surface = CalcGreeksSurface(module, 'ba', 't', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, false)
    //surface = CalcGreeksSurface(module, 'ba', 'r', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, false, false, false)
    //console.log(surface)
    //surface = CalcGreeksSurface(module, 'bt', 'd', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, false)
    //surface = CalcGreeksSurface(module, 'bt', 'g', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true)
    //surface = CalcGreeksSurface(module, 'bt', 'v', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true)
    //surface = CalcGreeksSurface(module, 'bt', 't', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, false)
    //surface = CalcGreeksSurface(module, 'bt', 'r', array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, false, false, false)
    //console.log(surface)
}

Test_DerivX_Vanilla_American()
