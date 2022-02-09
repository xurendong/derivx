
# -*- coding: utf-8 -*-

# Copyright (c) 2021-2022 the DerivX authors
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

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import syscfg
import cyberx

func_calc_price = 1
func_calc_greek = 2
func_calc_greek_surface = 3

def CalcPrice(module, model, s, k, r, q, v, t, is_call):
    inputs = {"model":model, "s":s, "k":k, "r":r, "q":q, "v":v, "t":t, "is_call":is_call}
    result = json.loads(module.DirectCalc(func_calc_price, 0, json.dumps(inputs)))
    if result["return_code"] != 0:
        print(result["return_code"], result["return_info"])
    return result["result_data"]

def CalcGreek(module, model, greek, s, k, r, q, v, t, is_long = True, is_call = True, is_futures = False, is_foreign = False):
    inputs = {"model":model, "greek":greek, "s":s, "k":k, "r":r, "q":q, "v":v, "t":t, "is_long":is_long, "is_call":is_call, "is_futures":is_futures, "is_foreign":is_foreign}
    result = json.loads(module.DirectCalc(func_calc_greek, 0, json.dumps(inputs)))
    if result["return_code"] != 0:
        print(result["return_code"], result["return_info"])
    return result["result_data"]

def CalcGreekSurface(module, model, greek, array_s, k, r, q, v, array_t, is_long = True, is_call = True, is_futures = False, is_foreign = False):
    inputs = {"model":model, "greek":greek, "array_s":array_s, "k":k, "r":r, "q":q, "v":v, "array_t":array_t, "is_long":is_long, "is_call":is_call, "is_futures":is_futures, "is_foreign":is_foreign}
    result = json.loads(module.DirectCalc(func_calc_greek_surface, 0, json.dumps(inputs)))
    if result["return_code"] != 0:
        print(result["return_code"], result["return_info"])
    return result["result_data"]

def FigureResult(array_s, array_t, result):
    figure = plt.figure()
    ax = Axes3D(figure)
    #ax = Axes3D(figure, auto_add_to_figure = False)
    #figure.add_axes(ax)
    x = array_t * 250
    y = array_s
    X, Y = np.meshgrid(x, y)
    ax.plot_surface(X, Y, result, rstride = 1, cstride = 1, cmap = plt.get_cmap("rainbow"))
    #ax.view_init(20, -25) # 视角：距离到期 由远到近
    ax.view_init(20, -125) # 视角：距离到期 由近到远
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.show()

def CalcPrice_Spread_Bull_Call(module, model, s, k_l_c_l, k_h_c_s, r, q, v_l_c_l, v_h_c_s, t):
    price_low_call_long = CalcPrice(module, model, s, k_l_c_l, r, q, v_l_c_l, t, True)
    price_high_call_short = -CalcPrice(module, model, s, k_h_c_s, r, q, v_h_c_s, t, True) # -
    return price_low_call_long + price_high_call_short

def CalcPrice_Spread_Bull_Put(module, model, s, k_l_p_l, k_h_p_s, r, q, v_l_p_l, v_h_p_s, t):
    price_low_put_long = CalcPrice(module, model, s, k_l_p_l, r, q, v_l_p_l, t, False)
    price_high_put_short = -CalcPrice(module, model, s, k_h_p_s, r, q, v_h_p_s, t, False) # -
    return price_low_put_long + price_high_put_short

def CalcPrice_Spread_Bear_Call(module, model, s, k_l_c_s, k_h_c_l, r, q, v_l_c_s, v_h_c_l, t):
    price_low_call_short = -CalcPrice(module, model, s, k_l_c_s, r, q, v_l_c_s, t, True) # -
    price_high_call_long = CalcPrice(module, model, s, k_h_c_l, r, q, v_h_c_l, t, True)
    return price_low_call_short + price_high_call_long

def CalcPrice_Spread_Bear_Put(module, model, s, k_l_p_s, k_h_p_l, r, q, v_l_p_s, v_h_p_l, t):
    price_low_put_short = -CalcPrice(module, model, s, k_l_p_s, r, q, v_l_p_s, t, False) # -
    price_high_put_long = CalcPrice(module, model, s, k_h_p_l, r, q, v_h_p_l, t, False)
    return price_low_put_short + price_high_put_long

