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
    
    let array_s = nj.arange(5.0, 105.0, 5.0).tolist()
    let array_t = nj.arange(0.004, 1.004, 1.0 / 250).tolist()
    let surface = nj.zeros([array_s.length, array_t.length]).tolist()
    
    vanilla.CalcGreeksSurface(surface, "bs", "d", array_s, 50.0, 0.05, 0.0, 0.2, array_t, true)
    //vanilla.CalcGreeksSurface(surface, "bs", "g", array_s, 50.0, 0.05, 0.0, 0.2, array_t)
    //vanilla.CalcGreeksSurface(surface, "bs", "v", array_s, 50.0, 0.05, 0.0, 0.2, array_t)
    //vanilla.CalcGreeksSurface(surface, "bs", "t", array_s, 50.0, 0.05, 0.0, 0.2, array_t, true)
    //vanilla.CalcGreeksSurface(surface, "bs", "r", array_s, 50.0, 0.05, 0.0, 0.2, array_t, true, false, false)
    console.log(surface)
    
    vanilla.CalcGreeksSurface(surface, "bs", "d", array_s, 50.0, 0.05, 0.0, 0.2, array_t, false)
    //vanilla.CalcGreeksSurface(surface, "bs", "g", array_s, 50.0, 0.05, 0.0, 0.2, array_t)
    //vanilla.CalcGreeksSurface(surface, "bs", "v", array_s, 50.0, 0.05, 0.0, 0.2, array_t)
    //vanilla.CalcGreeksSurface(surface, "bs", "t", array_s, 50.0, 0.05, 0.0, 0.2, array_t, false)
    //vanilla.CalcGreeksSurface(surface, "bs", "r", array_s, 50.0, 0.05, 0.0, 0.2, array_t, false, false, false)
    console.log(surface)
    
    console.log(vanilla.GetError())
}

Test_Vanilla_European()
