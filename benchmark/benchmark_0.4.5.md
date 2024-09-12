# Benchmark

### Version
DerivX V0.4.5 to V0.6.2

### Environment:
| Module | Specification                            |
| :----: | :--------------------------------------- |
| CPU    | AMD Ryzen 9 5900X 12C/24T 3.7GHz-4.8GHz  |
| RAM    | Corsair 64GB DDR4 1600MHz Dual (3200MHz) |
| SSD    | SAMSUNG 980 Pro NVMe M.2 1TB             |
| SYS    | Windows 10 Ent 64-bit 21H1 19043.1237    |

### Parameters: (Autocall Snowball)
| Parameter           | Value                                              | Note               |
| :------------------ | :------------------------------------------------: | :----------------: |
| rand_rows           | 3600000                                            | -                  |
| rand_cols           | 250                                                | -                  |
| rand_quasi          | false                                              | -                  |
| rand_seed           | [0, ..., 23]                                       | use 1 - 24 threads |
| dual_smooth         | true                                               | -                  |
| runs_size           | 7200000                                            | -                  |
| runs_step           | 244                                                | -                  |
| year_days           | 244                                                | -                  |
| sigma               | 0.16                                               | -                  |
| risk_free_rate      | 0.03                                               | -                  |
| basis_rate          | 0.05                                               | -                  |
| price_limit_ratio   | 0.1                                                | -                  |
| price_limit_style   | 0                                                  | -                  |
| notional            | 100000.0                                           | -                  |
| trade_long          | false                                              | -                  |
| start_price         | 100.0                                              | -                  |
| strike_price        | 100.0                                              | -                  |
| knock_o_ratio       | 1.0                                                | -                  |
| knock_i_ratio       | 0.7                                                | -                  |
| knock_o_steps       | 0.0                                                | -                  |
| knock_i_valid       | true                                               | -                  |
| knock_i_occur       | false                                              | -                  |
| knock_i_margin_call | true                                               | -                  |
| coupon_rate         | 0.11                                               | -                  |
| margin_rate         | 1.0                                                | -                  |
| margin_interest     | 0.03                                               | -                  |
| prefix_coupon       | 0.0                                                | -                  |
| prefix_coupon_ann   | false                                              | -                  |
| prefix_coupon_use   | false                                              | -                  |
| ukiuko_coupon       | 0.0                                                | -                  |
| ukiuko_coupon_ann   | false                                              | -                  |
| ukiuko_coupon_use   | false                                              | -                  |
| knock_o_days        | [61, 81, 101, 122, 142, 162, 183, 203, 223, 244]   | -                  |
| knock_o_rate        | [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0] | -                  |
| calc_price          | [66, ..., 115]                                     | 50 price points    |
| run_from            | 0                                                  | -                  |
| run_days            | 1                                                  | -                  |

### CalcPayoff: (Turn off SMT / Hyper-Threading)
<table>
    <tr><th rowspan="2">Threads</th><th>Before Opt</th><th>Before Opt</th><th>After Opt</th><th>After Opt</th><th>Percent</th></tr>
    <tr><th>(s)</th><th>(ms/million/price)</th><th>(s)</th><th>(ms/million/price)</th><th>(%)</th></tr>
    <tr align="center"><td> 1</td><td>835.944</td><td>2322.07</td><td>508.4295</td><td>1412.30</td><td>60.821</td></tr>
    <tr align="center"><td> 2</td><td>507.977</td><td>1411.05</td><td>222.2580</td><td> 617.38</td><td>43.754</td></tr>
    <tr align="center"><td> 3</td><td>394.977</td><td>1097.16</td><td>154.9950</td><td> 430.54</td><td>39.242</td></tr>
    <tr align="center"><td> 4</td><td>354.352</td><td> 984.31</td><td>120.4790</td><td> 334.66</td><td>34.000</td></tr>
    <tr align="center"><td> 5</td><td>335.574</td><td> 932.15</td><td> 98.9535</td><td> 274.87</td><td>29.488</td></tr>
    <tr align="center"><td> 6</td><td>317.240</td><td> 881.22</td><td> 90.1795</td><td> 250.50</td><td>28.426</td></tr>
    <tr align="center"><td> 8</td><td>302.594</td><td> 840.54</td><td> 74.7045</td><td> 207.51</td><td>24.688</td></tr>
    <tr align="center"><td> 9</td><td>301.359</td><td> 837.11</td><td> 65.1340</td><td> 180.93</td><td>21.613</td></tr>
    <tr align="center"><td>10</td><td>304.820</td><td> 846.72</td><td> 69.2710</td><td> 192.42</td><td>22.725</td></tr>
    <tr align="center"><td>12</td><td>313.900</td><td> 871.94</td><td> 53.3565</td><td> 148.21</td><td>16.998</td></tr>