def CalcPrice_Spread_Butterfly_Call(module, model, s, k_l_c_l, k_m_c_s, k_h_c_l, r, q, v_l_c_l, v_m_c_s, v_h_c_l, t):
    price_low_call_long = CalcPrice(module, model, s, k_l_c_l, r, q, v_l_c_l, t, True)
    price_middle_call_short = -CalcPrice(module, model, s, k_m_c_s, r, q, v_m_c_s, t, True) * 2 # - # * 2
    price_high_call_long = CalcPrice(module, model, s, k_h_c_l, r, q, v_h_c_l, t, True)
    return price_low_call_long + price_middle_call_short + price_high_call_long

def CalcPrice_Spread_Butterfly_Put(module, model, s, k_l_p_l, k_m_p_s, k_h_p_l, r, q, v_l_p_l, v_m_p_s, v_h_p_l, t):
    price_low_put_long = CalcPrice(module, model, s, k_l_p_l, r, q, v_l_p_l, t, False)
    price_middle_put_short = -CalcPrice(module, model, s, k_m_p_s, r, q, v_m_p_s, t, False) * 2 # - # * 2
    price_high_put_long = CalcPrice(module, model, s, k_h_p_l, r, q, v_h_p_l, t, False)
    return price_low_put_long + price_middle_put_short + price_high_put_long

def CalcPrice_Spread_Box_Bull_Call_Bear_Put(module, model, s, k_l_cp_ls, k_h_cp_sl, r, q, v_l_cp_ls, v_h_cp_sl, t):
    price_bull_call = CalcPrice_Spread_Bull_Call(module, model, s, k_l_cp_ls, k_h_cp_sl, r, q, v_l_cp_ls, v_h_cp_sl, t)
    price_bear_put = CalcPrice_Spread_Bear_Put(module, model, s, k_l_cp_ls, k_h_cp_sl, r, q, v_l_cp_ls, v_h_cp_sl, t)
    return price_bull_call + price_bear_put

def CalcPrice_Spread_Box_Bull_Put_Bear_Call(module, model, s, k_l_pc_ls, k_h_pc_sl, r, q, v_l_pc_ls, v_h_pc_sl, t):
    price_bull_put = CalcPrice_Spread_Bull_Put(module, model, s, k_l_pc_ls, k_h_pc_sl, r, q, v_l_pc_ls, v_h_pc_sl, t)
    price_bear_call = CalcPrice_Spread_Bear_Call(module, model, s, k_l_pc_ls, k_h_pc_sl, r, q, v_l_pc_ls, v_h_pc_sl, t)
    return price_bull_put + price_bear_call

def CalcGreek_Spread_Bull_Call(module, model, greek, s, k_l_c_l, k_h_c_s, r, q, v_l_c_l, v_h_c_s, t, is_long):
    result = 0.0
    if model == "bs":
        if greek == "d":
            delta_low_call_long = CalcGreek(module, model, greek, s, k_l_c_l, r, q, v_l_c_l, t, True, True)
            delta_high_call_short = CalcGreek(module, model, greek, s, k_h_c_s, r, q, v_h_c_s, t, False, True)
            result = delta_low_call_long + delta_high_call_short
        elif greek == "g":
            gamma_low_call_long = CalcGreek(module, model, greek, s, k_l_c_l, r, q, v_l_c_l, t, True)
            gamma_high_call_short = CalcGreek(module, model, greek, s, k_h_c_s, r, q, v_h_c_s, t, False)
            result = gamma_low_call_long + gamma_high_call_short
        elif greek == "v":
            vega_low_call_long = CalcGreek(module, model, greek, s, k_l_c_l, r, q, v_l_c_l, t, True)
            vega_high_call_short = CalcGreek(module, model, greek, s, k_h_c_s, r, q, v_h_c_s, t, False)
            result = vega_low_call_long + vega_high_call_short
        elif greek == "t":
            theta_low_call_long = CalcGreek(module, model, greek, s, k_l_c_l, r, q, v_l_c_l, t, True, True)
            theta_high_call_short = CalcGreek(module, model, greek, s, k_h_c_s, r, q, v_h_c_s, t, False, True)
            result = theta_low_call_long + theta_high_call_short
        elif greek == "r":
            rho_low_call_long = CalcGreek(module, model, greek, s, k_l_c_l, r, q, v_l_c_l, t, True, True, False, False)
            rho_high_call_short = CalcGreek(module, model, greek, s, k_h_c_s, r, q, v_h_c_s, t, False, True, False, False)
            result = rho_low_call_long + rho_high_call_short
    if is_long == True:
        return result
    else:
        return -result

