# DerivX
V0.2.7-Beta Build 20210813

© 2021-2021 Xu Rendong. All Rights Reserved.

### Project Summary
Derivatives Pricing Engine.

### Install
##### C++:
```bash

```

##### Python:
```bash
pip install derivx
```

##### JavaScript:
```bash
npm install derivx
```

### Usage
##### C++:
```c++

```

##### Python:
```python
import derivx
print(derivx.Version())
```
For more usages please refer to test files in [derivx_py](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_py) folder.

DerivX is not dependent on numpy, pandas and matplotlib, but if you want to run tests, you'd better install them with:
```bash
pip install numpy pandas matplotlib
```

##### JavaScript:
```javascript
const derivx = require('derivx')
console.log(derivx.Version())
```
For more usages please refer to test files in [derivx_js](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_js) folder.

DerivX is not dependent on numjs, but if you want to run tests, you'd better install it with:
```bash
npm install git+https://github.com/nicolaspanel/numjs.git
```

### Benchmark
##### Environment:
+ CPU: Intel Core i7-4790 4C/8T 3.60GHz
+ RAM: 16.0GB
+ SYS: Windows 10 Pro 64-bit 20H2 19042.1110

##### Parameters:
+ rand_rows: 500000
+ rand_cols: 250
+ rand_seed: { 0, 1, 2, 3, 4, 5, 6, 7 }
+ dual_smooth: true
+ runs_size: 1000000
+ runs_step: 244

##### C++:
+ InitRand: 461ms - 550ms
+ InitPath: 1575ms - 1961ms

Autocall Snowball:

+ CalcCoupon: 468ms - 564ms (there is still 200ms optimization space)
+ CalcPayoff: 965ms - 983ms per price
+ CalcDelta: 1932ms - 1983ms per price
+ CalcGamma: 2898ms - 2918ms per price
+ CalcVega: 2047ms - 2073ms per price
+ CalcTheta: 1636ms - 1647ms per price
+ CalcRho: 2106ms - 2161ms per price

### Contact Information
QQ: 277195007, WeChat: xrd_ustc, E-mail: xrd@ustc.edu
