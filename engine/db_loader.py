import pandas as pd
from sqlalchemy import create_engine
import os

def load_to_database():
    print("⏳ Reading enriched data...")
    csv_path = "data/lagos_commute_enriched.csv"
    
    if not os.path.exists(csv_path):
        print("❌ Error: Enriched CSV not found. Run tax_calc.py first.")
        return

    df = pd.read_csv(csv_path)

    # Create a local SQLite database file named 'lagos_commute.db'
    db_path = "sqlite:///data/lagos_commute.db"
    engine = create_engine(db_path)

    print("🔌 Connecting to the Database...")
    
    # Load the dataframe into a SQL table named 'commuter_metrics'
    # if_exists='replace' means if we run this again, it updates with fresh data
    df.to_sql('commuter_metrics', con=engine, if_exists='replace', index=False)
    
    print(f"✅ Successfully loaded {len(df)} rows into the 'commuter_metrics' SQL table!")

if __name__ == "__main__":
    load_to_database()