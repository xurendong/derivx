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

function Test_Vanilla_Spread_American() {
    let result = 0.0
    let vanilla_spread = new derivx.VanillaSpread("American")
    
    console.log(vanilla_spread.GetError())
}

Test_Vanilla_Spread_American()
