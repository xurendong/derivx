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

const derivx = require('derivx')

function Test_Vanilla_American() {
    let result = 0.0
    let vanilla = new derivx.Vanilla("American")
    
    // CalcPrice(model, s, k, r, q, v, t, is_call)
    // CalcGreeks(model, greek, s, k, r, q, v, t, is_long, is_call, is_futures, is_foreign)
    // CalcGreeksSurface(surface, model, greek, s, k, r, q, v, t, is_long, is_call, is_futures, is_foreign)
    
    console.log(vanilla.GetError())
}

Test_Vanilla_American()
