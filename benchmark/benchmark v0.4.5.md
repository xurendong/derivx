# Benchmark

### Version
DerivX V0.4.5 to V0.4.5

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
| rand_seed           | [0, ..., 24]                                       | use 1 - 24 threads |
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

### CalcPayoff (Turn off SMT (Hyper-Threading)):
| Threads | After Opt (s) | After Opt (ms/million/price) | Before Opt (s) | Before Opt (ms/million/price) | Percent (%) |
| :-----: | ------------: | ---------------------------: | -------------: | ----------------------------: | ----------: |
| 1       | 508.4295      | 1412.30                      | 835.944        | 60.821      |
| 2       | 222.2580      |  617.38                      | 507.977        | 43.754      |
| 3       | 154.9950      |  430.54                      | 394.977        | 39.242      |
| 4       | 120.4790      |  334.66                      | 354.352        | 34.000      |
| 5       |  98.9535      |  274.87                      | 335.574        | 29.488      |
| 6       |  90.1795      |  250.50                      | 317.240        | 28.426      |
| 8       |  74.7045      |  207.51                      | 302.594        | 24.688      |
| 9       |  65.1340      |  180.93                      | 301.359        | 21.613      |
| 10      |  69.2710      |  192.42                      | 304.820        | 22.725      |
| 12      |  53.3565      |  148.21                      | 313.900        | 16.998      |

### CalcPayoff (Turn on SMT (Hyper-Threading)):
| Threads | After Opt (s) | After Opt (ms/million/price) | Before Opt (s) | Before Opt (ms/million/price) | Percent (%) |
| :-----: | ------------: | ---------------------------: | -------------: | ----------------------------: | ----------: |
| 1       | 434.4775      |  | 792.797        |  | 54.803      |
| 2       | 225.2550      |  | 461.788        |  | 48.779      |
| 3       | 157.4240      |  | 335.781        |  | 46.883      |
| 4       | 122.4635      |  | 292.033        |  | 41.935      |
| 5       | 101.5020      |  | 260.722        |  | 38.931      |
| 6       |  88.4575      |  | 257.782        |  | 34.315      |
| 8       |  73.6720      |  | 242.623        |  | 30.365      |
| 9       |  68.3380      |  | 247.655        |  | 27.594      |
| 10      |  62.7545      |  | 243.931        |  | 25.726      |
| 12      |  59.2515      |  | 229.034        |  | 25.870      |
| 15      |  55.7285      |  | 236.646        |  | 23.549      |
| 16      |  54.1535      |  | 236.399        |  | 22.908      |
| 18      |  51.4915      |  | 235.929        |  | 21.825      |
| 20      |  49.1955      |  | 236.556        |  | 20.797      |
| 24      |  45.3750      |  | 241.292        |  | 18.805      |

### Optimization Result
![avatar](I:/Project/Public/DerivX/DerivX/benchmark/img_opt_ret_0.4.5_1.png)
