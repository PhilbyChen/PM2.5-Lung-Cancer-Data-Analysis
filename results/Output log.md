PM2.5 （微克每立方米）:
mean      55.557278
std       17.514926
min       21.605333
25%       42.864085
50%       53.371453
75%       64.722948
max      108.338356
Name: PM2.5 （微克每立方米）, dtype: float64

男:
mean      49.494331
std       14.710345
min       10.520000
25%       40.770000
50%       47.830000
75%       57.250000
max      103.080000
Name: 男, dtype: float64

女:
mean      23.333058
std        8.786709
min        4.260000
25%       17.480000
50%       22.550000
75%       26.610000
max       55.020000



男/女与PM2.5散点图显示出较弱的线性关系，其中有少量值离大多数数据点较远

==================================================



PM2.5 （微克每立方米）列:
  样本量: 121
  K²统计量: 6.4067
  P值: 0.040625
  结论: 不符合正态分布 (p ≤ 0.05)

男列:
  样本量: 121
  K²统计量: 30.5059
  P值: 0.000000
  结论: 不符合正态分布 (p ≤ 0.05)

女列:
  样本量: 121
  K²统计量: 27.8431
  P值: 0.000001
  结论: 不符合正态分布 (p ≤ 0.05)



检验总结:
PM2.5 （微克每立方米）列: 不符合正态分布 (p=0.040625)
男列: 不符合正态分布 (p=0.000000)
女列: 不符合正态分布 (p=0.000001)

==================================================



`斯皮尔曼相关系数`
============================================================
`有效样本量: 121`

`=== 斯皮尔曼相关系数结果 ===`
`PM2.5 vs 男性肺癌发病率:`
  `相关系数: 0.220`
  `P值: 0.015146`
  `显著性: 显著`

`PM2.5 vs 女性肺癌发病率:`
  `相关系数: 0.178`
  `P值: 0.050252`
  `显著性: 不显著`

`男性 vs 女性肺癌发病率:`
  `相关系数: 0.650`
  `P值: 0.000000`



`结果解释`

`男性肺癌发病率与PM2.5:`
  `正相关，弱相关`
  `统计显著 (p=0.015)`

`女性肺癌发病率与PM2.5:`
  `正相关，弱相关`
  `统计不显著 (p=0.050)`

`男女肺癌发病率与PM2.5的相关性强度相近`



`spearman相关系数矩阵:`
`Longitude  Latitude     PM2.5      Male    Female`
`Longitude   1.000000  0.404796  0.272870  0.298607  0.443612`
`Latitude    0.404796  1.000000  0.467281  0.167661  0.302771`
`PM2.5       0.272870  0.467281  1.000000  0.220371  0.178404`
`Male        0.298607  0.167661  0.220371  1.000000  0.650458`
`Female      0.443612  0.302771  0.178404  0.650458  1.000000`

`=======================================================`

`斯皮尔曼相关系数结果（含95%置信区间）`
======================================================================

1. `PM2.5 vs 男性肺癌发病率:`
   `相关系数 ρ = 0.220`
   `95%置信区间: [0.026, 0.407]`
   `P值 = 0.0151`
   `显著性: ✅ 显著`

2. `PM2.5 vs 女性肺癌发病率:`
   `相关系数 ρ = 0.178`
   `95%置信区间: [-0.006, 0.363]`
   `P值 = 0.0503`
   `显著性: ⚠️ 不显著`

3. `男性 vs 女性肺癌发病率:`
   `相关系数 ρ = 0.650`
   `95%置信区间: [0.528, 0.751]`
   `P值 = 0.0000`
   `显著性: ✅ 显著`

`======================================================================`
### `相关性强度解读`

`PM2.5与男性发病率: 弱相关 (ρ = 0.220)`
`PM2.5与女性发病率: 弱相关 (ρ = 0.178)`
`男性与女性发病率: 强相关 (ρ = 0.650)`

# 斯皮尔曼相关系数

男性:
  斯皮尔曼相关: ρ = 0.220 (95%CI [0.031, 0.400])
  相对风险: RR = 1.014 (95%CI [1.011, 1.016])

女性:
  斯皮尔曼相关: ρ = 0.178 (95%CI [-0.002, 0.368])
  相对风险: RR = 1.009 (95%CI [1.005, 1.013])

# 泊松回归

总人群泊松回归结果:
  PM2.5系数 β = 0.001080 (95%CI [0.000852, 0.001308])
  每1μg/m³ RR = 1.0011 (95%CI [1.0009, 1.0013])
  每10μg/m³ RR = 1.0109 (95%CI [1.0086, 1.0132])
  P值 = 0.0000