def CalcGreekSurface_Spread_Bull_Call(module, model, greek, array_s, k_l_c_l, k_h_c_s, r, q, v_l_c_l, v_h_c_s, array_t, is_long):
    surface_low_call_long = np.zeros((len(array_s), len(array_t)))
    surface_high_call_short = np.zeros((len(array_s), len(array_t)))
    if model == "bs":
        if greek == "d":
            surface_low_call_long = np.array(CalcGreekSurface(module, model, greek, array_s, k_l_c_l, r, q, v_l_c_l, array_t, True, True))
            surface_high_call_short = np.array(CalcGreekSurface(module, model, greek, array_s, k_h_c_s, r, q, v_h_c_s, array_t, False, True))
        elif greek == "g":
            surface_low_call_long = np.array(CalcGreekSurface(module, model, greek, array_s, k_l_c_l, r, q, v_l_c_l, array_t, True))
            surface_high_call_short = np.array(CalcGreekSurface(module, model, greek, array_s, k_h_c_s, r, q, v_h_c_s, array_t, False))
        elif greek == "v":
            surface_low_call_long = np.array(CalcGreekSurface(module, model, greek, array_s, k_l_c_l, r, q, v_l_c_l, array_t, True))
            surface_high_call_short = np.array(CalcGreekSurface(module, model, greek, array_s, k_h_c_s, r, q, v_h_c_s, array_t, False))
        elif greek == "t":
            surface_low_call_long = np.array(CalcGreekSurface(module, model, greek, array_s, k_l_c_l, r, q, v_l_c_l, array_t, True, True))
            surface_high_call_short = np.array(CalcGreekSurface(module, model, greek, array_s, k_h_c_s, r, q, v_h_c_s, array_t, False, True))
        elif greek == "r":
            surface_low_call_long = np.array(CalcGreekSurface(module, model, greek, array_s, k_l_c_l, r, q, v_l_c_l, array_t, True, True, False, False))
            surface_high_call_short = np.array(CalcGreekSurface(module, model, greek, array_s, k_h_c_s, r, q, v_h_c_s, array_t, False, True, False, False))
    result = surface_low_call_long + surface_high_call_short
    if is_long == True:
        return result
    else:
        return -result

