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
// 1、测试远程执行调用

'use strict'

// 使用 timers/promises 的 setTimeout 要求 Node 版本为 15.0.0 及以上
// 以后可以用 timers/promises 的 scheduler.wait 代替，要求 Node 版本为 17.3.0 及以上
const promises = require('timers/promises')

const nj = require('numjs')

const syscfg = require('./syscfg')
const tasker = require('./tasker')
const cyberx = require('cyberx') // cyberx-js

let func_make_data_gbm = 1

let event_task_finish = null // AbortController

class Config {
    constructor() {
        this.rand_rows = 10 // 随机数据行数
        this.rand_cols = 50 // 随机数据列数
        this.dimension = 0 // 随机数据维度 // 未使用
        this.rand_seed = [0, 1, 2, 3, 4, 5, 6, 7] // 随机数据种子 // 非负整数，有效位数不超逻辑处理器数量
        this.runs_size = 10 // 模拟路径数量
        this.runs_step = 50 // 价格变动步数
        this.year_days = 244 // 年交易日数量
        this.price = 1.0 // 初始价格
        this.sigma = 0.2 // 波动率
        this.risk_free_rate = 0.03 // 无风险利率
        this.basis_rate = 0.0 // 股息率或贴水率
    }
    
    ToJson() {
        return JSON.stringify(this)
    }
}

function OnResult_Remote() {
    try {
        let [result] = Array.from(arguments)
        //console.log("Callback OnResult_Remote:", result)
        if(result['return_code'] !== 0) {
            console.log(result['return_code'], result['return_info'])
        }
        else {
            result = JSON.parse(result['result_data'])
            console.log('result:', result)
        }
    }
    catch(error) {
        console.log('OnResult_Remote 异常！' + error)
    }
    event_task_finish.abort() //
}

async function Test_Remote() {
    let kernel = new cyberx.Kernel(new syscfg.SysCfg()) // 全局唯一
    
    let config = new Config()
    //console.log(config.ToJson())
    
    let result = null
    
    let tasker_test = new tasker.Tasker()
    tasker_test.plugin_id = 'derivx_stochastic_model'
    tasker_test.timeout_wait = 3600 // 秒
    tasker_test.distribute_type = 1 // 远程计算任务
    tasker_test.common_args = config.ToJson()
    
    tasker_test.method_id = func_make_data_gbm
    
    result = kernel.AssignTask(tasker_test) // 同步
    //console.log('同步:', result)
    if(result['return_code'] !== 0) {
        console.log(result['return_code'], result['return_info'])
    }
    else {
        result = JSON.parse(result['result_data'])
        console.log('result:', result)
    }
    
    event_task_finish = new AbortController()
    result = kernel.AssignTask(tasker_test, OnResult_Remote) // 异步
    //console.log('异步:', result)
    if(result['return_code'] !== 0) {
        console.log(result['return_code'], result['return_info'])
    }
    else {
        let tasker_id = result['tasker_id']
        const ret_wait = await promises.setTimeout(tasker_test.timeout_wait * 1000, '', { signal:event_task_finish.signal }).then(() => false, err => true) // 等待任务结果
        if(ret_wait != true) {
            console.log('等待任务结果超时！' + tasker_id)
        }
    }
}

Test_Remote()
