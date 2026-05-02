import pandas as pd
import numpy as np
import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore')

class PAFCalculator:
    def __init__(self, tmrel=5.0):
        """Initialize PAF Calculator"""
        self.tmrel = tmrel
        self.df = None
        self.beta_male = None
        self.beta_female = None
        self.beta_total = None
        
    def load_and_preprocess_data(self, file_path):
        """Load and preprocess data"""
        try:
            # Read Excel file
            self.df = pd.read_excel(file_path)
            print("Original column names:", self.df.columns.tolist())
            
            # Data cleaning and column renaming
            self.df = self.df.rename(columns={
                'PM2.5 （微克每立方米）': 'pm25',
                '世标率(男)': 'male_rate', 
                '世标率(女)': 'female_rate',
                '常住人口（男/万人）': 'male_pop_10k',
                '常住人口（女/万人）': 'female_pop_10k'
            })
            
            # Convert population from 10k to actual numbers
            self.df['male_population'] = self.df['male_pop_10k'] * 10000
            self.df['female_population'] = self.df['female_pop_10k'] * 10000
            self.df['total_population'] = self.df['male_population'] + self.df['female_population']
            
            # Calculate case numbers
            self.df['male_cases'] = (self.df['male_rate'] / 100000) * self.df['male_population']
            self.df['female_cases'] = (self.df['female_rate'] / 100000) * self.df['female_population']
            self.df['total_cases'] = self.df['male_cases'] + self.df['female_cases']
            
            # Remove missing values
            self.df = self.df.dropna()
            print(f"Cities available for analysis: {len(self.df)}")
            
            return self.df
            
        except Exception as e:
            print(f"Data loading error: {e}")
            return None
    
    def fit_poisson_model(self, gender='total'):
        """Fit exposure-response relationship using Poisson regression"""
        if self.df is None:
            raise ValueError("Please load data first")
        
        # Prepare data
        if gender == 'total':
            cases = self.df['total_cases']
            population = self.df['total_population']
        elif gender == 'male':
            cases = self.df['male_cases']
            population = self.df['male_population']
        elif gender == 'female':
            cases = self.df['female_cases']
            population = self.df['female_population']
        else:
            raise ValueError("gender should be 'total', 'male', or 'female'")
        
        pm25 = self.df['pm25']
        
        # Add intercept
        X = sm.add_constant(pm25)
        
        try:
            # Use Poisson regression with population as offset ！！！泊松回归
            model = sm.GLM(cases, X, family=sm.families.Poisson(), 
                          offset=np.log(population))
            result = model.fit()
            
            # Extract beta coefficient
            beta = result.params[1]
            p_value = result.pvalues[1]
            
            # Save beta values
            if gender == 'total':
                self.beta_total = beta
            elif gender == 'male':
                self.beta_male = beta
            elif gender == 'female':
                self.beta_female = beta
            
            print(f"\n=== {gender.upper()} EXPOSURE-RESPONSE RELATIONSHIP ===")
            print(f"PM2.5 coefficient (β): {beta:.6f}")
            print(f"Relative Risk (RR) = exp(β) = {np.exp(beta):.6f}")
            print(f"RR per 1 μg/m³ increase: {np.exp(beta):.4f}")
            print(f"RR per 10 μg/m³ increase: {np.exp(10 * beta):.4f}")
            print(f"P-value: {p_value:.6f}")
            
            if p_value < 0.05:
                print("✅ Statistically significant (p < 0.05)")
            else:
                print("⚠️ Not statistically significant")
            
            return beta, result
            
        except Exception as e:
            print(f"{gender} model fitting error: {e}")
            return None, None
    
    def calculate_rr_for_city(self, pm25_concentration, gender='total'):
        """Calculate relative risk for a specific PM2.5 concentration"""
        if gender == 'total' and self.beta_total is not None:
            beta = self.beta_total
        elif gender == 'male' and self.beta_male is not None:
            beta = self.beta_male
        elif gender == 'female' and self.beta_female is not None:
            beta = self.beta_female
        else:
            raise ValueError(f"Please fit {gender} model first")
        
        # RR = exp[β × (X - X_0)]
        rr = np.exp(beta * (pm25_concentration - self.tmrel))
        return rr
    
    def calculate_paf(self, gender='total'):
        """Calculate Population Attributable Fraction"""
        if self.df is None:
            raise ValueError("Please load data first")
        
        # Ensure model is fitted
        if gender == 'total' and self.beta_total is None:
            self.fit_poisson_model('total')
        elif gender == 'male' and self.beta_male is None:
            self.fit_poisson_model('male')
        elif gender == 'female' and self.beta_female is None:
            self.fit_poisson_model('female')
        
        # Calculate population weights
        if gender == 'total':
            total_population = self.df['total_population'].sum()
            population_weights = self.df['total_population'] / total_population
        elif gender == 'male':
            total_population = self.df['male_population'].sum()
            population_weights = self.df['male_population'] / total_population
        elif gender == 'female':
            total_population = self.df['female_population'].sum()
            population_weights = self.df['female_population'] / total_population
        
        # Calculate RR for each city
        rr_values = []
        for pm25 in self.df['pm25']:
            rr = self.calculate_rr_for_city(pm25, gender)
            rr_values.append(rr)
        
        rr_values = np.array(rr_values)
        
        # Calculate PAF using the standard formula
        numerator = np.sum(population_weights * (rr_values - 1))
        denominator = np.sum(population_weights * rr_values)
        paf = numerator / denominator
        
        # Calculate avoidable cases
        if gender == 'total':
            total_cases = self.df['total_cases'].sum()
        elif gender == 'male':
            total_cases = self.df['male_cases'].sum()
        elif gender == 'female':
            total_cases = self.df['female_cases'].sum()
        
        avoidable_cases = total_cases * paf
        
        print(f"\n=== {gender.upper()} PAF CALCULATION ===")
        print(f"TMREL (reference level): {self.tmrel} μg/m³")
        print(f"Average PM2.5 concentration: {self.df['pm25'].mean():.2f} μg/m³")
        print(f"Population Attributable Fraction (PAF): {paf:.4f} ({paf*100:.2f}%)")
        print(f"Total cases: {total_cases:.0f}")
        print(f"Avoidable cases: {avoidable_cases:.0f}")
        
        return paf, avoidable_cases
    
    def sensitivity_analysis_tmrel(self, tmrel_values=[2.4, 5.0, 7.5, 10.0]):
        """Sensitivity analysis for different TMREL values"""
        original_tmrel = self.tmrel
        results = []
        
        print("\n" + "="*60)
        print("SENSITIVITY ANALYSIS: Effect of TMREL on PAF")
        print("="*60)
        
        for tmrel in tmrel_values:
            self.tmrel = tmrel
            paf_total, avoidable_total = self.calculate_paf('total')
            paf_male, avoidable_male = self.calculate_paf('male')
            paf_female, avoidable_female = self.calculate_paf('female')
            
            results.append({
                'TMREL': tmrel,
                'PAF_Total': paf_total,
                'Avoidable_Total': avoidable_total,
                'PAF_Male': paf_male,
                'Avoidable_Male': avoidable_male,
                'PAF_Female': paf_female,
                'Avoidable_Female': avoidable_female
            })
        
        self.tmrel = original_tmrel  # Restore original value
        
        sensitivity_df = pd.DataFrame(results)
        print("\nSensitivity analysis results:")
        print(sensitivity_df.round(4))
        
        return sensitivity_df