def Test_DerivX_Vanilla_European():
    result = 0.0
    surface = []
    kernel = cyberx.Kernel(syscfg.SysCfg().ToArgs()) # 全局唯一
    module = cyberx.Create("derivx_vanilla_european")
    
    #result = CalcPrice(module, "bs", 100.0, 100.0, 0.03, 0.08 - 0.03, 0.15, 1.0, True)
    #result = CalcPrice(module, "bs", 42.0, 40.0, 0.1, 0.0, 0.2, 0.5, True)
    #result = CalcGreek(module, "bs", "d", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True, True)
    #result = CalcGreek(module, "bs", "g", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True)
    #result = CalcGreek(module, "bs", "v", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True)
    #result = CalcGreek(module, "bs", "t", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True, True)
    #result = CalcGreek(module, "bs", "r", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True, True, False, False)
    #print(result)
    
    #result = CalcPrice(module, "bs", 100.0, 100.0, 0.03, 0.08 + 0.03, 0.22, 1.0, False)
    #result = CalcPrice(module, "bs", 42.0, 40.0, 0.1, 0.0, 0.2, 0.5, False)
    #result = CalcGreek(module, "bs", "d", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True, False)
    #result = CalcGreek(module, "bs", "g", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True)
    #result = CalcGreek(module, "bs", "v", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True)
    #result = CalcGreek(module, "bs", "t", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True, False)
    #result = CalcGreek(module, "bs", "r", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True, False, False, False)
    #print(result)
    
    #array_s = np.arange(5.0, 105.0, 5.0).tolist()
    #array_t = np.arange(0.004, 1.004, 1.0 / 250).tolist()
    
    #surface = CalcGreekSurface(module, "bs", "d", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True, True)
    #surface = CalcGreekSurface(module, "bs", "g", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True)
    #surface = CalcGreekSurface(module, "bs", "v", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True)
    #surface = CalcGreekSurface(module, "bs", "t", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True, True)
    #surface = CalcGreekSurface(module, "bs", "r", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True, True, False, False)
    #FigureResult(np.array(array_s), np.array(array_t), np.array(surface))
    
    #surface = CalcGreekSurface(module, "bs", "d", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True, False)
    #surface = CalcGreekSurface(module, "bs", "g", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True)
    #surface = CalcGreekSurface(module, "bs", "v", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True)
    #surface = CalcGreekSurface(module, "bs", "t", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True, False)
    #surface = CalcGreekSurface(module, "bs", "r", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True, False, False, False)
    #FigureResult(np.array(array_s), np.array(array_t), np.array(surface))
    
    array_s = np.arange(5.0, 105.0, 5.0).tolist()
    array_t = np.arange(0.004, 1.004, 1.0 / 250).tolist()
    model, s, k_l, k_m, k_h, r, q, v_l, v_m, v_h, t, is_long = "bs", 50.0, 40.0, 50.0, 60.0, 0.05, 0.0, 0.2, 0.2, 0.2, 0.5, True
    #print(CalcPrice_Spread_Bull_Call(module, model, s, k_l, k_h, r, q, v_l, v_h, t))
    #print(CalcPrice_Spread_Bull_Put(module, model, s, k_l, k_h, r, q, v_l, v_h, t))
    #print(CalcPrice_Spread_Bear_Call(module, model, s, k_l, k_h, r, q, v_l, v_h, t))
    #print(CalcPrice_Spread_Bear_Put(module, model, s, k_l, k_h, r, q, v_l, v_h, t))
    #print(CalcPrice_Spread_Butterfly_Call(module, model, s, k_l, k_m, k_h, r, q, v_l, v_m, v_h, t))
    #print(CalcPrice_Spread_Butterfly_Put(module, model, s, k_l, k_m, k_h, r, q, v_l, v_m, v_h, t))
    #print(CalcPrice_Spread_Box_Bull_Call_Bear_Put(module, model, s, k_l, k_h, r, q, v_l, v_h, t))
    #print(CalcPrice_Spread_Box_Bull_Put_Bear_Call(module, model, s, k_l, k_h, r, q, v_l, v_h, t))
    #print(CalcGreek_Spread_Bull_Call(module, model, "d", s, k_l, k_h, r, q, v_l, v_h, t, is_long))
    #print(CalcGreek_Spread_Bull_Call(module, model, "g", s, k_l, k_h, r, q, v_l, v_h, t, is_long))
    #print(CalcGreek_Spread_Bull_Call(module, model, "v", s, k_l, k_h, r, q, v_l, v_h, t, is_long))
    #print(CalcGreek_Spread_Bull_Call(module, model, "t", s, k_l, k_h, r, q, v_l, v_h, t, is_long))
    #print(CalcGreek_Spread_Bull_Call(module, model, "r", s, k_l, k_h, r, q, v_l, v_h, t, is_long))
    #surface = CalcGreekSurface_Spread_Bull_Call(module, model, "d", array_s, k_l, k_h, r, q, v_l, v_h, array_t, is_long)
    #surface = CalcGreekSurface_Spread_Bull_Call(module, model, "g", array_s, k_l, k_h, r, q, v_l, v_h, array_t, is_long)
    #surface = CalcGreekSurface_Spread_Bull_Call(module, model, "v", array_s, k_l, k_h, r, q, v_l, v_h, array_t, is_long)
    #surface = CalcGreekSurface_Spread_Bull_Call(module, model, "t", array_s, k_l, k_h, r, q, v_l, v_h, array_t, is_long)
    surface = CalcGreekSurface_Spread_Bull_Call(module, model, "r", array_s, k_l, k_h, r, q, v_l, v_h, array_t, is_long)
    FigureResult(np.array(array_s), np.array(array_t), surface)

if __name__ == "__main__":
    Test_DerivX_Vanilla_European()
