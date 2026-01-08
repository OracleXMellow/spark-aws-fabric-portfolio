import pandas as pd
import sqlite3
from pathlib import Path

def main():
    cwd = Path.cwd()
    print("📌 Running from:", cwd)

    csv_path = (cwd / "data" / "car_price_dataset_medium.csv").resolve()
    db_path  = (cwd / "data" / "car_prices.db").resolve()

    print("📄 CSV:", csv_path)
    print("💾 DB :", db_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    df = pd.read_csv(csv_path)
    print("✅ Loaded CSV:", df.shape)

    with sqlite3.connect(db_path) as conn:
        df.to_sql("car_prices", conn, if_exists="replace", index=False)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM car_prices;")
        print("✅ Rows inserted:", cur.fetchone()[0])

    print("✅ Database created:", db_path)

if __name__ == "__main__":
    main()