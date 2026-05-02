import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# 设置图表样式
plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial', 'Helvetica']

class PAFCalculator:
    def __init__(self, tmrel=5.0, rr_per_10ug=1.09):
        self.tmrel = tmrel
        self.rr_per_10ug = rr_per_10ug
        self.beta = np.log(rr_per_10ug) / 10
        self.df = None
        
    def load_data(self, file_path):
        try:
            self.df = pd.read_excel(file_path)
            print("数据列名:", self.df.columns.tolist())
            
            # 重命名列
            self.df = self.df.rename(columns={
                'PM2.5 （微克每立方米）': 'pm25',
                '世标率(男)': 'male_rate', 
                '世标率(女)': 'female_rate',
                '常住人口（男/万人）': 'male_pop_10k',
                '常住人口（女/万人）': 'female_pop_10k'
            })
            
            # 转换人口数据
            self.df['male_population'] = self.df['male_pop_10k'] * 10000
            self.df['female_population'] = self.df['female_pop_10k'] * 10000
            self.df['total_population'] = self.df['male_population'] + self.df['female_population']
            
            # 计算病例数
            self.df['male_cases'] = (self.df['male_rate'] / 100000) * self.df['male_population']
            self.df['female_cases'] = (self.df['female_rate'] / 100000) * self.df['female_population']
            self.df['total_cases'] = self.df['male_cases'] + self.df['female_cases']
            
            self.df = self.df.dropna()
            print(f"分析城市数量: {len(self.df)}")
            
            return self.df
            
        except Exception as e:
            print(f"数据加载错误: {e}")
            return None
    
    def calculate_rr(self, pm25):
        return np.exp(self.beta * (pm25 - self.tmrel))
    
    def calculate_paf(self, gender='total'):
        if gender == 'total':
            pop = self.df['total_population']
            cases = self.df['total_cases']
        elif gender == 'male':
            pop = self.df['male_population']
            cases = self.df['male_cases']
        else:
            pop = self.df['female_population']
            cases = self.df['female_cases']
        
        total_pop = pop.sum()
        weights = pop / total_pop
        rr_values = self.df['pm25'].apply(self.calculate_rr)
        
        numerator = np.sum(weights * (rr_values - 1))
        denominator = np.sum(weights * rr_values)
        paf = numerator / denominator
        avoidable_cases = cases.sum() * paf
        
        return paf, avoidable_cases
    
    def create_exposure_response_chart(self):
        plt.figure(figsize=(8, 5))
        
        pm25_range = np.linspace(0, 100, 100)
        rr_range = [self.calculate_rr(x) for x in pm25_range]
        
        plt.plot(pm25_range, rr_range, 'b-', linewidth=2)
        plt.axhline(y=1, color='red', linestyle='--', alpha=0.7, label='RR=1')
        plt.axvline(x=self.tmrel, color='green', linestyle='--', alpha=0.7, label=f'TMREL={self.tmrel}μg/m³')
        
        avg_pm25 = self.df['pm25'].mean()
        avg_rr = self.calculate_rr(avg_pm25)
        plt.plot(avg_pm25, avg_rr, 'ro', markersize=6, label=f'Current avg')
        
        plt.xlabel('PM2.5 Concentration (μg/m³)')
        plt.ylabel('Relative Risk (RR)')
        plt.title(f'Exposure-Response Curve (RR={self.rr_per_10ug}/10μg/m³)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def create_paf_chart(self, paf_total, paf_male, paf_female):
        plt.figure(figsize=(6, 4))
        
        categories = ['Total', 'Male', 'Female']
        paf_values = [paf_total*100, paf_male*100, paf_female*100]
        
        bars = plt.bar(categories, paf_values, color=['lightblue', 'lightcoral', 'lightgreen'])
        
        for bar, value in zip(bars, paf_values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                    f'{value:.1f}%', ha='center', va='bottom')
        
        plt.ylabel('PAF (%)')
        plt.title('Population Attributable Fraction by Gender')
        plt.ylim(0, max(paf_values) + 5)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.show()

def main():
    calculator = PAFCalculator(tmrel=5.0, rr_per_10ug=1.09)
    
    file_path = r"D:\SRT\output_data\最最终原始数据用.xlsx"
    df = calculator.load_data(file_path)
    
    if df is None:
        return
    
    print("\n参数设置:")
    print(f"RR (每10μg/m³增加): {calculator.rr_per_10ug}")
    print(f"β系数: {calculator.beta:.6f}")
    print(f"TMREL: {calculator.tmrel} μg/m³")
    
    # 计算PAF
    paf_total, avoid_total = calculator.calculate_paf('total')
    paf_male, avoid_male = calculator.calculate_paf('male')
    paf_female, avoid_female = calculator.calculate_paf('female')
    
    print("\n结果:")
    print(f"总体PAF: {paf_total:.3f} ({paf_total*100:.1f}%)")
    print(f"男性PAF: {paf_male:.3f} ({paf_male*100:.1f}%)")
    print(f"女性PAF: {paf_female:.3f} ({paf_female*100:.1f}%)")
    print(f"可避免病例数: {avoid_total:.0f}")
    
    # 生成图表
    calculator.create_exposure_response_chart()
    calculator.create_paf_chart(paf_total, paf_male, paf_female)
    
    return calculator, df

if __name__ == "__main__":
    calculator, df = main()