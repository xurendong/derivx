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

class Tasker {
    constructor() {
        this.tasker_id = 0 // 任务分配标识
        this.method_id = 0 // 执行函数标识
        this.plugin_id = '' // 执行插件名称
        this.grain_size = 0 // 任务分发粒度
        this.split_size = 0 // 任务拆分数量
        this.serialize_type = 0 // 参数序列化类型
        this.distribute_type = 0 // 任务分发类型
        this.common_args = '' // 共有公共参数，需已序列化
        this.custom_args = [] // 私有定制参数，需已序列化
    }
}

module.exports.Tasker = Tasker
