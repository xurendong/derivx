
# -*- coding: utf-8 -*-

# Copyright (c) 2021-2022 the CyberX authors
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

class SysCfg(object):
    def __init__(self):
        self.work_path = "" # 工作路径 # 路径中 "\" 使用 "\\" 替换
        self.local_cpu_thread = 8 # 本机 CPU 逻辑核心使用数量
        self.plugins = [ # 插件列表
            {"work": True, "name": "derivx_autocall_booster", "version": "1.0.0"},
            {"work": True, "name": "derivx_autocall_fixed_coupon_notes", "version": "1.0.0"},
            {"work": True, "name": "derivx_autocall_phoenix", "version": "1.0.0"},
            {"work": True, "name": "derivx_autocall_snowball", "version": "1.0.0"},
            {"work": True, "name": "derivx_autocall_snowball_stage_coupon", "version": "1.0.0"},
            {"work": True, "name": "derivx_barrier_sharkfin", "version": "1.0.0"},
            {"work": True, "name": "derivx_barrier_single", "version": "1.0.0"},
            {"work": True, "name": "derivx_digital_simple", "version": "1.0.0"},
            {"work": True, "name": "derivx_stochastic_model", "version": "1.0.0"},
            {"work": True, "name": "derivx_vanilla_american", "version": "1.0.0"},
            {"work": True, "name": "derivx_vanilla_european", "version": "1.0.0"}
        ]

    def ToArgs(self):
        return self.__dict__
