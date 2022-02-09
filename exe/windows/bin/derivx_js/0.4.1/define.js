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

// 任务分发粒度
exports.tasker_grain_single_machine = 0 // 单台机器
exports.tasker_grain_cpu_logic_core = 1 // CPU 逻辑核心

// 任务分发类型
exports.tasker_distribute_local = 0 // 本地计算任务
exports.tasker_distribute_remote = 1 // 远程计算任务

// 序列化类型
exports.tasker_serialize_json = 0 // Json
exports.tasker_serialize_bson = 1 // Bson
exports.tasker_serialize_thrift = 2 // Thrift
exports.tasker_serialize_msgpack = 3 // MsgPack
exports.tasker_serialize_protobuf = 4 // ProtoBuf
