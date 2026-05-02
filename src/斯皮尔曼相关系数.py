import pandas as pd
import numpy as np
from scipy.stats import spearmanr
import matplotlib.pyplot as plt

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def spearmanr_with_ci(x, y, alpha=0.05, n_bootstrap=1000):
    """计算斯皮尔曼相关系数及其置信区间（自助法）"""
    # 移除缺失值
    mask = ~(np.isnan(x) | np.isnan(y))
    x_clean = x[mask]
    y_clean = y[mask]
    
    if len(x_clean) < 10:  # 样本量太小
        return np.nan, np.nan, (np.nan, np.nan)
    
    # 原始相关系数
    corr_original, p_value = spearmanr(x_clean, y_clean)
    
    # 自助法计算置信区间
    n = len(x_clean)
    bootstrap_corrs = []
    
    for _ in range(n_bootstrap):
        # 重抽样
        indices = np.random.choice(n, n, replace=True)
        x_bootstrap = x_clean.iloc[indices] if hasattr(x_clean, 'iloc') else x_clean[indices]
        y_bootstrap = y_clean.iloc[indices] if hasattr(y_clean, 'iloc') else y_clean[indices]
        
        corr_bootstrap, _ = spearmanr(x_bootstrap, y_bootstrap)
        if not np.isnan(corr_bootstrap):
            bootstrap_corrs.append(corr_bootstrap)
    
    # 计算置信区间
    if len(bootstrap_corrs) > 0:
        ci_lower = np.percentile(bootstrap_corrs, 100 * alpha/2)
        ci_upper = np.percentile(bootstrap_corrs, 100 * (1 - alpha/2))
    else:
        ci_lower = ci_upper = np.nan
    
    return corr_original, p_value, (ci_lower, ci_upper)

def calculate_spearman_for_pm25():
    """为PM2.5数据计算斯皮尔曼相关系数"""
    
    # 加载数据
    file_path = r"D:\SRT\output_data\最最终原始数据用.xlsx"
    df = pd.read_excel(file_path)
    
    print("=" * 70)
    print("PM2.5与肺癌发病率的斯皮尔曼相关分析")
    print("=" * 70)
    
    # 显示数据基本信息
    print(f"\n数据基本信息:")
    print(f"样本量: {len(df)}")
    print(f"PM2.5范围: {df['PM2.5 （微克每立方米）'].min():.1f} - {df['PM2.5 （微克每立方米）'].max():.1f} μg/m³")
    print(f"男性发病率范围: {df['世标率(男)'].min():.1f} - {df['世标率(男)'].max():.1f} /10万")
    print(f"女性发病率范围: {df['世标率(女)'].min():.1f} - {df['世标率(女)'].max():.1f} /10万")
    
    # 计算斯皮尔曼相关系数
    print(f"\n{'='*70}")
    print("斯皮尔曼相关系数结果（含95%置信区间）")
    print(f"{'='*70}")
    
    # PM2.5 vs 男性发病率
    corr_male, p_male, ci_male = spearmanr_with_ci(
        df['PM2.5 （微克每立方米）'], df['世标率(男)'])
    
    # PM2.5 vs 女性发病率
    corr_female, p_female, ci_female = spearmanr_with_ci(
        df['PM2.5 （微克每立方米）'], df['世标率(女)'])
    
    # 男性 vs 女性发病率
    corr_gender, p_gender, ci_gender = spearmanr_with_ci(
        df['世标率(男)'], df['世标率(女)'])
    
    # 输出结果
    print(f"\n1. PM2.5 vs 男性肺癌发病率:")
    print(f"   相关系数 ρ = {corr_male:.3f}")
    print(f"   95%置信区间: [{ci_male[0]:.3f}, {ci_male[1]:.3f}]")
    print(f"   P值 = {p_male:.4f}")
    print(f"   显著性: {'✅ 显著' if p_male < 0.05 else '⚠️ 不显著'}")
    
    print(f"\n2. PM2.5 vs 女性肺癌发病率:")
    print(f"   相关系数 ρ = {corr_female:.3f}")
    print(f"   95%置信区间: [{ci_female[0]:.3f}, {ci_female[1]:.3f}]")
    print(f"   P值 = {p_female:.4f}")
    print(f"   显著性: {'✅ 显著' if p_female < 0.05 else '⚠️ 不显著'}")
    
    print(f"\n3. 男性 vs 女性肺癌发病率:")
    print(f"   相关系数 ρ = {corr_gender:.3f}")
    print(f"   95%置信区间: [{ci_gender[0]:.3f}, {ci_gender[1]:.3f}]")
    print(f"   P值 = {p_gender:.4f}")
    print(f"   显著性: {'✅ 显著' if p_gender < 0.05 else '⚠️ 不显著'}")
    
    # 相关性强度解读
    print(f"\n{'='*70}")
    print("相关性强度解读")
    print(f"{'='*70}")
    
    def interpret_correlation_strength(corr, group):
        if abs(corr) < 0.1:
            return "可忽略的相关"
        elif abs(corr) < 0.3:
            return "弱相关"
        elif abs(corr) < 0.5:
            return "中等相关"
        elif abs(corr) < 0.7:
            return "强相关"
        else:
            return "极强相关"
    
    print(f"\nPM2.5与男性发病率: {interpret_correlation_strength(corr_male, '男性')} (ρ = {corr_male:.3f})")
    print(f"PM2.5与女性发病率: {interpret_correlation_strength(corr_female, '女性')} (ρ = {corr_female:.3f})")
    print(f"男性与女性发病率: {interpret_correlation_strength(corr_gender, '性别间')} (ρ = {corr_gender:.3f})")
    
    # 绘制相关性散点图
    plot_correlation_scatter(df, corr_male, corr_female, p_male, p_female)
    
    return {
        'male': {'correlation': corr_male, 'p_value': p_male, 'ci_lower': ci_male[0], 'ci_upper': ci_male[1]},
        'female': {'correlation': corr_female, 'p_value': p_female, 'ci_lower': ci_female[0], 'ci_upper': ci_female[1]},
        'gender_corr': {'correlation': corr_gender, 'p_value': p_gender, 'ci_lower': ci_gender[0], 'ci_upper': ci_gender[1]}
    }