</table>

### CalcPayoff: (Turn on SMT / Hyper-Threading)
<table>
    <tr><th rowspan="2">Threads</th><th>Before Opt</th><th>Before Opt</th><th>After Opt</th><th>After Opt</th><th>Percent</th></tr>
    <tr><th>(s)</th><th>(ms/million/price)</th><th>(s)</th><th>(ms/million/price)</th><th>(%)</th></tr>
    <tr align="center"><td> 1</td><td>792.797</td><td>2202.21</td><td>434.4775</td><td>1206.88</td><td>54.803</td></tr>
    <tr align="center"><td> 2</td><td>461.788</td><td>1282.74</td><td>225.2550</td><td> 625.71</td><td>48.779</td></tr>
    <tr align="center"><td> 3</td><td>335.781</td><td> 932.73</td><td>157.4240</td><td> 437.29</td><td>46.883</td></tr>
    <tr align="center"><td> 4</td><td>292.033</td><td> 811.20</td><td>122.4635</td><td> 340.18</td><td>41.935</td></tr>
    <tr align="center"><td> 5</td><td>260.722</td><td> 724.23</td><td>101.5020</td><td> 281.95</td><td>38.931</td></tr>
    <tr align="center"><td> 6</td><td>257.782</td><td> 716.06</td><td> 88.4575</td><td> 245.72</td><td>34.315</td></tr>
    <tr align="center"><td> 8</td><td>242.623</td><td> 673.95</td><td> 73.6720</td><td> 204.64</td><td>30.365</td></tr>
    <tr align="center"><td> 9</td><td>247.655</td><td> 687.93</td><td> 68.3380</td><td> 189.83</td><td>27.594</td></tr>
    <tr align="center"><td>10</td><td>243.931</td><td> 677.59</td><td> 62.7545</td><td> 174.32</td><td>25.726</td></tr>
    <tr align="center"><td>12</td><td>229.034</td><td> 636.21</td><td> 59.2515</td><td> 164.59</td><td>25.870</td></tr>
    <tr align="center"><td>15</td><td>236.646</td><td> 657.35</td><td> 55.7285</td><td> 154.80</td><td>23.549</td></tr>
    <tr align="center"><td>16</td><td>236.399</td><td> 656.66</td><td> 54.1535</td><td> 150.43</td><td>22.908</td></tr>
    <tr align="center"><td>18</td><td>235.929</td><td> 655.36</td><td> 51.4915</td><td> 143.03</td><td>21.825</td></tr>
    <tr align="center"><td>20</td><td>236.556</td><td> 657.10</td><td> 49.1955</td><td> 136.65</td><td>20.797</td></tr>
    <tr align="center"><td>24</td><td>241.292</td><td> 670.26</td><td> 45.3750</td><td> 126.04</td><td>18.805</td></tr>
</table>

### Optimization Result
![avatar](https://github.com/xurendong/derivx/blob/main/benchmark/img_opt_ret_0.4.5_1.png?raw=true)
