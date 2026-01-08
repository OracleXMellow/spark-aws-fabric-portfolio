import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/car_price_dataset_medium.csv")
OUT_DIR = Path("data/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    df = pd.read_csv(DATA_PATH)

    # Basic checks (profiling)
    print("Rows, Cols:", df.shape)
    print("Missing values per column:\n", df.isna().sum())
    print("Price_USD stats:\n", df["Price_USD"].describe())

    # Save processed outputs
    df.to_csv(OUT_DIR / "car_prices_clean.csv", index=False)
    df.to_parquet(OUT_DIR / "car_prices_clean.parquet", index=False)

    print("\n✅ Saved outputs to data/processed/")

if __name__ == "__main__":
    main()