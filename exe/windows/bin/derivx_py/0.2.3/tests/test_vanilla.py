
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
import pandas as pd
import matplotlib.pyplot as plt

import derivx

def Test_Vanilla():
    vanilla = derivx.Vanilla("European") # American | European
    
    # CalcPayoff(model, s, k, r, q, sigma, t, is_call)
    # CalcGreeks(model, greek, s, k, r, q, sigma, t, is_call, is_futures, is_foreign)
    
    result = vanilla.CalcPayoff("bs", 100.0, 100.0, 0.03, 0.08 - 0.03, 0.15, 1.0, True)
    #result = vanilla.CalcPayoff("bs", 42, 40, 0.1, 0.0, 0.2, 0.5, True)
    #result = vanilla.CalcGreeks("bs", "d", 49, 50, 0.05, 0.0, 0.2, 0.3846, True)
    #result = vanilla.CalcGreeks("bs", "g", 49, 50, 0.05, 0.0, 0.2, 0.3846)
    #result = vanilla.CalcGreeks("bs", "v", 49, 50, 0.05, 0.0, 0.2, 0.3846)
    #result = vanilla.CalcGreeks("bs", "t", 49, 50, 0.05, 0.0, 0.2, 0.3846, True)
    #result = vanilla.CalcGreeks("bs", "r", 49, 50, 0.05, 0.0, 0.2, 0.3846, True, False, False)
    print(result)
    
    result = vanilla.CalcPayoff("bs", 100.0, 100.0, 0.03, 0.08 + 0.03, 0.22, 1.0, False)
    #result = vanilla.CalcPayoff("bs", 42, 40, 0.1, 0.0, 0.2, 0.5, False)
    #result = vanilla.CalcGreeks("bs", "d", 49, 50, 0.05, 0.0, 0.2, 0.3846, False)
    #result = vanilla.CalcGreeks("bs", "g", 49, 50, 0.05, 0.0, 0.2, 0.3846)
    #result = vanilla.CalcGreeks("bs", "v", 49, 50, 0.05, 0.0, 0.2, 0.3846)
    #result = vanilla.CalcGreeks("bs", "t", 49, 50, 0.05, 0.0, 0.2, 0.3846, False)
    #result = vanilla.CalcGreeks("bs", "r", 49, 50, 0.05, 0.0, 0.2, 0.3846, False, False, False)
    print(result)
    
    print(vanilla.GetError())

if __name__ == "__main__":
    Test_Vanilla()
