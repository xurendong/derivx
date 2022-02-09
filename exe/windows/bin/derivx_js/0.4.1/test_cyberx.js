/*
* Copyright (c) 2021-2022 the CyberX authors
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

const syscfg = require('./syscfg')
const cyberx = require('cyberx') // cyberx-js

console.log(cyberx.Version())

let g_syscfg = new syscfg.SysCfg()
let g_kernel = new cyberx.Kernel(g_syscfg) // 全局唯一 // 全局会析构

function OnResult() {
    let [flag, task, unit, func, form, code, info, data] = Array.from(arguments)
    console.log("TestAsync Callback OnResult:", flag, task, unit, func, form, code, info, data)
}

function Test_Kernel_Object() {
    //let g_syscfg = new syscfg.SysCfg()
    //let g_kernel = new cyberx.Kernel(g_syscfg) // 全局唯一 // 局部会析构
    
    for(let i = 0; i < 10; i++) {
        console.log(g_kernel.Test())
    }
    
    let obj_req = {'type_int':123, 'type_bool':true, 'type_double':123.456, 'type_string':'cyberx'}
    let msg_req = JSON.stringify(obj_req)
    let msg_ans = g_kernel.TestJson(msg_req)
    let obj_ans = JSON.parse(msg_ans)
    console.log('obj_req:', obj_req)
    console.log('msg_req:', msg_req)
    console.log('msg_ans:', msg_ans)
    console.log('obj_ans:', obj_ans)
    
    g_kernel.TestAsync(OnResult)
    g_kernel.TestAsync(OnResult)
}

Test_Kernel_Object()
