
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
# 1、演示数字期权 Gap、CashOrNothing、AssetOrNothing、SuperShare 等的价格和收益计算；
# 2、演示通过 Create 方法获取执行模块实例；
# 3、演示 直接模式 DirectCalc 任务执行调用；
# 4、演示任务参数序列化和任务结果反序列化的封装；

import json

import syscfg
import cyberx

func_gap_calc_price               = 1
func_gap_calc_payoff              = 2
func_cash_or_nothing_calc_price   = 3
func_cash_or_nothing_calc_payoff  = 4
func_asset_or_nothing_calc_price  = 5
func_asset_or_nothing_calc_payoff = 6
func_super_share_calc_price       = 7
func_super_share_calc_payoff      = 8

def Gap_CalcPrice(module, s, k_1, k_2, r, q, v, t, is_call):
    inputs = {"s":s, "k_1":k_1, "k_2":k_2, "r":r, "q":q, "v":v, "t":t, "is_call":is_call}
    result = json.loads(module.DirectCalc(func_gap_calc_price, 0, json.dumps(inputs)))
    if result["return_code"] != 0:
        print(result["return_code"], result["return_info"])
    return result["result_data"]

def Gap_CalcPayoff(module, s, k_1, k_2, is_call):
    inputs = {"s":s, "k_1":k_1, "k_2":k_2, "is_call":is_call}
    result = json.loads(module.DirectCalc(func_gap_calc_payoff, 0, json.dumps(inputs)))
    if result["return_code"] != 0:
        print(result["return_code"], result["return_info"])
    return result["result_data"]

def CashOrNothing_CalcPrice(module, s, k, r, q, v, t, cash, is_call):
    inputs = {"s":s, "k":k, "r":r, "q":q, "v":v, "t":t, "cash":cash, "is_call":is_call}
    result = json.loads(module.DirectCalc(func_cash_or_nothing_calc_price, 0, json.dumps(inputs)))
    if result["return_code"] != 0:
        print(result["return_code"], result["return_info"])
    return result["result_data"]

def CashOrNothing_CalcPayoff(module, s, k, cash, is_call):
    inputs = {"s":s, "k":k, "cash":cash, "is_call":is_call}
    result = json.loads(module.DirectCalc(func_cash_or_nothing_calc_payoff, 0, json.dumps(inputs)))
    if result["return_code"] != 0:
        print(result["return_code"], result["return_info"])
    return result["result_data"]

def AssetOrNothing_CalcPrice(module, s, k, r, q, v, t, is_call):
    inputs = {"s":s, "k":k, "r":r, "q":q, "v":v, "t":t, "is_call":is_call}
    result = json.loads(module.DirectCalc(func_asset_or_nothing_calc_price, 0, json.dumps(inputs)))
    if result["return_code"] != 0:
        print(result["return_code"], result["return_info"])
    return result["result_data"]

def AssetOrNothing_CalcPayoff(module, s, k, is_call):
    inputs = {"s":s, "k":k, "is_call":is_call}
    result = json.loads(module.DirectCalc(func_asset_or_nothing_calc_payoff, 0, json.dumps(inputs)))
    if result["return_code"] != 0:
        print(result["return_code"], result["return_info"])
    return result["result_data"]

def SuperShare_CalcPrice(module, s, k_l, k_h, r, q, v, t):
    inputs = {"s":s, "k_l":k_l, "k_h":k_h, "r":r, "q":q, "v":v, "t":t}
    result = json.loads(module.DirectCalc(func_super_share_calc_price, 0, json.dumps(inputs)))
    if result["return_code"] != 0:
        print(result["return_code"], result["return_info"])
    return result["result_data"]

def SuperShare_CalcPayoff(module, s, k_l, k_h):
    inputs = {"s":s, "k_l":k_l, "k_h":k_h}
    result = json.loads(module.DirectCalc(func_super_share_calc_payoff, 0, json.dumps(inputs)))
    if result["return_code"] != 0:
        print(result["return_code"], result["return_info"])
    return result["result_data"]

def Test_Derivx_Digital_Simple():
    kernel = cyberx.Kernel(syscfg.SysCfg().ToArgs()) # 全局唯一
    module = cyberx.Create("derivx_digital_simple")
    
    result = 0.0
    result = Gap_CalcPrice(module, 50.0, 50.0, 57.0, 0.09, 0.0, 0.2, 0.5, True)
    print("price:", result)
    result = Gap_CalcPayoff(module, 55.0, 50.0, 57.0, True)
    print("payoff:", result)
    result = CashOrNothing_CalcPrice(module, 100.0, 80.0, 0.06, 0.06, 0.35, 0.75, 10.0, False)
    print("price:", result)
    result = CashOrNothing_CalcPayoff(module, 100.0, 80.0, 10.0, True)
    print("payoff:", result)
    result = AssetOrNothing_CalcPrice(module, 70.0, 65.0, 0.07, 0.05, 0.27, 0.5, False)
    print("price:", result)
    result = AssetOrNothing_CalcPayoff(module, 70.0, 65.0, True)
    print("payoff:", result)
    result = SuperShare_CalcPrice(module, 100.0, 90.0, 110.0, 0.1, 0.1, 0.2, 0.25)
    print("price:", result)
    result = SuperShare_CalcPayoff(module, 100.0, 90.0, 110.0)
    print("payoff:", result)

if __name__ == "__main__":
    Test_Derivx_Digital_Simple()
