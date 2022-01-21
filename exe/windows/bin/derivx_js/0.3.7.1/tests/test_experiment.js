/*
* Copyright (c) 2021-2022 the DerivX authors
* All rights reserved.
*
* The project sponsor and lead author is Xu Rendong.
* E-mail: xrd@ustc.edu, QQ: 277195007, WeChat: xrd_ustc
* See the contributors file for names of other contributors.
*
* Commercial use of this code in source and binary forms is
* governed by a LGPL v3 license. You may get a copy from the
* root directory. Or else you should get a specific written
* permission from the project author.
*
* Individual and educational use of this code in source and
* binary forms is governed by a 3-clause BSD license. You may
* get a copy from the root directory. Certainly welcome you
* to contribute code of all sorts.
*
* Be sure to retain the above copyright notice and conditions.
*/

'use strict'

const nj = require('numjs')

const derivx = require('derivx')

function Test_01() {
    let experiment = new derivx.Experiment()
    let array_11 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    let array_12 = []
    let result = experiment.Test_Array_D1(array_11, array_12)
    console.log(result)
    console.log(array_12)
}

function Test_Experiment() {
    Test_01()
}

Test_Experiment()
