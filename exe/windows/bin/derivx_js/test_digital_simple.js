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

const derivx = require('derivx')

class Config_Gap {
    constructor() {
        this.s = 0.0 // 标的价格
        this.k_1 = 0.0 // 行权价格
        this.k_2 = 0.0 // 行权价格
        this.r = 0.0 // 无风险利率
        this.q = 0.0 // 年化分红率
        this.v = 0.0 // 波动率
        this.t = 0.0 // 年化到期期限
        this.is_call = true // 看涨看跌
    }
}

class Config_CashOrNothing {
    constructor() {
        this.s = 0.0 // 标的价格
        this.k = 0.0 // 行权价格
        this.r = 0.0 // 无风险利率
        this.q = 0.0 // 年化分红率
        this.v = 0.0 // 波动率
        this.t = 0.0 // 年化到期期限
        this.cash = 0.0 // 现金回报
        this.is_call = true // 看涨看跌
    }
}

class Config_AssetOrNothing {
    constructor() {
        this.s = 0.0 // 标的价格
        this.k = 0.0 // 行权价格
        this.r = 0.0 // 无风险利率
        this.q = 0.0 // 年化分红率
        this.v = 0.0 // 波动率
        this.t = 0.0 // 年化到期期限
        this.is_call = true // 看涨看跌
    }
}

class Config_SuperShare {
    constructor() {
        this.s = 0.0 // 标的价格
        this.k_l = 0.0 // 低端行权价格
        this.k_h = 0.0 // 高端行权价格
        this.r = 0.0 // 无风险利率
        this.q = 0.0 // 年化分红率
        this.v = 0.0 // 波动率
        this.t = 0.0 // 年化到期期限
    }
}

function Test_Digital_Simple() {
    let digital = null, config = null
    
    digital = new derivx.Digital("Gap")
    
    config = new Config_Gap()
    config.k_1 = 50.0 // 行权价格
    config.k_2 = 57.0 // 行权价格
    config.r = 0.09 // 无风险利率
    config.q = 0.0 // 年化分红率
    config.v = 0.2 // 波动率
    config.t = 0.5 // 年化到期期限
    config.is_call = true // 看涨看跌
    
    config.s = 50.0 // 标的价格
    if(digital.InitArgs(config) < 0) {
        console.log(digital.GetError())
        return
    }
    console.log("price:", digital.CalcPrice())
    
    config.s = 55.0 // 标的价格
    if(digital.InitArgs(config) < 0) {
        console.log(digital.GetError())
        return
    }
    console.log("payoff:", digital.CalcPayoff())
    
    //////////////////////////////////////////////////
    
    digital = new derivx.Digital("CashOrNothing")
    
    config = new Config_CashOrNothing()
    config.s = 100.0 // 标的价格
    config.k = 80.0 // 行权价格
    config.r = 0.06 // 无风险利率
    config.q = 0.06 // 年化分红率
    config.v = 0.35 // 波动率
    config.t = 0.75 // 年化到期期限
    config.cash = 10.0 // 现金回报
    
    config.is_call = false // 看涨看跌
    if(digital.InitArgs(config) < 0) {
        console.log(digital.GetError())
        return
    }
    console.log("price:", digital.CalcPrice())
    
    config.is_call = true // 看涨看跌
    if(digital.InitArgs(config) < 0) {
        console.log(digital.GetError())
        return
    }
    console.log("payoff:", digital.CalcPayoff())
    
    //////////////////////////////////////////////////
    
    digital = new derivx.Digital("AssetOrNothing")
    
    config = new Config_AssetOrNothing()
    config.s = 70.0 // 标的价格
    config.k = 65.0 // 行权价格
    config.r = 0.07 // 无风险利率
    config.q = 0.05 // 年化分红率
    config.v = 0.27 // 波动率
    config.t = 0.5 // 年化到期期限
    
    config.is_call = false // 看涨看跌
    if(digital.InitArgs(config) < 0) {
        console.log(digital.GetError())
        return
    }
    console.log("price:", digital.CalcPrice())
    
    config.is_call = true // 看涨看跌
    if(digital.InitArgs(config) < 0) {
        console.log(digital.GetError())
        return
    }
    console.log("payoff:", digital.CalcPayoff())
    
    //////////////////////////////////////////////////
    
    digital = new derivx.Digital("SuperShare")
    
    config = new Config_SuperShare()
    config.s = 100.0 // 标的价格
    config.k_l = 90.0 // 低端行权价格
    config.k_h = 110.0 // 高端行权价格
    config.r = 0.1 // 无风险利率
    config.q = 0.1 // 年化分红率
    config.v = 0.2 // 波动率
    config.t = 0.25 // 年化到期期限
    
    if(digital.InitArgs(config) < 0) {
        console.log(digital.GetError())
        return
    }
    console.log("price:", digital.CalcPrice())
    
    if(digital.InitArgs(config) < 0) {
        console.log(digital.GetError())
        return
    }
    console.log("payoff:", digital.CalcPayoff())
}

Test_Digital_Simple()
