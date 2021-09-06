# DerivX
V0.3.2-Beta Build 20210906

© 2021-2021 Xu Rendong. All Rights Reserved.

### Project Summary
Derivatives Pricing Engine.
+ Plain Vanilla European / American options portfolio calculation.
+ Plain Vanilla European / American option pricing and greek value calculation.
+ Exotic Autocall Phoenix / Snowball option pricing and greek value calculation.
+ Interfaces and examples for C++, Python, JavaScript.

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
For more usages please refer to examples in [derivx_py](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_py) folder.

DerivX is not dependent on numpy, pandas and matplotlib, but if you want to run examples, you'd better install them with:
```bash
pip install numpy pandas matplotlib
```

##### JavaScript:
```javascript
const derivx = require('derivx')
console.log(derivx.Version())
```
For more usages please refer to examples in [derivx_js](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_js) folder.

DerivX is not dependent on numjs, but if you want to run examples, you'd better install it with:
```bash
npm install git+https://github.com/nicolaspanel/numjs.git
```

### Benchmark
##### Environment:
| Module | Specification                         |
| :----: | :------------------------------------ |
| CPU    | Intel Core i7-4790 4C/8T 3.60GHz      |
| RAM    | 16.0GB DDR3 800MHz Dual               |
| SYS    | Windows 10 Pro 64-bit 20H2 19042.1110 |

##### Parameters:
| Parameter   | Value  |
| :---------- | :----: |
| rand_rows   | 500000 |
| rand_cols   | 250 |
| rand_seed   | { 0, 1, 2, 3, 4, 5, 6, 7 } |
| dual_smooth | true |
| runs_size   | 1000000 |
| runs_step   | 244 |
| run_from    | 0 |
| run_days    | 1 |

##### C++:
| Function | Min    | Max    |
| :------- | -----: | -----: |
| InitRand |  461ms |  550ms |
| InitPath | 1575ms | 1961ms |

&nbsp;&nbsp;&nbsp;&nbsp;Autocall Snowball:

| Function   | Min    | Max    | Unit      | Note |
| :--------- | -----: | -----: | :-------: | :--: |
| CalcCoupon |  468ms |  564ms | -         | 1    |
| CalcPayoff |  965ms |  983ms | per price | -    |
| CalcDelta  | 1932ms | 1983ms | per price | -    |
| CalcGamma  | 2898ms | 2918ms | per price | -    |
| CalcVega   | 2047ms | 2073ms | per price | -    |
| CalcTheta  | 1636ms | 1647ms | per price | 2    |
| CalcRho    | 2106ms | 2161ms | per price | -    |
1. There is still 200ms optimization space.
2. As run_days increases this tends to CalcPayoff's time consumption.
3. The difference between CalcCoupon and CalcPayoff shows that different prices and barriers will cause different time consumption.

### Contact Information
QQ: 277195007, WeChat: xrd_ustc, E-mail: xrd@ustc.edu
