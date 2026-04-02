import pandas as pd
import numpy as np
import random

# THE LAGOS 2026 PRICE MATRIX [Danfo, BRT, Private Car]
# Private Car rates mathematically grounded based on a 2012 4-Cylinder Sedan (Camry/Corolla)
# Assuming 6.5 km/L in standard traffic at ₦1,200/L
PRICE_MATRIX = {
    # 40km trip. ~6.5L fuel + toll
    ("Ikorodu", "Victoria Island"): [1800, 1100, 7800], 
    # ~25km trip. ~4L fuel
    ("Ikorodu", "Ikeja"): [1200, 750, 4800],           
    # ~35km trip. ~5.5L fuel + toll
    ("Egbeda", "Victoria Island"): [1600, 980, 7000],  
    # ~15km trip. ~2.5L fuel
    ("Egbeda", "Ikeja"): [800, 450, 3000],             
    # ~18km trip. ~3L fuel + toll
    ("Surulere", "Victoria Island"): [900, 570, 4000], 
    # ~12km trip. ~2L fuel
    ("Surulere", "Ikeja"): [900, 570, 2400],           
}

def generate_lagos_data(n=1000):
    data = []
    hubs = ["Ikorodu", "Egbeda", "Surulere"]
    destinations = ["Victoria Island", "Ikeja"]

    for i in range(n):
        home = random.choice(hubs)
        work = random.choice(destinations)
        
        # 1. Determine Income FIRST
        if random.random() < 0.20: # 20% are Minimum Wage
            income = random.randint(70000, 100000)
        else:
            income = random.randint(150000, 850000)

        # 2. Assign Transport Mode based on Income Capacity (The Fix!)
        if income <= 100000:
            # Min wage: 70% Danfo, 30% BRT, 0% Car
            mode = random.choices(["Danfo", "BRT"], weights=[70, 30])[0]
        elif income <= 350000:
            # Lower Middle Class: 50% Danfo, 40% BRT, 10% Car
            mode = random.choices(["Danfo", "BRT", "Private Car"], weights=[50, 40, 10])[0]
        else:
            # Execs/Upper Middle: 10% Danfo, 20% BRT, 70% Car
            mode = random.choices(["Danfo", "BRT", "Private Car"], weights=[10, 20, 70])[0]

        # 3. The Rain Factor
        is_rainy = 1 if random.random() < 0.20 else 0
        
        # 4. Pull Base Price
        base_prices = PRICE_MATRIX[(home, work)]
        if mode == "Danfo": base_fare = base_prices[0]
        elif mode == "BRT": base_fare = base_prices[1]
        else: base_fare = base_prices[2]

        # Apply initial generator modifiers (tax_calc will reverse engineer this cleanly now)
        daily_cost = (base_fare * 2) 
        if is_rainy:
            if mode == "Danfo": daily_cost *= 1.5 
            elif mode == "Private Car": daily_cost *= 1.3 
        
        # 5. Time & Sleep Math
        base_time = 120 if home != "Surulere" else 60 
        total_daily_time = (base_time * 2) + (is_rainy * 90)
        
        sleep_hours = 5 if home != "Surulere" else 6.5
        sleep_debt = 8 - sleep_hours

        data.append({
            "User_ID": f"LOS-{i:04d}",
            "Home_Hub": home,
            "Work_Hub": work,
            "Mode": mode,
            "Monthly_Income": income,
            "Is_Rainy_Day": is_rainy,
            "Daily_Commute_Cost": daily_cost,
            "Daily_Time_Mins": total_daily_time,
            "Sleep_Debt_Hours": sleep_debt
        })

    df = pd.DataFrame(data)
    df.to_csv("data/lagos_commute_raw.csv", index=False)
    print(f"✅ Generated {n} SMART Lagosian personas in data/lagos_commute_raw.csv")

if __name__ == "__main__":
    generate_lagos_data()