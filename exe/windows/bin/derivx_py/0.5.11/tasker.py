
# -*- coding: utf-8 -*-

# Copyright (c) 2021-2023 the CyberX authors
# All rights reserved.
#
# The project sponsor and lead author is Xu Rendong.
# E-mail: xrd@ustc.edu, QQ: 277195007, WeChat: xrd_ustc
# See the contributors file for names of other contributors.
#
# Commercial use of this code in source and binary forms is
# governed by a LGPL v3 license. You may get a copy from the
# root directory. Or else you should get a specific written 
# permission from the project author.
#
# Individual and educational use of this code in source and
# binary forms is governed by a 3-clause BSD license. You may
# get a copy from the root directory. Certainly welcome you
# to contribute code of all sorts.
#
# Be sure to retain the above copyright notice and conditions.

# 任务分发粒度
grain_single_machine = 0 # 单台机器
grain_cpu_logic_core = 1 # CPU 逻辑核心

# 任务分发类型
distribute_local = 0 # 本地计算任务
distribute_remote = 1 # 远程计算任务

# 序列化类型
serialize_json = 0 # Json
serialize_bson = 1 # Bson
serialize_thrift = 2 # Thrift
serialize_msgpack = 3 # MsgPack
serialize_protobuf = 4 # ProtoBuf

class Tasker(object):
    def __init__(self):
        self.tasker_id = 0 # 任务分配标识
        self.method_id = 0 # 执行函数标识
        self.plugin_id = "" # 执行插件名称
        self.grain_size = 0 # 任务分发粒度
        self.split_size = 0 # 任务拆分数量
        self.timeout_wait = 0 # 任务超时秒数
        self.serialize_type = 0 # 参数序列化类型
        self.distribute_type = 0 # 任务分发类型
        self.common_args = "" # 共有公共参数，需已序列化
        self.custom_args = [] # 私有定制参数，需已序列化

    def ToArgs(self):
        return self.__dict__
