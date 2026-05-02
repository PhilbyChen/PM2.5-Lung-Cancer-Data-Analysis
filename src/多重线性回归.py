# -*- coding: utf-8 -*-
"""
PM2.5与肺癌发病率关系的多元线性回归分析
使用真实数据版本
数据文件: D:\SRT\output_data\最最终原始数据用.xlsx
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import warnings
warnings.filterwarnings('ignore')

print("✅ PM2.5与肺癌世标率关系分析开始...")

# 设置绘图风格
sns.set_style("whitegrid")
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# 第一步：读取真实数据
print("📂 正在读取数据文件...")
file_path = r"D:\SRT\output_data\最最终原始数据用.xlsx"

try:
    # 读取Excel文件
    df = pd.read_excel(file_path)
    print(f"✅ 数据读取成功！共{len(df)}个城市的数据")
    
    # 显示列名，确认数据格式
    print("\n数据文件包含的列：")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")
    
    # 显示前几行数据
    print("\n数据前5行预览：")
    print(df.head())
    
except FileNotFoundError:
    print(f"❌ 错误：找不到文件 {file_path}")
    print("请检查文件路径是否正确")
    exit()
except Exception as e:
    print(f"❌ 读取文件时出错：{e}")
    exit()

# 第二步：数据清洗和准备
print("\n" + "="*60)
print("数据清洗和准备")
print("="*60)

# 检查必要的列是否存在
required_columns = ['PM2.5 （微克每立方米）', '世标率(男)', '世标率(女)', '常住人口（男/万人）', '常住人口（女/万人）']
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    print(f"❌ 缺少必要的列：{missing_columns}")
    print("请检查Excel文件的列名是否与以下名称完全一致：")
    for col in required_columns:
        print(f"  - {col}")
    exit()

# 创建数据副本进行处理
data = df[required_columns].copy()

# 重命名列名，方便后续处理
data.columns = ['pm25', 'std_rate_male', 'std_rate_female', 'pop_male_10k', 'pop_female_10k']

# 处理缺失值
original_count = len(data)
data = data.dropna()
if len(data) < original_count:
    print(f"⚠️ 删除了 {original_count - len(data)} 个包含缺失值的行")
    print(f"✅ 剩余 {len(data)} 个有效城市数据")

# 检查数据基本信息
print("\n数据基本信息：")
print(data.describe())

# 检查异常值
print("\n数据范围检查：")
for col in data.columns:
    print(f"{col}: {data[col].min():.2f} ~ {data[col].max():.2f}")

# 第三步：创建分析变量
print("\n" + "="*60)
print("创建分析变量")
print("="*60)

# 计算总人口（转换为实际人数，而不是万人）
data['pop_male'] = data['pop_male_10k'] * 10000  # 转换为实际人数
data['pop_female'] = data['pop_female_10k'] * 10000
data['pop_total'] = data['pop_male'] + data['pop_female']

# 计算加权平均的总体世标率（按人口加权）
data['std_rate_total'] = (data['std_rate_male'] * data['pop_male'] + 
                         data['std_rate_female'] * data['pop_female']) / data['pop_total']

# 计算性别比
data['gender_ratio'] = data['pop_male'] / data['pop_female']

print("变量创建完成：")
print(f"- PM2.5浓度范围: {data['pm25'].min():.1f} ~ {data['pm25'].max():.1f} μg/m³")
print(f"- 男性世标率范围: {data['std_rate_male'].min():.1f} ~ {data['std_rate_male'].max():.1f} /10万")
print(f"- 女性世标率范围: {data['std_rate_female'].min():.1f} ~ {data['std_rate_female'].max():.1f} /10万")
print(f"- 总体世标率范围: {data['std_rate_total'].min():.1f} ~ {data['std_rate_total'].max():.1f} /10万")
print(f"- 性别比范围: {data['gender_ratio'].min():.2f} ~ {data['gender_ratio'].max():.2f}")

# 第四步：探索性数据分析
print("\n" + "="*60)
print("探索性数据分析")
print("="*60)

# 创建散点图矩阵
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# PM2.5 vs 总体世标率
axes[0,0].scatter(data['pm25'], data['std_rate_total'], alpha=0.7, s=60, color='blue')
axes[0,0].set_xlabel('PM2.5浓度 (μg/m³)')
axes[0,0].set_ylabel('肺癌总体世标率 (每十万人)')
axes[0,0].set_title('PM2.5 vs 总体肺癌世标率')
z_total = np.polyfit(data['pm25'], data['std_rate_total'], 1)
p_total = np.poly1d(z_total)
axes[0,0].plot(data['pm25'], p_total(data['pm25']), "r--", linewidth=2)

# PM2.5 vs 男性世标率
axes[0,1].scatter(data['pm25'], data['std_rate_male'], alpha=0.7, s=60, color='green')
axes[0,1].set_xlabel('PM2.5浓度 (μg/m³)')
axes[0,1].set_ylabel('肺癌男性世标率 (每十万人)')
axes[0,1].set_title('PM2.5 vs 男性肺癌世标率')
z_male = np.polyfit(data['pm25'], data['std_rate_male'], 1)
p_male = np.poly1d(z_male)
axes[0,1].plot(data['pm25'], p_male(data['pm25']), "r--", linewidth=2)

# PM2.5 vs 女性世标率
axes[1,0].scatter(data['pm25'], data['std_rate_female'], alpha=0.7, s=60, color='purple')
axes[1,0].set_xlabel('PM2.5浓度 (μg/m³)')
axes[1,0].set_ylabel('肺癌女性世标率 (每十万人)')
axes[1,0].set_title('PM2.5 vs 女性肺癌世标率')
z_female = np.polyfit(data['pm25'], data['std_rate_female'], 1)
p_female = np.poly1d(z_female)
axes[1,0].plot(data['pm25'], p_female(data['pm25']), "r--", linewidth=2)

# 性别比分布
axes[1,1].hist(data['gender_ratio'], bins=15, alpha=0.7, color='orange')
axes[1,1].set_xlabel('性别比 (男/女)')
axes[1,1].set_ylabel('城市数量')
axes[1,1].set_title('性别比分布')
axes[1,1].axvline(data['gender_ratio'].mean(), color='red', linestyle='--', 
                 label=f'均值: {data["gender_ratio"].mean():.2f}')
axes[1,1].legend()

plt.tight_layout()
plt.savefig('pm25_lung_cancer_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# 第五步：多元线性回归分析
print("\n" + "="*60)
print("多元线性回归分析")
print("="*60)

# 分析方案1：总体世标率 vs PM2.5 + 性别比
print("\n🔍 分析方案1：总体世标率分析")
y_total = data['std_rate_total']
X_total = data[['pm25', 'gender_ratio']]
X_total = sm.add_constant(X_total)

model_total = sm.OLS(y_total, X_total).fit()
print(model_total.summary())

# 分析方案2：男性世标率分析
print("\n🔍 分析方案2：男性世标率分析")
y_male = data['std_rate_male']
X_male = data[['pm25', 'gender_ratio']]
X_male = sm.add_constant(X_male)

model_male = sm.OLS(y_male, X_male).fit()
print(model_male.summary())

# 分析方案3：女性世标率分析
print("\n🔍 分析方案3：女性世标率分析")
y_female = data['std_rate_female']
X_female = data[['pm25', 'gender_ratio']]
X_female = sm.add_constant(X_female)

model_female = sm.OLS(y_female, X_female).fit()
print(model_female.summary())

# 第六步：结果解读和总结
print("\n" + "="*60)
print("关键结果总结")
print("="*60)

def interpret_model(model, model_name):
    """解读回归模型结果"""
    pm25_coef = model.params['pm25']
    pm25_pval = model.pvalues['pm25']
    r_squared = model.rsquared
    
    print(f"\n📊 {model_name}结果:")
    print(f"  • 模型解释度 (R²): {r_squared:.3f} ({r_squared*100:.1f}%)")
    print(f"  • PM2.5系数: {pm25_coef:.4f}")
    print(f"  • PM2.5 p值: {pm25_pval:.4f}")
    
    if pm25_pval < 0.001:
        sig_level = "极其显著 (***)"
    elif pm25_pval < 0.01:
        sig_level = "非常显著 (**)"
    elif pm25_pval < 0.05:
        sig_level = "显著 (*)"
    else:
        sig_level = "不显著"
    
    print(f"  • 统计显著性: {sig_level}")
    print(f"  • 实际意义: PM2.5每增加10μg/m³，世标率变化{pm25_coef*10:.2f}例/10万")

# 解读三个模型
interpret_model(model_total, "总体世标率")
interpret_model(model_male, "男性世标率")
interpret_model(model_female, "女性世标率")

# 第七步：共线性诊断
print("\n" + "="*60)
print("共线性诊断 (VIF)")
print("="*60)

vif_data = pd.DataFrame()
vif_data["Variable"] = X_total.columns
vif_data["VIF"] = [variance_inflation_factor(X_total.values, i) for i in range(X_total.shape[1])]
print(vif_data)

print("\n" + "="*60)
print("分析完成！")
print("="*60)
print("📋 分析总结：")
print("1. 使用世标率消除了年龄结构影响，结果更科学")
print("2. 分别分析了总体、男性和女性的情况")
print("3. 控制了性别比的影响")
print("4. 结果已保存到 'pm25_lung_cancer_analysis.png'")
print("5. 请重点关注PM2.5的系数和p值来判断关联显著性")