def plot_correlation_scatter(df, corr_male, corr_female, p_male, p_female):
    """绘制相关性散点图"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # PM2.5 vs 男性发病率
    ax1.scatter(df['PM2.5 （微克每立方米）'], df['世标率(男)'], alpha=0.6, color='blue')
    ax1.set_xlabel('PM2.5浓度 (μg/m³)')
    ax1.set_ylabel('男性肺癌发病率 (/10万)')
    ax1.set_title(f'PM2.5 vs 男性发病率\nρ = {corr_male:.3f}, P = {p_male:.4f}')
    ax1.grid(True, alpha=0.3)
    
    # 添加趋势线
    z_male = np.polyfit(df['PM2.5 （微克每立方米）'], df['世标率(男)'], 1)
    p_male = np.poly1d(z_male)
    ax1.plot(df['PM2.5 （微克每立方米）'], p_male(df['PM2.5 （微克每立方米）']), "r--", alpha=0.8)
    
    # PM2.5 vs 女性发病率
    ax2.scatter(df['PM2.5 （微克每立方米）'], df['世标率(女)'], alpha=0.6, color='red')
    ax2.set_xlabel('PM2.5浓度 (μg/m³)')
    ax2.set_ylabel('女性肺癌发病率 (/10万)')
    ax2.set_title(f'PM2.5 vs 女性发病率\nρ = {corr_female:.3f}, P = {p_female:.4f}')
    ax2.grid(True, alpha=0.3)
    
    # 添加趋势线
    z_female = np.polyfit(df['PM2.5 （微克每立方米）'], df['世标率(女)'], 1)
    p_female = np.poly1d(z_female)
    ax2.plot(df['PM2.5 （微克每立方米）'], p_female(df['PM2.5 （微克每立方米）']), "r--", alpha=0.8)
    
    plt.tight_layout()
    plt.show()

# 运行分析
if __name__ == "__main__":
    results = calculate_spearman_for_pm25()
    
    # 最终总结
    print(f"\n{'='*70}")
    print("分析总结")
    print(f"{'='*70}")
    
    print(f"\n主要发现:")
    if results['male']['p_value'] < 0.05:
        print(f"✅ PM2.5与男性肺癌发病率存在显著正相关 (ρ = {results['male']['correlation']:.3f})")
    else:
        print(f"⚠️ PM2.5与男性肺癌发病率相关性不显著 (ρ = {results['male']['correlation']:.3f})")
    
    if results['female']['p_value'] < 0.05:
        print(f"✅ PM2.5与女性肺癌发病率存在显著正相关 (ρ = {results['female']['correlation']:.3f})")
    else:
        print(f"⚠️ PM2.5与女性肺癌发病率相关性不显著 (ρ = {results['female']['correlation']:.3f})")
    
    if results['gender_corr']['p_value'] < 0.05:
        print(f"✅ 男性与女性肺癌发病率存在显著相关 (ρ = {results['gender_corr']['correlation']:.3f})")