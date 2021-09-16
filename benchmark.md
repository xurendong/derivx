# DerivX
V0.3.1-Beta Build 20210903

### Environment:
| Module | Specification                         |
| :----: | :------------------------------------ |
| CPU    | Intel Core i7-4790 4C/8T 3.6-4.0GHz   |
| RAM    | 16.0GB DDR3 800MHz Dual (1600MHz)     |
| SYS    | Windows 10 Pro 64-bit 20H2 19042.1110 |

### Parameters:
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

### C++:
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

### Environment:
| Module | Specification                              |
| :----: | :----------------------------------------- |
| CPU    | AMD Ryzen 9 5900X 12C/24T 3.7-4.8GHz       |
| RAM    | Corsair 64.0GB DDR4 1600MHz Dual (3200MHz) |
| SSD    | SAMSUNG 980 Pro NVMe M.2 1TB               |
| SYS    | Windows 10 Ent 64-bit 21H1 19043.1165      |

### Parameters:
TBD...
