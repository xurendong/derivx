
# -*- coding: utf-8 -*-

# Copyright (c) 2021-2024 the DerivX authors
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
# 1、演示美式香草期权隐含波动率、理论价格、希腊值、希腊值曲面等的计算（基于 BAW 公式）；
# 2、演示美式香草期权隐含波动率、理论价格、希腊值、希腊值曲面等的计算（基于二叉树方法）；
# 3、演示通过 Create 方法获取执行模块实例；
# 4、演示 直接模式 DirectCall 任务执行调用；
# 5、演示任务参数序列化和任务结果反序列化的封装；

# 注意：版本 >= 0.5.14 的，编译环境 Visual Studio 从 17.9.X 升级为 17.10.X 后，
#      对于 Python 3.6、3.7、3.8、3.9、3.10、3.11 存在一些兼容问题，
#      需要将 import cyberx 语句放在 import 如 pandas、PyQt5 等其他第三方库之前，
#      对于 Python 3.12 则仍然可以正常地任意放置，初始化 cyberx.Kernel 时不会异常。

import json

import cyberx

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import syscfg
# import cyberx

func_calc_iv             = 1
func_calc_price          = 2
func_calc_greeks         = 3
func_calc_greeks_surface = 4

def CalcIV(module, model, method, p, s, k, r, q, t, is_call, tree_step = 10000):
    inputs = {"model":model, "method":method, "p":p, "s":s, "k":k, "r":r, "q":q, "t":t, "is_call":is_call, "tree_step":tree_step}
    result = json.loads(module.DirectCall(func_calc_iv, 0, json.dumps(inputs)))
    if result["return_code"] != 0:
        print(result["return_code"], result["return_info"])
    return result["result_data"]

def CalcPrice(module, model, s, k, r, q, v, t, is_call, tree_step = 10000):
    inputs = {"model":model, "s":s, "k":k, "r":r, "q":q, "v":v, "t":t, "is_call":is_call, "tree_step":tree_step}
    result = json.loads(module.DirectCall(func_calc_price, 0, json.dumps(inputs)))
    if result["return_code"] != 0:
        print(result["return_code"], result["return_info"])
    return result["result_data"]

def CalcGreeks(module, model, greek, s, k, r, q, v, t, is_long = True, is_call = True, is_futures = False, is_foreign = False, tree_step = 10000):
    inputs = {"model":model, "greek":greek, "s":s, "k":k, "r":r, "q":q, "v":v, "t":t, "is_long":is_long, "is_call":is_call, "is_futures":is_futures, "is_foreign":is_foreign, "tree_step":tree_step}
    result = json.loads(module.DirectCall(func_calc_greeks, 0, json.dumps(inputs)))
    if result["return_code"] != 0:
        print(result["return_code"], result["return_info"])
    return result["result_data"]

def CalcGreeksSurface(module, model, greek, array_s, k, r, q, v, array_t, is_long = True, is_call = True, is_futures = False, is_foreign = False, tree_step = 10000):
    inputs = {"model":model, "greek":greek, "array_s":array_s, "k":k, "r":r, "q":q, "v":v, "array_t":array_t, "is_long":is_long, "is_call":is_call, "is_futures":is_futures, "is_foreign":is_foreign, "tree_step":tree_step}
    result = json.loads(module.DirectCall(func_calc_greeks_surface, 0, json.dumps(inputs)))
    if result["return_code"] != 0:
        print(result["return_code"], result["return_info"])
    return result["result_data"]

def FigureResult(array_s, array_t, result):
    figure = plt.figure()
    ax = Axes3D(figure)
    #ax = Axes3D(figure, auto_add_to_figure = False)
    figure.add_axes(ax)
    x = array_t * 250
    y = array_s
    X, Y = np.meshgrid(x, y)
    ax.plot_surface(X, Y, result, rstride = 1, cstride = 1, cmap = plt.get_cmap("rainbow"))
    #ax.view_init(20, -25) # 视角：距离到期 由远到近
    ax.view_init(20, -125) # 视角：距离到期 由近到远
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.show()

