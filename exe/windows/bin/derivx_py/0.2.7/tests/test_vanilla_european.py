
# -*- coding: utf-8 -*-

# Copyright (c) 2021-2021 the DerivX authors
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

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import derivx

def FigureResult(array_s, array_t, result):
    figure = plt.figure()
    ax = Axes3D(figure)
    x = array_t * 250
    y = array_s
    X, Y = np.meshgrid(x, y)
    ax.plot_surface(X, Y, result, rstride = 1, cstride = 1, cmap = plt.get_cmap("rainbow"))
    #ax.view_init(20, -25) # 视角：距离到期 由远到近
    ax.view_init(20, -125) # 视角：距离到期 由近到远
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.show()

def Test_Vanilla_European():
    vanilla = derivx.Vanilla("European")
    
    # CalcPrice(model, s, k, r, q, sigma, t, is_call)
    # CalcGreeks(model, greek, s, k, r, q, sigma, t, is_call, is_futures, is_foreign)
    # CalcGreeksSurface(surface, model, greek, s, k, r, q, sigma, t, is_call, is_futures, is_foreign)
    
    #result = vanilla.CalcPrice("bs", 100.0, 100.0, 0.03, 0.08 - 0.03, 0.15, 1.0, True)
    #result = vanilla.CalcPrice("bs", 42.0, 40.0, 0.1, 0.0, 0.2, 0.5, True)
    #result = vanilla.CalcGreeks("bs", "d", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True)
    #result = vanilla.CalcGreeks("bs", "g", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846)
    #result = vanilla.CalcGreeks("bs", "v", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846)
    #result = vanilla.CalcGreeks("bs", "t", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True)
    #result = vanilla.CalcGreeks("bs", "r", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, True, False, False)
    #print(result)
    
    #result = vanilla.CalcPrice("bs", 100.0, 100.0, 0.03, 0.08 + 0.03, 0.22, 1.0, False)
    #result = vanilla.CalcPrice("bs", 42.0, 40.0, 0.1, 0.0, 0.2, 0.5, False)
    #result = vanilla.CalcGreeks("bs", "d", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, False)
    #result = vanilla.CalcGreeks("bs", "g", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846)
    #result = vanilla.CalcGreeks("bs", "v", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846)
    #result = vanilla.CalcGreeks("bs", "t", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, False)
    #result = vanilla.CalcGreeks("bs", "r", 49.0, 50.0, 0.05, 0.0, 0.2, 0.3846, False, False, False)
    #print(result)
    
    array_s = np.arange(5.0, 105.0, 5.0)
    array_t = np.arange(0.004, 1.004, 1.0 / 250)
    surface = np.zeros((len(array_s), len(array_t)))
    
    vanilla.CalcGreeksSurface(surface, "bs", "d", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True)
    #vanilla.CalcGreeksSurface(surface, "bs", "g", array_s, 50.0, 0.05, 0.0, 0.2, array_t)
    #vanilla.CalcGreeksSurface(surface, "bs", "v", array_s, 50.0, 0.05, 0.0, 0.2, array_t)
    #vanilla.CalcGreeksSurface(surface, "bs", "t", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True)
    #vanilla.CalcGreeksSurface(surface, "bs", "r", array_s, 50.0, 0.05, 0.0, 0.2, array_t, True, False, True)
    FigureResult(array_s, array_t, surface)
    
    vanilla.CalcGreeksSurface(surface, "bs", "d", array_s, 50.0, 0.05, 0.0, 0.2, array_t, False)
    #vanilla.CalcGreeksSurface(surface, "bs", "g", array_s, 50.0, 0.05, 0.0, 0.2, array_t)
    #vanilla.CalcGreeksSurface(surface, "bs", "v", array_s, 50.0, 0.05, 0.0, 0.2, array_t)
    #vanilla.CalcGreeksSurface(surface, "bs", "t", array_s, 50.0, 0.05, 0.0, 0.2, array_t, False)
    #vanilla.CalcGreeksSurface(surface, "bs", "r", array_s, 50.0, 0.05, 0.0, 0.2, array_t, False, False, True)
    FigureResult(array_s, array_t, surface)
    
    print(vanilla.GetError())

if __name__ == "__main__":
    Test_Vanilla_European()