# Main program
def main():
    # Create calculator instance
    calculator = PAFCalculator(tmrel=5.0)
    
    # Load data
    file_path = r"D:\SRT\output_data\最最终原始数据用.xlsx"
    df = calculator.load_and_preprocess_data(file_path)
    
    if df is None:
        print("Data loading failed, please check file path and data format")
        return
    
    print("\n" + "="*60)
    print("CORE PAF ANALYSIS")
    print("="*60)
    
    # 1. Fit exposure-response models and get beta coefficients
    print("\n1. EXPOSURE-RESPONSE RELATIONSHIP FITTING")
    beta_total, model_total = calculator.fit_poisson_model('total')
    beta_male, model_male = calculator.fit_poisson_model('male')
    beta_female, model_female = calculator.fit_poisson_model('female')
    
    # 2. Calculate PAF for each gender group
    print("\n2. POPULATION ATTRIBUTABLE FRACTION (PAF) CALCULATION")
    paf_total, avoidable_total = calculator.calculate_paf('total')
    paf_male, avoidable_male = calculator.calculate_paf('male')
    paf_female, avoidable_female = calculator.calculate_paf('female')
    
    # 3. Sensitivity analysis
    print("\n3. SENSITIVITY ANALYSIS")
    sensitivity_results = calculator.sensitivity_analysis_tmrel()
    
    # 4. Final summary
    print("\n" + "="*60)
    print("FINAL RESULTS SUMMARY")
    print("="*60)
    
    print(f"\nEXPOSURE-RESPONSE COEFFICIENTS (β):")
    print(f"Total population β: {beta_total:.6f}")
    print(f"Male population β: {beta_male:.6f}") 
    print(f"Female population β: {beta_female:.6f}")
    
    print(f"\nRELATIVE RISK PER 10 μg/m³ INCREASE:")
    print(f"Total RR: {np.exp(10 * beta_total):.4f}")
    print(f"Male RR: {np.exp(10 * beta_male):.4f}")
    print(f"Female RR: {np.exp(10 * beta_female):.4f}")
    
    print(f"\nPOPULATION ATTRIBUTABLE FRACTION (PAF) - TMREL = 5.0 μg/m³:")
    print(f"Total PAF: {paf_total:.4f} ({paf_total*100:.1f}%)")
    print(f"Male PAF: {paf_male:.4f} ({paf_male*100:.1f}%)")
    print(f"Female PAF: {paf_female:.4f} ({paf_female*100:.1f}%)")
    
    print(f"\nINTERPRETATION:")
    print(f"PM2.5 exposure accounts for {paf_total*100:.1f}% of lung cancer cases.")
    print(f"If PM2.5 were reduced to {calculator.tmrel} μg/m³, {avoidable_total:.0f} cases could be prevented.")
    
    return calculator, df

# Run the program
if __name__ == "__main__":
    calculator, df = main()