def Test_DerivX_Vanilla_American():
    result = 0.0
    surface = []
    kernel = cyberx.Kernel(syscfg.SysCfg().ToArgs()) # 全局唯一
    module = cyberx.Create("derivx_vanilla_american") # 全局唯一
    #module_01 = cyberx.Create("derivx_vanilla_american") # 重复创建会报异常
    #module_01 = cyberx.GetCreate("derivx_vanilla_american") # 可以获取已创建的实例
    
    #result = CalcIV(module, "ba", "v", 0.1566, 5.29, 6.0, 0.04, 0.0, 0.5, True) # Vega 法
    #result = CalcIV(module, "ba", "v", 0.7503, 5.29, 6.0, 0.04, 0.0, 0.5, False) # Vega 法
    #result = CalcIV(module, "ba", "b", 0.1566, 5.29, 6.0, 0.04, 0.0, 0.5, True) # Binary 法
    #result = CalcIV(module, "ba", "b", 0.7503, 5.29, 6.0, 0.04, 0.0, 0.5, False) # Binary 法
    #result = CalcIV(module, "ba", "n", 0.1566, 5.29, 6.0, 0.04, 0.0, 0.5, True) # Newton 法
    #result = CalcIV(module, "ba", "n", 0.7503, 5.29, 6.0, 0.04, 0.0, 0.5, False) # Newton 法
    #print(result)
    
    #result = CalcPrice(module, "ba", 100.0, 100.0, 0.03, 0.08 - 0.03, 0.2, 1.0, True)
    #result = CalcPrice(module, "ba", 42.0, 40.0, 0.1, 0.0, 0.2, 0.5, True)
    #result = CalcPrice(module, "ba", 42.0, 40.0, 0.1, -0.01, 0.2, 0.5, True) # b >= r
    #result = CalcGreeks(module, "ba", "d", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True, True)
    #result = CalcGreeks(module, "ba", "g", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True)
    #result = CalcGreeks(module, "ba", "v", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True)
    #result = CalcGreeks(module, "ba", "t", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True, True)
    #result = CalcGreeks(module, "ba", "r", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True, True, False, False)
    #print(result)
    
    #result = CalcPrice(module, "ba", 100.0, 100.0, 0.03, 0.08 + 0.03, 0.2, 1.0, False)
    #result = CalcPrice(module, "ba", 42.0, 40.0, 0.1, 0.0, 0.2, 0.5, False)
    #result = CalcPrice(module, "ba", 42.0, 40.0, 0.1, -0.01, 0.2, 0.5, False) # b >= r
    #result = CalcGreeks(module, "ba", "d", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True, False)
    #result = CalcGreeks(module, "ba", "g", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True)
    #result = CalcGreeks(module, "ba", "v", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True)
    #result = CalcGreeks(module, "ba", "t", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True, False)
    #result = CalcGreeks(module, "ba", "r", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True, False, False, False)
    #print(result)
    
    # 为使代码美观参数清晰，示例中二叉树节点层数通过 CalcIV、CalcPrice、CalcGreeks、CalcGreeksSurface 等函数的入参默认值设置
    
    #result = CalcIV(module, "bt", "v", 0.1566, 5.29, 6.0, 0.04, 0.0, 0.5, True) # Vega 法
    #result = CalcIV(module, "bt", "v", 0.7503, 5.29, 6.0, 0.04, 0.0, 0.5, False) # Vega 法
    #result = CalcIV(module, "bt", "b", 0.1566, 5.29, 6.0, 0.04, 0.0, 0.5, True) # Binary 法
    #result = CalcIV(module, "bt", "b", 0.7503, 5.29, 6.0, 0.04, 0.0, 0.5, False) # Binary 法
    #result = CalcIV(module, "bt", "n", 0.1566, 5.29, 6.0, 0.04, 0.0, 0.5, True) # Newton 法
    #result = CalcIV(module, "bt", "n", 0.7503, 5.29, 6.0, 0.04, 0.0, 0.5, False) # Newton 法
    #print(result)
    
    #result = CalcPrice(module, "ba", 50.0, 50.0, 0.1, 0.03, 0.4, 0.4167, True)
    #print(result)
    #result = CalcPrice(module, "bt", 50.0, 50.0, 0.1, 0.03, 0.4, 0.4167, True)
    #print(result)
    
    #result = CalcPrice(module, "ba", 50.0, 50.0, 0.1, 0.03, 0.4, 0.4167, False)
    #print(result)
    #result = CalcPrice(module, "bt", 50.0, 50.0, 0.1, 0.03, 0.4, 0.4167, False)
    #print(result)
    
    #result = CalcGreeks(module, "ba", "d", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True, True)
    #result = CalcGreeks(module, "ba", "g", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True)
    #result = CalcGreeks(module, "ba", "v", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True)
    #result = CalcGreeks(module, "ba", "t", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True, True)
    #result = CalcGreeks(module, "ba", "r", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True, True, False, False)
    #print(result)
    #result = CalcGreeks(module, "bt", "d", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True, True)
    #result = CalcGreeks(module, "bt", "g", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True)
    #result = CalcGreeks(module, "bt", "v", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True)
    #result = CalcGreeks(module, "bt", "t", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True, True)
    #result = CalcGreeks(module, "bt", "r", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True, True, False, False)
    #print(result)
    
    #result = CalcGreeks(module, "ba", "d", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True, False)
    #result = CalcGreeks(module, "ba", "g", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True)
    #result = CalcGreeks(module, "ba", "v", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True)
    #result = CalcGreeks(module, "ba", "t", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True, False)
    #result = CalcGreeks(module, "ba", "r", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True, False, False, False)
    #print(result)
    #result = CalcGreeks(module, "bt", "d", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True, False)
    #result = CalcGreeks(module, "bt", "g", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True)
    #result = CalcGreeks(module, "bt", "v", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True)
    #result = CalcGreeks(module, "bt", "t", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True, False)
    #result = CalcGreeks(module, "bt", "r", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True, False, False, False)
    #print(result)
    
    #array_s = np.arange(5.0, 105.0, 5.0).tolist()
    #array_t = np.arange(0.004, 1.004, 1.0 / 250).tolist()
    #array_t = np.arange(0.020, 1.020, 5.0 / 250).tolist() # 测试二叉树时建议减少计算时间点
    
    #surface = CalcGreeksSurface(module, "ba", "d", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True, True)
    #surface = CalcGreeksSurface(module, "ba", "g", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True)
    #surface = CalcGreeksSurface(module, "ba", "v", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True)
    #surface = CalcGreeksSurface(module, "ba", "t", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True, True)
    #surface = CalcGreeksSurface(module, "ba", "r", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True, True, False, False)
    #FigureResult(np.array(array_s), np.array(array_t), np.array(surface))
    #surface = CalcGreeksSurface(module, "bt", "d", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True, True)
    #surface = CalcGreeksSurface(module, "bt", "g", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True)
    #surface = CalcGreeksSurface(module, "bt", "v", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True)
    #surface = CalcGreeksSurface(module, "bt", "t", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True, True)
    #surface = CalcGreeksSurface(module, "bt", "r", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True, True, False, False)
    #FigureResult(np.array(array_s), np.array(array_t), np.array(surface))
    
    #surface = CalcGreeksSurface(module, "ba", "d", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True, False)
    #surface = CalcGreeksSurface(module, "ba", "g", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True)
    #surface = CalcGreeksSurface(module, "ba", "v", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True)
    #surface = CalcGreeksSurface(module, "ba", "t", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True, False)
    #surface = CalcGreeksSurface(module, "ba", "r", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True, False, False, False)
    #FigureResult(np.array(array_s), np.array(array_t), np.array(surface))
    #surface = CalcGreeksSurface(module, "bt", "d", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True, False)
    #surface = CalcGreeksSurface(module, "bt", "g", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True)
    #surface = CalcGreeksSurface(module, "bt", "v", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True)
    #surface = CalcGreeksSurface(module, "bt", "t", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True, False)
    #surface = CalcGreeksSurface(module, "bt", "r", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True, False, False, False)
    #FigureResult(np.array(array_s), np.array(array_t), np.array(surface))

if __name__ == "__main__":
    Test_DerivX_Vanilla_American()
