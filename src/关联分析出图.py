import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 设置样式
plt.style.use('default')

# 创建数据
data = {
    'Group': ['Total', 'Male', 'Female'],
    'Spearman_rho': [None, 0.220, 0.178],
    'Spearman_lower': [None, 0.031, -0.002],
    'Spearman_upper': [None, 0.400, 0.368],
    'RR_per_10ug': [1.0109, 1.0137, 1.0090],
    'RR_lower': [1.0086, 1.0109, 1.0049],
    'RR_upper': [1.0132, 1.0165, 1.0131],
    'P_value': [0.0000, 0.0000, 0.0000]
}

df = pd.DataFrame(data)

# 创建画布
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Association between PM2.5 Exposure and Health Outcomes', fontsize=16, fontweight='bold')

# 图表1: 斯皮尔曼相关系数（仅男性和女性）
ax1.bar([1, 2], df.loc[1:, 'Spearman_rho'], color=['steelblue', 'lightcoral'], 
        alpha=0.7, width=0.6)
ax1.errorbar([1, 2], df.loc[1:, 'Spearman_rho'], 
             yerr=[df.loc[1:, 'Spearman_rho'] - df.loc[1:, 'Spearman_lower'], 
                   df.loc[1:, 'Spearman_upper'] - df.loc[1:, 'Spearman_rho']],
             fmt='o', color='black', capsize=5)
ax1.set_xticks([1, 2])
ax1.set_xticklabels(['Male', 'Female'])
ax1.set_ylabel('Spearman Correlation Coefficient (ρ)')
ax1.set_title('Spearman Correlation by Gender')
ax1.grid(True, alpha=0.3)
ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.7)

# 在柱子上添加数值
for i, (idx, row) in enumerate(df.loc[1:].iterrows()):
    ax1.text(i+1, row['Spearman_rho'] + 0.01, f'ρ = {row["Spearman_rho"]:.3f}', 
             ha='center', va='bottom', fontweight='bold')

# 图表2: 每10μg/m³ PM2.5的相对风险
groups = df['Group']
x_pos = np.arange(len(groups))
bars = ax2.bar(x_pos, df['RR_per_10ug'] - 1, color=['darkgreen', 'steelblue', 'lightcoral'], 
               alpha=0.7, width=0.6)
ax2.errorbar(x_pos, df['RR_per_10ug'] - 1, 
             yerr=[df['RR_per_10ug'] - df['RR_lower'], df['RR_upper'] - df['RR_per_10ug']],
             fmt='o', color='black', capsize=5)
ax2.set_xticks(x_pos)
ax2.set_xticklabels(groups)
ax2.set_ylabel('Relative Risk (RR - 1) per 10μg/m³ PM2.5')
ax2.set_title('Relative Risk Increase per 10μg/m³ PM2.5')
ax2.grid(True, alpha=0.3)

# 在柱子上添加RR值
for i, (bar, rr) in enumerate(zip(bars, df['RR_per_10ug'])):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.0005, f'RR={rr:.4f}', 
             ha='center', va='bottom', fontweight='bold')

# 图表3: 泊松回归系数的森林图
coefficients = [0.001080, 0.001360, 0.000892]
ci_lower = [0.000852, 0.001085, 0.000486]
ci_upper = [0.001308, 0.001636, 0.001298]

y_pos = [2, 1, 0]
ax3.errorbar(coefficients, y_pos, xerr=[np.array(coefficients) - np.array(ci_lower), 
                                       np.array(ci_upper) - np.array(coefficients)], 
             fmt='o', color='black', capsize=5)
ax3.scatter(coefficients, y_pos, s=80, color=['darkgreen', 'steelblue', 'lightcoral'], 
           alpha=0.7)
ax3.set_yticks(y_pos)
ax3.set_yticklabels(['Female', 'Male', 'Total'])
ax3.set_xlabel('Poisson Regression Coefficient (β)')
ax3.set_title('Poisson Regression Coefficients with 95% CI')
ax3.axvline(x=0, color='red', linestyle='--', alpha=0.5)
ax3.grid(True, alpha=0.3)

# 添加系数值
for i, (coef, y) in enumerate(zip(coefficients, y_pos)):
    ax3.text(coef + 0.0001, y, f'β={coef:.6f}', va='center', fontweight='bold')

# 图表4: 性别比较 - 相对风险
gender_groups = ['Male', 'Female']
male_rr = [df.loc[1, 'RR_per_10ug'], df.loc[1, 'Spearman_rho']]
female_rr = [df.loc[2, 'RR_per_10ug'], df.loc[2, 'Spearman_rho']]

x = np.arange(len(gender_groups))
width = 0.35

bars1 = ax4.bar(x - width/2, [male_rr[0] - 1, male_rr[1]], width, label='Male', 
                color='steelblue', alpha=0.7)
bars2 = ax4.bar(x + width/2, [female_rr[0] - 1, female_rr[1]], width, label='Female', 
                color='lightcoral', alpha=0.7)

ax4.set_xticks(x)
ax4.set_xticklabels(['RR-1 (per 10μg/m³)', 'Spearman ρ'])
ax4.set_ylabel('Effect Size')
ax4.set_title('Gender Comparison: RR and Correlation')
ax4.legend()
ax4.grid(True, alpha=0.3)

# 添加数值标签
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        if bar.get_x() < 0.5:  # RR bars
            value = height + 1
            ax4.text(bar.get_x() + bar.get_width()/2., height + 0.001, f'{value:.3f}', 
                    ha='center', va='bottom', fontsize=9)
        else:  # Correlation bars
            ax4.text(bar.get_x() + bar.get_width()/2., height + 0.01, f'{height:.3f}', 
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()

# 创建汇总表格
print("\nSummary Table of Results:")
print("="*80)
print(f"{'Group':<10} {'Spearman ρ':<15} {'95% CI':<25} {'RR per 10μg/m³':<15} {'95% CI':<25}")
print("-"*80)
for i, row in df.iterrows():
    if pd.isna(row['Spearman_rho']):
        spearman_ci = "N/A"
        spearman_str = "N/A"
    else:
        spearman_ci = f"[{row['Spearman_lower']:.3f}, {row['Spearman_upper']:.3f}]"
        spearman_str = f"{row['Spearman_rho']:.3f}"
    
    rr_ci = f"[{row['RR_lower']:.4f}, {row['RR_upper']:.4f}]"
    print(f"{row['Group']:<10} {spearman_str:<15} {spearman_ci:<25} {row['RR_per_10ug']:<15.4f} {rr_ci:<25}")

print("="*80)