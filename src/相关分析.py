import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
import matplotlib as mpl

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

class PM25Analysis:
    def __init__(self):
        self.df = None
        self.results = {}
    
    def load_data(self):
        """加载并预处理数据"""
        file_path = r"D:\SRT\output_data\最最终原始数据用.xlsx"
        self.df = pd.read_excel(file_path)
        print(f"数据加载成功，共{len(self.df)}个城市")
        
        # 计算实际人口数（从万人转换为实际人数）
        self.df['male_population'] = self.df['常住人口（男/万人）'] * 10000
        self.df['female_population'] = self.df['常住人口（女/万人）'] * 10000
        self.df['total_population'] = self.df['male_population'] + self.df['female_population']
        
        # 计算实际病例数（基于世标率和人口）
        self.df['male_cases'] = (self.df['世标率(男)'] / 100000) * self.df['male_population']
        self.df['female_cases'] = (self.df['世标率(女)'] / 100000) * self.df['female_population']
        self.df['total_cases'] = self.df['male_cases'] + self.df['female_cases']
        
        return self.df
    
    def spearman_with_ci(self, x, y, n_bootstrap=1000):
        """计算斯皮尔曼相关系数及95%置信区间（自助法）"""
        # 移除缺失值
        mask = ~(np.isnan(x) | np.isnan(y))
        x_clean = x[mask]
        y_clean = y[mask]
        
        if len(x_clean) < 10:
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
        
        # 计算95%置信区间
        if len(bootstrap_corrs) > 0:
            ci_lower = np.percentile(bootstrap_corrs, 2.5)
            ci_upper = np.percentile(bootstrap_corrs, 97.5)
        else:
            ci_lower = ci_upper = np.nan
        
        return corr_original, p_value, (ci_lower, ci_upper)
    
    def spearman_analysis(self):
        """斯皮尔曼相关分析（含置信区间）"""
        print("\n=== 斯皮尔曼相关分析（含95%置信区间）===")
        
        # PM2.5与男性发病率相关性
        corr_male, p_male, ci_male = self.spearman_with_ci(
            self.df['PM2.5 （微克每立方米）'], self.df['世标率(男)'])
        
        # PM2.5与女性发病率相关性
        corr_female, p_female, ci_female = self.spearman_with_ci(
            self.df['PM2.5 （微克每立方米）'], self.df['世标率(女)'])
        
        print(f"PM2.5 vs 男性发病率:")
        print(f"  ρ = {corr_male:.3f}, 95%CI [{ci_male[0]:.3f}, {ci_male[1]:.3f}], P = {p_male:.4f}")
        
        print(f"PM2.5 vs 女性发病率:")
        print(f"  ρ = {corr_female:.3f}, 95%CI [{ci_female[0]:.3f}, {ci_female[1]:.3f}], P = {p_female:.4f}")
        
        self.results['spearman'] = {
            'male': {'correlation': corr_male, 'p_value': p_male, 'ci_lower': ci_male[0], 'ci_upper': ci_male[1]},
            'female': {'correlation': corr_female, 'p_value': p_female, 'ci_lower': ci_female[0], 'ci_upper': ci_female[1]}
        }
        
        return self.results['spearman']
    
    def poisson_regression(self, gender='total'):
        """泊松回归分析（含置信区间）"""
        # 选择数据
        if gender == 'male':
            cases = self.df['male_cases']
            population = self.df['male_population']
            gender_name = '男性'
        elif gender == 'female':
            cases = self.df['female_cases']
            population = self.df['female_population']
            gender_name = '女性'
        else:  # total
            cases = self.df['total_cases']
            population = self.df['total_population']
            gender_name = '总人群'
        
        # 准备变量
        X = sm.add_constant(self.df['PM2.5 （微克每立方米）'])
        
        # 拟合泊松回归模型
        model = sm.GLM(cases, X, family=sm.families.Poisson(),
                      offset=np.log(population)).fit()
        
        # 提取系数和置信区间
        beta = model.params[1]  # PM2.5的系数
        p_value = model.pvalues[1]
        
        # 计算系数的95%置信区间
        beta_ci = model.conf_int().iloc[1]  # PM2.5系数的置信区间
        beta_ci_lower, beta_ci_upper = beta_ci[0], beta_ci[1]
        
        # 计算相对风险及其置信区间
        rr_1 = np.exp(beta)                    # 每1μg/m³增加的相对风险
        rr_1_ci_lower = np.exp(beta_ci_lower)  # RR的95%置信区间下限
        rr_1_ci_upper = np.exp(beta_ci_upper)  # RR的95%置信区间上限
        
        rr_10 = np.exp(10 * beta)              # 每10μg/m³增加的相对风险
        rr_10_ci_lower = np.exp(10 * beta_ci_lower)  # RR10的95%置信区间下限
        rr_10_ci_upper = np.exp(10 * beta_ci_upper)  # RR10的95%置信区间上限
        
        # 存储结果
        if 'poisson' not in self.results:
            self.results['poisson'] = {}
        
        self.results['poisson'][gender] = {
            'beta': beta,
            'beta_ci_lower': beta_ci_lower,
            'beta_ci_upper': beta_ci_upper,
            'p_value': p_value,
            'RR_1': rr_1,
            'RR_1_ci_lower': rr_1_ci_lower,
            'RR_1_ci_upper': rr_1_ci_upper,
            'RR_10': rr_10,
            'RR_10_ci_lower': rr_10_ci_lower,
            'RR_10_ci_upper': rr_10_ci_upper,
            'model': model
        }
        
        print(f"\n{gender_name}泊松回归结果:")
        print(f"  PM2.5系数 β = {beta:.6f} (95%CI [{beta_ci_lower:.6f}, {beta_ci_upper:.6f}])")
        print(f"  每1μg/m³ RR = {rr_1:.4f} (95%CI [{rr_1_ci_lower:.4f}, {rr_1_ci_upper:.4f}])")
        print(f"  每10μg/m³ RR = {rr_10:.4f} (95%CI [{rr_10_ci_lower:.4f}, {rr_10_ci_upper:.4f}])")
        print(f"  P值 = {p_value:.4f}")
        
        return model
    
    def plot_correlation_scatter(self):
        """绘制相关性散点图（含置信区间信息）"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 男性数据散点图
        male_result = self.results['spearman']['male']
        corr_male = male_result['correlation']
        ci_male_lower = male_result['ci_lower']
        ci_male_upper = male_result['ci_upper']
        p_male = male_result['p_value']
        
        ax1.scatter(self.df['PM2.5 （微克每立方米）'], self.df['世标率(男)'], 
                   alpha=0.6, color='blue', s=50)
        ax1.set_xlabel('PM2.5浓度 (μg/m³)')
        ax1.set_ylabel('男性肺癌发病率 (/10万)')
        ax1.set_title(f'PM2.5 vs 男性发病率\nρ = {corr_male:.3f} (95%CI [{ci_male_lower:.3f}, {ci_male_upper:.3f}])')
        ax1.grid(True, alpha=0.3)
        
        # 添加趋势线
        z_male = np.polyfit(self.df['PM2.5 （微克每立方米）'], self.df['世标率(男)'], 1)
        p_male_line = np.poly1d(z_male)
        x_range = np.linspace(self.df['PM2.5 （微克每立方米）'].min(), 
                             self.df['PM2.5 （微克每立方米）'].max(), 100)
        ax1.plot(x_range, p_male_line(x_range), "r--", alpha=0.8, linewidth=2)
        
        # 女性数据散点图
        female_result = self.results['spearman']['female']
        corr_female = female_result['correlation']
        ci_female_lower = female_result['ci_lower']
        ci_female_upper = female_result['ci_upper']
        p_female = female_result['p_value']
        
        ax2.scatter(self.df['PM2.5 （微克每立方米）'], self.df['世标率(女)'], 
                   alpha=0.6, color='red', s=50)
        ax2.set_xlabel('PM2.5浓度 (μg/m³)')
        ax2.set_ylabel('女性肺癌发病率 (/10万)')
        ax2.set_title(f'PM2.5 vs 女性发病率\nρ = {corr_female:.3f} (95%CI [{ci_female_lower:.3f}, {ci_female_upper:.3f}])')
        ax2.grid(True, alpha=0.3)
        
        # 添加趋势线
        z_female = np.polyfit(self.df['PM2.5 （微克每立方米）'], self.df['世标率(女)'], 1)
        p_female_line = np.poly1d(z_female)
        ax2.plot(x_range, p_female_line(x_range), "r--", alpha=0.8, linewidth=2)
        
        plt.tight_layout()
        plt.show()
    
    def plot_rr_comparison(self):
        """绘制相对风险比较图（含置信区间）"""
        # 获取RR结果和置信区间
        categories = ['总人群', '男性', '女性']
        rr_values = []
        rr_ci_lower = []
        rr_ci_upper = []
        
        for gender in ['total', 'male', 'female']:
            result = self.results['poisson'][gender]
            rr_values.append(result['RR_10'])
            rr_ci_lower.append(result['RR_10_ci_lower'])
            rr_ci_upper.append(result['RR_10_ci_upper'])
        
        colors = ['purple', 'blue', 'red']
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 绘制柱状图和误差线
        x_pos = np.arange(len(categories))
        bars = ax.bar(x_pos, rr_values, color=colors, alpha=0.7, width=0.6, 
                     yerr=[np.array(rr_values) - np.array(rr_ci_lower), 
                           np.array(rr_ci_upper) - np.array(rr_values)],
                     capsize=8, error_kw={'elinewidth': 2, 'capthick': 2})
        
        # 添加参考线
        ax.axhline(y=1.0, color='black', linestyle='--', linewidth=2, label='RR = 1.0')
        
        # 在柱子上添加数值和置信区间
        for i, (bar, rr, ci_low, ci_up) in enumerate(zip(bars, rr_values, rr_ci_lower, rr_ci_upper)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 0.02, 
                   f'RR={rr:.3f}\n({ci_low:.3f}-{ci_up:.3f})', 
                   ha='center', va='bottom', fontsize=10)
        
        ax.set_ylabel('相对风险 (每10μg/m³ PM2.5增加)', fontsize=12)
        ax.set_title('PM2.5与肺癌相对风险比较（含95%置信区间）', fontsize=14, fontweight='bold')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(categories)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.show()
    
    def run_analysis(self):
        """运行完整分析"""
        # 加载数据
        self.load_data()
        
        # 斯皮尔曼相关分析（含置信区间）
        self.spearman_analysis()
        
        # 泊松回归分析（含置信区间）
        print("\n=== 泊松回归分析（含95%置信区间）===")
        for gender in ['total', 'male', 'female']:
            self.poisson_regression(gender)
        
        # 绘制图表
        print("\n=== 生成分析图表 ===")
        self.plot_correlation_scatter()
        self.plot_rr_comparison()
        
        return self.results

# 运行分析
if __name__ == "__main__":
    analyzer = PM25Analysis()
    results = analyzer.run_analysis()
    
    # 输出总结
    print("\n" + "="*60)
    print("分析总结")
    print("="*60)
    
    print("\n主要发现:")
    for gender, name in [('male', '男性'), ('female', '女性'), ('total', '总人群')]:
        spearman_result = analyzer.results['spearman'].get(gender, {})
        poisson_result = analyzer.results['poisson'].get(gender, {})
        
        if spearman_result and poisson_result:
            print(f"\n{name}:")
            print(f"  斯皮尔曼相关: ρ = {spearman_result['correlation']:.3f} (95%CI [{spearman_result['ci_lower']:.3f}, {spearman_result['ci_upper']:.3f}])")
            print(f"  相对风险: RR = {poisson_result['RR_10']:.3f} (95%CI [{poisson_result['RR_10_ci_lower']:.3f}, {poisson_result['RR_10_ci_upper']:.3f}])")