# Spark + AWS + Fabric Portfolio

This repository is my hands-on learning + portfolio journey to become:
- **Data Engineer (Databricks/Spark)**
- **Cloud Data Engineer (AWS + Microsoft Fabric)**
- **Automation-focused (Power tools later)**
- **Service Delivery / Operations-ready (runbooks, monitoring later)**

---

## Week 1 — Python Environment + Dataset Profiling + CSV/Parquet Outputs

### Goal
Set up a professional project workspace and run a first data pipeline step:
- Load a dataset using Python
- Perform basic profiling checks
- Save processed outputs as **CSV** and **Parquet**

---

## Project Structure

```
spark-aws-fabric-portfolio/
├── src/                  # Python scripts
│   └── load_car_prices.py
├── data/                 # local input data
│   ├── car_price_dataset_medium.csv
│   └── processed/        # generated outputs
│       ├── car_prices_clean.csv
│       └── car_prices_clean.parquet
├── docs/                 # screenshots/diagrams (optional)
├── sql/                  # SQL practice queries (later)
├── notebooks/            # Databricks notebooks (later)
├── ops/                  # runbooks (later)
└── .venv/                # Python virtual environment (local)
```

---

## Dataset

**File:** `data/car_price_dataset_medium.csv`  
**Columns:**
- Car_ID
- Brand
- Model_Year
- Kilometers_Driven
- Fuel_Type
- Transmission
- Owner_Type
- Engine_CC
- Max_Power_bhp
- Mileage_kmpl
- Seats
- Price_USD

---

## Python Setup (Virtual Environment)

A **virtual environment** keeps project dependencies isolated (so packages don’t clash across projects).

### 1) Create venv (run in repo root)
```powershell
python -m venv .venv
```

### 2) Activate venv (PowerShell)
```powershell
.\.venv\Scripts\Activate
```

✅ When active, your terminal shows:
`(.venv)`

### 3) Install required packages
```powershell
python -m pip install --upgrade pip
pip install pandas requests pyarrow
```

---

## Script: `src/load_car_prices.py`

### What it does
1. Reads the dataset into a pandas DataFrame  
2. Prints basic profiling information:
   - Rows and columns
   - Missing values per column
   - Summary statistics for `Price_USD`
3. Saves processed outputs:
   - `data/processed/car_prices_clean.csv`
   - `data/processed/car_prices_clean.parquet`

### Code
```python
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
```

---

## How to Run

From the repo root:
```powershell
python src/load_car_prices.py
```

---

## Results (Successful Run)

- Dataset shape: **(1000, 12)**
- Missing values: **0 in every column**
- `Price_USD` summary:
  - count: 1000
  - mean: 59217.249420
  - std: 33545.254183
  - min: 3028.420000
  - 25%: 30030.822500
  - 50% (median): 56806.745000
  - 75%: 87088.897500
  - max: 119611.940000

✅ Output files saved to:
- `data/processed/car_prices_clean.csv`
- `data/processed/car_prices_clean.parquet`

To confirm:
```powershell
dir data\processed
```

---

## Troubleshooting

### Parquet error: "Missing optional dependency 'pyarrow'"
This happens if:
- the venv is not active, or
- `pyarrow` isn’t installed in the active environment.

Fix:
1) Activate venv: `.\.venv\Scripts\Activate`
2) Install pyarrow:
```powershell
pip install pyarrow
```

---

## Next Steps (Week 1 remaining / Week 2 preview)
- Add SQL practice queries in `sql/week1_basics.sql`
- Build an Excel Pivot dashboard + slicers using `data/processed/car_prices_clean.csv`
- Upload raw + processed files to AWS S3 (Bronze/Silver concept)
- Begin Databricks/Spark transformations (Bronze → Silver → Gold)
- Start publishing curated outputs into Microsoft Fabric for reporting