男性泊松回归结果:
  PM2.5系数 β = 0.001360 (95%CI [0.001085, 0.001636])
  每1μg/m³ RR = 1.0014 (95%CI [1.0011, 1.0016])
  每10μg/m³ RR = 1.0137 (95%CI [1.0109, 1.0165])
  P值 = 0.0000

女性泊松回归结果:
  PM2.5系数 β = 0.000892 (95%CI [0.000486, 0.001298])
  每1μg/m³ RR = 1.0009 (95%CI [1.0005, 1.0013])
  每10μg/m³ RR = 1.0090 (95%CI [1.0049, 1.0131])
  P值 = 0.0000



## CORE PAF ANALYSIS

1. EXPOSURE-RESPONSE RELATIONSHIP FITTING

=== TOTAL EXPOSURE-RESPONSE RELATIONSHIP ===
PM2.5 coefficient (β): 0.001080
Relative Risk (RR) = exp(β) = 1.001081
RR per 1 μg/m³ increase: 1.0011
RR per 10 μg/m³ increase: 1.0109
P-value: 0.000000
✅ Statistically significant (p < 0.05)

=== MALE EXPOSURE-RESPONSE RELATIONSHIP ===
PM2.5 coefficient (β): 0.001360
Relative Risk (RR) = exp(β) = 1.001361
RR per 1 μg/m³ increase: 1.0014
RR per 10 μg/m³ increase: 1.0137
P-value: 0.000000
✅ Statistically significant (p < 0.05)

=== FEMALE EXPOSURE-RESPONSE RELATIONSHIP ===
PM2.5 coefficient (β): 0.000892
Relative Risk (RR) = exp(β) = 1.000893
RR per 1 μg/m³ increase: 1.0009
RR per 10 μg/m³ increase: 1.0090
P-value: 0.000016
✅ Statistically significant (p < 0.05)

2. POPULATION ATTRIBUTABLE FRACTION (PAF) CALCULATION

=== TOTAL PAF CALCULATION ===
TMREL (reference level): 5.0 μg/m³
Average PM2.5 concentration: 55.56 μg/m³
Population Attributable Fraction (PAF): 0.0572 (5.72%)
Total cases: 223680
Avoidable cases: 12802

=== MALE PAF CALCULATION ===
TMREL (reference level): 5.0 μg/m³
Average PM2.5 concentration: 55.56 μg/m³
Population Attributable Fraction (PAF): 0.0714 (7.14%)
Total cases: 152932
Avoidable cases: 10927

=== FEMALE PAF CALCULATION ===
TMREL (reference level): 5.0 μg/m³
Average PM2.5 concentration: 55.56 μg/m³
Population Attributable Fraction (PAF): 0.0476 (4.76%)
Total cases: 70748
Avoidable cases: 3368

3. SENSITIVITY ANALYSIS

============================================================
SENSITIVITY ANALYSIS: Effect of TMREL on PAF
============================================================

=== TOTAL PAF CALCULATION ===
TMREL (reference level): 2.4 μg/m³
Average PM2.5 concentration: 55.56 μg/m³
Population Attributable Fraction (PAF): 0.0599 (5.99%)
Total cases: 223680
Avoidable cases: 13394

=== MALE PAF CALCULATION ===
TMREL (reference level): 2.4 μg/m³
Average PM2.5 concentration: 55.56 μg/m³
Population Attributable Fraction (PAF): 0.0747 (7.47%)
Total cases: 152932
Avoidable cases: 11428

=== FEMALE PAF CALCULATION ===
TMREL (reference level): 2.4 μg/m³
Average PM2.5 concentration: 55.56 μg/m³
Population Attributable Fraction (PAF): 0.0498 (4.98%)
Total cases: 70748
Avoidable cases: 3524

=== TOTAL PAF CALCULATION ===
TMREL (reference level): 5.0 μg/m³
Average PM2.5 concentration: 55.56 μg/m³
Population Attributable Fraction (PAF): 0.0572 (5.72%)
Total cases: 223680
Avoidable cases: 12802

=== MALE PAF CALCULATION ===
TMREL (reference level): 5.0 μg/m³
Average PM2.5 concentration: 55.56 μg/m³
Population Attributable Fraction (PAF): 0.0714 (7.14%)
Total cases: 152932
Avoidable cases: 10927

=== FEMALE PAF CALCULATION ===
TMREL (reference level): 5.0 μg/m³
Average PM2.5 concentration: 55.56 μg/m³
Population Attributable Fraction (PAF): 0.0476 (4.76%)
Total cases: 70748
Avoidable cases: 3368

