
# -*- coding: utf-8 -*-

# Copyright (c) 2021-2023 the DerivX authors
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

# 示例说明：
# 1、测试远程执行调用

import json
import threading

import numpy as np
import matplotlib.pyplot as plt

import syscfg
import tasker
import cyberx

func_make_data_gbm = 1

event_task_finish = threading.Event()

def ShowPlot_Distribution(price, path, step, title, ylabel):
    plt.figure()
    ax = plt.subplot2grid((1, 1), (0, 0), colspan = 1, rowspan = 1)
    ax.set_xlabel("Steps")
    ax.set_ylabel(ylabel)
    for i in range(path):
        ax.plot(range(step), price[i, :], color = np.random.rand(3), ls = "-", lw = 1.0)
    #ax.legend(loc = "best") # 不显示图例
    ax.margins(0, 0) # 0 ~ 1
    ax.set_title(title)
    plt.subplots_adjust(left = 0.05, bottom = 0.05, right = 0.99, top = 0.98, wspace = 0.0, hspace = 0.0)
    plt.grid(True, alpha = 0.5)
    plt.show()

class Config(object):
    def __init__(self):
        self.rand_rows = 500 # 随机数据行数
        self.rand_cols = 500 # 随机数据列数
        self.dimension = 0 # 随机数据维度 # 未使用
        self.rand_seed = [0, 1, 2, 3, 4, 5, 6, 7] # 随机数据种子 # 非负整数，有效位数不超逻辑处理器数量
        self.runs_size = 500 # 模拟路径数量
        self.runs_step = 500 # 价格变动步数
        self.year_days = 244 # 年交易日数量
        self.price = 1.0 # 初始价格
        self.sigma = 0.2 # 波动率
        self.risk_free_rate = 0.03 # 无风险利率
        self.basis_rate = 0.0 # 股息率或贴水率

    def ToJson(self):
        return json.dumps(self.__dict__)

def OnResult_Remote(result):
    try:
        #print("Callback OnResult_Remote:", result)
        if result["return_code"] != 0:
            print(result["return_code"], result["return_info"])
        else:
            result = json.loads(result["result_data"])
            #print("result:", result)
    except Exception as e:
        print("OnResult_Remote 异常！%s" % e)
    event_task_finish.set() #

def Test_Remote():
    kernel = cyberx.Kernel(syscfg.SysCfg().ToArgs()) # 全局唯一
    
    result = None
    
    result = kernel.StartRemote() #
    print(result["return_code"], result["return_info"])
    
    if kernel.CheckConnect() == True:
        print("connect success")
    else:
        print("connect failure")
    
    config = Config()
    #print(config.ToJson())
    
    tasker_test = tasker.Tasker()
    tasker_test.plugin_id = "derivx_stochastic_model"
    tasker_test.timeout_wait = 3600 # 秒
    tasker_test.distribute_type = 1 # 远程计算任务
    tasker_test.common_args = config.ToJson()
    
    tasker_test.method_id = func_make_data_gbm

    for i in range(1000):
        result = kernel.AssignTask(tasker_test.ToArgs()) # 同步
        #print("同步:", result)
        if result["return_code"] != 0:
            print(result["return_code"], result["return_info"])
        else:
            result = json.loads(result["result_data"])
            #print("result:", result)
            #ShowPlot_Distribution(np.array(result), config.runs_size, config.runs_step, "Price - Steps", "Price")
    
    for i in range(1000):
        event_task_finish.clear()
        result = kernel.AssignTask(tasker_test.ToArgs(), OnResult_Remote) # 异步
        #print("异步:", result)
        if result["return_code"] != 0:
            print(result["return_code"], result["return_info"])
        else:
            tasker_id = result["tasker_id"]
            ret_wait = event_task_finish.wait(timeout = tasker_test.timeout_wait) # 等待任务结果
            if ret_wait != True:
                print("等待任务结果超时！", tasker_id)
    
    result = kernel.StopRemote() #
    print(result["return_code"], result["return_info"])

if __name__ == "__main__":
    Test_Remote()
