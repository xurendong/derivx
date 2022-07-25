# DerivX
V0.4.7-Beta Build 20220725

© 2021-2022 Xu Rendong. All Rights Reserved.

### Project Summary
Derivatives Pricing Engine.
+ Plain Vanilla European / American options portfolio calculation.
+ Plain Vanilla European / American option pricing and greek value calculation.
+ Single Barrier / SharkFin option pricing and greek value calculation.
+ Exotic Autocall Booster / Phoenix / Snowball option pricing and greek value calculation.
+ Stochastic Diffusion Processes and Stochastic Volatility Models.
+ Interfaces and examples for C++, Python, JavaScript.
+ Based on CyberX distributed heterogeneous computing framework.

### Install (version >= 0.4.0)
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

### Usage (version >= 0.4.0)
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

### Install (version < 0.4.0)
#### C++:
```bash

```

#### Python:
```bash
pip install derivx
```

#### JavaScript:
```bash
npm install derivx
```

### Usage (version < 0.4.0)
#### C++:
```c++

```

#### Python:
```python
import derivx
print(derivx.Version())
```
For more usages please refer to examples in [derivx_py](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_py) folder.

DerivX is not dependent on numpy, pandas and matplotlib, but if you want to run examples, you'd better install them with:
```bash
pip install numpy pandas matplotlib
```

#### JavaScript:
```javascript
const derivx = require('derivx')
console.log(derivx.Version())
```
For more usages please refer to examples in [derivx_js](https://github.com/xurendong/derivx/tree/main/exe/windows/bin/derivx_js) folder.

DerivX is not dependent on numjs, but if you want to run examples, you'd better install it with:
```bash
npm install git+https://github.com/nicolaspanel/numjs.git
```

### Changes
Please refer to [changes](https://github.com/xurendong/derivx/blob/main/changes.txt) file.

### Benchmark
Please refer to [benchmark](https://github.com/xurendong/derivx/blob/main/benchmark.md) file.

### Contact Information
QQ: 277195007, WeChat: xrd_ustc, E-mail: xrd@ustc.edu
