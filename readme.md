# DerivX
V0.5.12-Beta Build 20240524

最新版本：[C++](https://github.com/xurendong/derivx/tree/main/exe/windows/bin)、[Python](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_py/0.5.12)、[JavaScript](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_js/0.5.12)

### 项目概述
定价引擎特性：
+ 普通欧式和美式香草期权定价及希腊值计算；
+ 普通欧式和美式香草期权组合计算；
+ 单障碍、鲨鱼鳍、安全气囊等障碍型奇异期权定价及希腊值计算；
+ 助推器、定息票据、普通凤凰、普通雪球等单标的自动赎回奇异期权定价及希腊值计算；
+ 彩虹雪球等多标的自动赎回奇异期权定价及希腊值计算；
+ 方便进行随机扩散过程和随机波动模型研究；
+ 提供适配 C++、Python、JavaScript 等开发语言的接口和示例；
+ 基于 CyberX 高性能分布式异构计算框架 灵活构建。

定价插件简介：
+ derivx_autocall_booster：
  + 助推器（Booster）类型（奇异期权）定价及希腊值计算。
  + 使用示例：test_derivx_autocall_booster（[Python](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_py/0.5.12/test_derivx_autocall_booster.py)、[JavaScript](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_js/0.5.12/test_derivx_autocall_booster.js)）
###
+ derivx_autocall_fixed_coupon_notes：
  + 定息票据（Fixed Coupon Notes）类型（奇异期权）定价及希腊值计算。
  + 使用示例：test_derivx_autocall_fixed_coupon_notes（[Python](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_py/0.5.12/test_derivx_autocall_fixed_coupon_notes.py)、[JavaScript](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_js/0.5.12/test_derivx_autocall_fixed_coupon_notes.js)）
###
+ derivx_autocall_phoenix：
  + 普通凤凰（Phoenix）类型（奇异期权）定价及希腊值计算。
  + 使用示例：test_derivx_autocall_phoenix（[Python](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_py/0.5.12/test_derivx_autocall_phoenix.py)、[JavaScript](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_js/0.5.12/test_derivx_autocall_phoenix.js)）
###
+ derivx_autocall_snowball：
  + 普通雪球（Snowball）类型（奇异期权）定价及希腊值计算。
  + 使用示例：test_derivx_autocall_snowball（[Python](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_py/0.5.12/test_derivx_autocall_snowball.py)、[JavaScript](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_js/0.5.12/test_derivx_autocall_snowball.js)）
###
+ derivx_autocall_snowball_gpu：
  + 普通雪球（Snowball）类型（奇异期权）定价及希腊值计算。
  + 使用示例：test_derivx_autocall_snowball_gpu（[Python](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_py/0.5.12/test_derivx_autocall_snowball_gpu.py)、[JavaScript](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_js/0.5.12/test_derivx_autocall_snowball_gpu.js)）
###
+ derivx_autocall_snowball_stage_coupon：
  + 早利雪球（Snowball）类型（奇异期权）定价及希腊值计算。
  + 使用示例：test_derivx_autocall_snowball_stage_coupon（[Python](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_py/0.5.12/test_derivx_autocall_snowball_stage_coupon.py)、[JavaScript](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_js/0.5.12/test_derivx_autocall_snowball_stage_coupon.js)）
###
+ derivx_autocall_snowball_rainbow：
  + 彩虹雪球（Rainbow Snowball）类型（多标的奇异期权）定价及希腊值计算。
  + 使用示例：test_derivx_autocall_snowball_rainbow（[Python](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_py/0.5.12/test_derivx_autocall_snowball_rainbow.py)、[JavaScript](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_js/0.5.12/test_derivx_autocall_snowball_rainbow.js)）
###
+ derivx_barrier_airbag：
  + 安全气囊（Airbag）类型（奇异期权）定价及希腊值计算。
  + 使用示例：test_derivx_barrier_airbag（[Python](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_py/0.5.12/test_derivx_barrier_airbag.py)、[JavaScript](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_js/0.5.12/test_derivx_barrier_airbag.js)）
###
+ derivx_barrier_sharkfin：
  + 鲨鱼鳍（SharkFin）类型（奇异期权）定价及希腊值计算。
  + 使用示例：test_derivx_barrier_sharkfin（[Python](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_py/0.5.12/test_derivx_barrier_sharkfin.py)、[JavaScript](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_js/0.5.12/test_derivx_barrier_sharkfin.js)）
###
+ derivx_barrier_single：
  + 单障碍（Single Barrier）类型（奇异期权）定价及希腊值计算。
  + 使用示例：test_derivx_barrier_single（[Python](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_py/0.5.12/test_derivx_barrier_single.py)、[JavaScript](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_js/0.5.12/test_derivx_barrier_single.js)）
###
+ derivx_digital_simple：
  + 数字（Digital）类型（奇异期权）定价及希腊值计算。
  + 使用示例：test_derivx_digital_simple（[Python](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_py/0.5.12/test_derivx_digital_simple.py)、[JavaScript](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_js/0.5.12/test_derivx_digital_simple.js)）
###
+ derivx_stochastic_model：
  + 部分随机扩散过程和随机波动模型实现及演示。
  + 使用示例：test_derivx_stochastic_model（[Python](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_py/0.5.12/test_derivx_stochastic_model.py)、[JavaScript](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_js/0.5.12/test_derivx_stochastic_model.js)）
###
+ derivx_vanilla_american：
  + 普通美式香草（Plain Vanilla American）类型（普通期权）定价及希腊值计算。
  + 使用示例：test_derivx_vanilla_american（[Python](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_py/0.5.12/test_derivx_vanilla_american.py)、[JavaScript](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_js/0.5.12/test_derivx_vanilla_american.js)）
###
+ derivx_vanilla_european：
  + 普通欧式香草（Plain Vanilla European）类型（普通期权）定价及希腊值计算。
  + 使用示例：test_derivx_vanilla_european（[Python](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_py/0.5.12/test_derivx_vanilla_european.py)、[JavaScript](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_js/0.5.12/test_derivx_vanilla_european.js)）
###

其他示例简介：
+ remote：
  + 分布式计算调用简单演示。
  + 使用示例：test_remote（[Python](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_py/0.5.12/test_remote.py)、[JavaScript](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_js/0.5.12/test_remote.js)）
###
+ remote_derivx_autocall_snowball：
  + 分布式计算调用普通雪球定价及希腊值计算。
  + 使用示例：test_remote_derivx_autocall_snowball（[Python](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_py/0.5.12/test_remote_derivx_autocall_snowball.py)、[JavaScript](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_js/0.5.12/test_remote_derivx_autocall_snowball.js)）
###

### 安装框架（建议安装最新版本）
#### C++:
```bash

```

#### Python:
```bash
pip install cyberx
```

#### JavaScript:
```bash
npm install cyberx-js
```

### 运行示例（建议运行最新版本）
#### C++:
```c++

```

#### Python:
Visit the latest version folder in [derivx_py](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_py), download the following items to a folder:

+ plugins (entire folder)
+ matlib.dll
+ syscfg.py
+ tasker.py
+ test_xxxx.py (all examples)

Edit syscfg.py and change 
```python
# the folder's absolute path, like "C:\\Users\\UserName\\Desktop\\Test"
self.work_path = ""
# your CPU's logic cores number, like 4
self.local_cpu_thread = 8
```
then open and run examples in Shell or a Python IDE.

DerivX is not dependent on numpy, pandas and matplotlib, but if you want to run examples, you'd better install them with:
```bash
pip install numpy pandas matplotlib
```

#### JavaScript:
Visit the latest version folder in [derivx_js](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_js), download the following items to a folder:

+ plugins (entire folder)
+ matlib.dll
+ syscfg.js
+ tasker.js
+ test_xxxx.js (all examples)

Edit syscfg.js and change 
```javascript
// the folder's absolute path, like 'C:\\Users\\UserName\\Desktop\\Test'
this.work_path = ''
// your CPU's logic cores number, like 4
this.local_cpu_thread = 8
```
then open and run examples in Shell or a JavaScript IDE.

DerivX is not dependent on numjs, but if you want to run examples, you'd better install it with:
```bash
npm install numjs
```

### 其他说明
+ 目前暂只支持 Windows 环境运行，Linux 后续有时间会支持，MacOS 没有计划。

### 更新日志
请参考 [更新日志](https://github.com/xurendong/derivx/blob/main/changes.txt) 文件。

### 性能测试
请参考 [性能测试](https://github.com/xurendong/derivx/blob/main/benchmark.md) 文件。

### 联系作者
WeChat：xrd_ustc，~~QQ：277195007~~，~~E-mail：xrd@ustc.edu~~

© 2021-2024 Rendong Xu All Rights Reserved.
