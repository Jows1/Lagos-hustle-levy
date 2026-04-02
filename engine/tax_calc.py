import pandas as pd

def calculate_monthly_cash(row):
    # 1. Reverse-engineer the pure 'Dry' morning base fare
    # The generator applied multipliers if Is_Rainy_Day was 1, so we strip them out first.
    daily_generated = row['Daily_Commute_Cost']
    
    if row['Is_Rainy_Day'] == 1:
        if row['Mode'] == 'Danfo':
            morning_base = (daily_generated / 1.5) / 2.0
        elif row['Mode'] == 'Private Car':
            # Matching the 1.3 multiplier used in the original generator script
            morning_base = (daily_generated / 1.3) / 2.0
        else:
            morning_base = daily_generated / 2.0 # BRT is fixed
    else:
        morning_base = daily_generated / 2.0

    # 2. Define the 'Lagos 22-Day Grind'
    dry_days = 18
    rainy_days = 4
    
    # 3. Calculate Dry Day Total
    if row['Mode'] == 'Danfo':
        evening_dry = morning_base * 1.20 # 20% evening rush hour surge
    else:
        evening_dry = morning_base # BRT and Private Car don't have an evening 'fare' surge
        
    daily_dry_total = morning_base + evening_dry
    
    # 4. Calculate Rainy Day Total
    if row['Mode'] == 'Danfo':
        morning_rainy = morning_base * 1.50
        evening_rainy = evening_dry * 1.50
    elif row['Mode'] == 'Private Car':
        # Applying the realistic 25% fuel inefficiency tax for rain
        morning_rainy = morning_base * 1.25
        evening_rainy = evening_dry * 1.25
    else:
        morning_rainy = morning_base
        evening_rainy = evening_dry
        
    daily_rainy_total = morning_rainy + evening_rainy
    
    # 5. Return the Monthly Total
    return (daily_dry_total * dry_days) + (daily_rainy_total * rainy_days)


def calculate_commute_tax():
    print("⏳ Loading raw data and calculating the Commute Tax...")
    df = pd.read_csv("data/lagos_commute_raw.csv")

    # Apply the realistic monthly cash function
    df['Monthly_Cash_Spend'] = df.apply(calculate_monthly_cash, axis=1)

    # 1. Base Variables
    df['Hourly_Rate'] = df['Monthly_Income'] / 160 # 160 standard working hours a month
    df['Monthly_Hours_Lost'] = (df['Daily_Time_Mins'] * 22) / 60

    # 2. THE REFINED "PAIN SCORE" (Weighted)
    # Opportunity Cost weighted at 40% of professional value (Leisure/Recovery time)
    df['Opportunity_Cost'] = df['Monthly_Hours_Lost'] * (df['Hourly_Rate'] * 0.40)
    
    # Sleep Debt weighted at 25% of professional value (Health/Burnout toll)
    df['Sleep_Debt_Cost'] = (df['Sleep_Debt_Hours'] * 22) * (df['Hourly_Rate'] * 0.25)

    # 3. Total Monthly Commute Tax
    df['Total_Commute_Tax'] = (
        df['Monthly_Cash_Spend'] + 
        df['Opportunity_Cost'] + 
        df['Sleep_Debt_Cost']
    )

    # 4. Calculate Final Percentage
    df['Tax_Percentage_of_Income'] = (df['Total_Commute_Tax'] / df['Monthly_Income']) * 100

    # Round columns for clean data presentation
    df['Monthly_Cash_Spend'] = df['Monthly_Cash_Spend'].round(2)
    df['Opportunity_Cost'] = df['Opportunity_Cost'].round(2)
    df['Total_Commute_Tax'] = df['Total_Commute_Tax'].round(2)
    df['Tax_Percentage_of_Income'] = df['Tax_Percentage_of_Income'].round(2)

    df.to_csv("data/lagos_commute_enriched.csv", index=False)
    print("✅ Refined Commute Tax (Weighted) calculated and saved to data/lagos_commute_enriched.csv!")


if __name__ == "__main__":
    calculate_commute_tax()