=== TOTAL PAF CALCULATION ===
TMREL (reference level): 7.5 μg/m³
Average PM2.5 concentration: 55.56 μg/m³
Population Attributable Fraction (PAF): 0.0547 (5.47%)
Total cases: 223680
Avoidable cases: 12232

=== MALE PAF CALCULATION ===
TMREL (reference level): 7.5 μg/m³
Average PM2.5 concentration: 55.56 μg/m³
Population Attributable Fraction (PAF): 0.0683 (6.83%)
Total cases: 152932
Avoidable cases: 10443

=== FEMALE PAF CALCULATION ===
TMREL (reference level): 7.5 μg/m³
Average PM2.5 concentration: 55.56 μg/m³
Population Attributable Fraction (PAF): 0.0455 (4.55%)
Total cases: 70748
Avoidable cases: 3218

=== TOTAL PAF CALCULATION ===
TMREL (reference level): 10.0 μg/m³
Average PM2.5 concentration: 55.56 μg/m³
Population Attributable Fraction (PAF): 0.0521 (5.21%)
Total cases: 223680
Avoidable cases: 11661

=== MALE PAF CALCULATION ===
TMREL (reference level): 10.0 μg/m³
Average PM2.5 concentration: 55.56 μg/m³
Population Attributable Fraction (PAF): 0.0651 (6.51%)
Total cases: 152932
Avoidable cases: 9958

=== FEMALE PAF CALCULATION ===
TMREL (reference level): 10.0 μg/m³
Average PM2.5 concentration: 55.56 μg/m³
Population Attributable Fraction (PAF): 0.0434 (4.34%)
Total cases: 70748
Avoidable cases: 3067

Sensitivity analysis results:
   TMREL  PAF_Total  Avoidable_Total  PAF_Male  Avoidable_Male  PAF_Female  Avoidable_Female
0    2.4     0.0599       13393.7248    0.0747      11428.1061      0.0498         3524.3651
1    5.0     0.0572       12802.4422    0.0714      10926.7797      0.0476         3368.2476
2    7.5     0.0547       12232.3334    0.0683      10443.0603      0.0455         3217.7926
3   10.0     0.0521       11660.6834    0.0651       9957.6932      0.0434         3067.0018

============================================================
FINAL RESULTS SUMMARY
============================================================

EXPOSURE-RESPONSE COEFFICIENTS (β):
Total population β: 0.001080
Male population β: 0.001360
Female population β: 0.000892

RELATIVE RISK PER 10 μg/m³ INCREASE:
Total RR: 1.0109
Male RR: 1.0137
Female RR: 1.0090

POPULATION ATTRIBUTABLE FRACTION (PAF) - TMREL = 5.0 μg/m³:
Total PAF: 0.0572 (5.7%)
Male PAF: 0.0714 (7.1%)
Female PAF: 0.0476 (4.8%)

INTERPRETATION:
PM2.5 exposure accounts for 5.7% of lung cancer cases.
If PM2.5 were reduced to 5.0 μg/m³, 12802 cases could be prevented.



### **核心要素解释（供您理解和回应审稿人使用）**

1. **为什么计算PAF？**

   - **弥补RR的不足**：相对风险只告诉你“风险增加多少倍”，但无法回答“这对整个社会影响有多大”。一个风险很高但暴露人数极少的因素，其人群危害可能很小。PAF同时考虑了**风险强度（RR）** 和**暴露人群规模（P_i）**，能量化该风险因素的**总体影响**。

2. **TMREL为什么设为5.0？**

   - 这是一个基于**现有科学证据的政策性假设**。WHO指南指出，PM2.5在此浓度以下，对健康的负面影响被认为非常小或可忽略。设定TMREL是计算PAF的必要前提，体现了研究的**政策相关性**（我们的目标是将PM2.5控制到安全水平）。在敏感性分析中，您可以测试不同TMREL（如2.4, 7.5）对结果的影响，以证明结论的稳健性。

3. **PAF结果如何解读？**

   - 您的结果（总PAF=5.7%，男性=7.1%，女性=4.8%）应解读为：

     > “在本研究涵盖的中国城市人群中，若能将PM2.5年均浓度降至WHO指导值（5.0 μg/m³），理论上可预防**5.7%** 的肺癌病例，其中男性（**7.1%**）的可预防比例高于女性（**4.8%**）。”

4. **PAF与RR的关系是什么？**

   - **RR是“因”，PAF是“果”**。泊松回归提供了**因果关系强度（β -> RR）** 的证据，而PAF则利用这个RR，结合暴露分布，计算出该因果关系导致的**人群疾病负担**。二者结合，从不同维度完整地讲述了PM2.5健康影响的故事。