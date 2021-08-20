
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

def Test_Vanilla_American():
    vanilla = derivx.Vanilla("American")
    
    # CalcPrice(model, s, k, r, q, sigma, t, is_call)
    # CalcGreeks(model, greek, s, k, r, q, sigma, t, is_long, is_call, is_futures, is_foreign)
    # CalcGreeksSurface(surface, model, greek, s, k, r, q, sigma, t, is_long, is_call, is_futures, is_foreign)
    
    print(vanilla.GetError())

if __name__ == "__main__":
    Test_Vanilla_American()
