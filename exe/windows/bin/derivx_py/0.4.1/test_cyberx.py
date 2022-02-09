
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

import json

import syscfg
import cyberx

print(cyberx.Version())

g_syscfg = syscfg.SysCfg()
g_kernel = cyberx.Kernel(g_syscfg.ToArgs()) # 全局唯一 # 全局不析构

def OnResult(flag, task, unit, func, form, code, info, data):
    print("TestAsync Callback OnResult:", flag, task, unit, func, form, code, info, data)

def Test_Kernel_Object():
    #g_syscfg = syscfg.SysCfg()
    #g_kernel = cyberx.Kernel(g_syscfg.ToArgs()) # 全局唯一 # 局部会析构
    
    for i in range(10):
        print(g_kernel.Test())
    
    obj_req = {"type_int":123, "type_bool":True, "type_double":123.456, "type_string":"cyberx"}
    msg_req = json.dumps(obj_req)
    msg_ans = g_kernel.TestJson(msg_req)
    obj_ans = json.loads(msg_ans)
    print("obj_req:", obj_req)
    print("msg_req:", msg_req)
    print("msg_ans:", msg_ans)
    print("obj_ans:", obj_ans)
    
    g_kernel.TestAsync(OnResult)
    g_kernel.TestAsync(OnResult)

if __name__ == "__main__":
    Test_Kernel_Object()
