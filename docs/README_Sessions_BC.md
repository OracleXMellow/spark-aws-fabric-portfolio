# Week 1 — Sessions B & C (README)

This README documents exactly what was done in **Session B** and **Session C** for Week 1.

---

## Session B (2 hours) — SQL Basics + AWS S3 Lake Structure

### Objective
- Practice SQL fundamentals (**SELECT**, **GROUP BY**, **JOIN**, **Window function**).
- Create an AWS S3 bucket with a standard data lake prefix structure (**bronze/silver/gold/logs/tmp**).
- Upload the raw dataset to the **Bronze** layer.
- Save proof (screenshots) and commit changes to GitHub.

---

### Part 1 — SQL Setup (SQLite + DBeaver)

#### Why SQLite + DBeaver
- The dataset is a **CSV** file.
- SQLite allows converting the CSV into a lightweight database file (`.db`) with a real SQL table.
- DBeaver is used as the SQL client/editor to run queries and view results.

#### Step B1.1 — Create a SQLite database from the CSV
**Input file:**
- `data/car_price_dataset_medium.csv`

**Output file created:**
- `data/car_prices.db`

**Python script created:**
- `src/make_sqlite_db.py`

**Script:**
```python
import pandas as pd
import sqlite3
from pathlib import Path

CSV_PATH = Path("data/car_price_dataset_medium.csv")
DB_PATH = Path("data/car_prices.db")

def main():
    df = pd.read_csv(CSV_PATH)
    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql("car_prices", conn, if_exists="replace", index=False)

    print(f"✅ Created SQLite DB: {DB_PATH}")
    print("✅ Table: car_prices")

if __name__ == "__main__":
    main()
```

**Command run (repo root):**
```powershell
python src/make_sqlite_db.py
```

✅ Expected result:
- A file `data/car_prices.db` exists
- A table `car_prices` exists inside the DB

---

#### Step B1.2 — Connect DBeaver to SQLite DB
⚠️ Important: Connect to the `.db` file, not the CSV.

**DBeaver steps:**
1. Open **DBeaver**
2. **Database → New Database Connection**
3. Select **SQLite**
4. Browse to: `data/car_prices.db`
5. Finish
6. Expand in Database Navigator:
   - Schemas → main → Tables → `car_prices`
7. Right-click `car_prices` → **View Data → All Rows**

---

#### Step B1.3 — SQL practice file + requirements
**SQL file created:**
- `sql/week1_basics.sql`

**Requirements covered:**
- 2 × SELECT queries
- 2 × GROUP BY queries
- 1 × JOIN query (using a derived table/CTE)
- 1 × window function query (ROW_NUMBER)

**Proof saved (recommended):**
- `docs/week1_sql_results_1.png`
- `docs/week1_sql_results_2.png`

---

### Part 2 — AWS S3 Lake Structure

#### Step B2.1 — Create S3 bucket
**AWS steps:**
1. AWS Console → Search **S3**
2. Click **Create bucket**
3. Bucket name: `yourname-data-lake-dev` (must be globally unique)
   - Example: `mamello-data-lake-dev`
4. Choose a region (default is fine)
5. Create bucket

#### Step B2.2 — Create prefixes (folders)
Inside the bucket, create these prefixes:
- `bronze/`
- `silver/`
- `gold/`
- `logs/`
- `tmp/`

#### Step B3 — Upload raw file to Bronze
Upload local file:
- `data/car_price_dataset_medium.csv`

To S3 path:
- `bronze/week1/car_price_dataset_medium.csv`

---

### Step B4 — Git commit (Session B)
**What to commit:**
- `sql/week1_basics.sql`
- `src/make_sqlite_db.py`
- `docs/week1_sql_results_*.png` (if you captured screenshots)

**Commands:**
```powershell
git add sql/week1_basics.sql src/make_sqlite_db.py docs/
git commit -m "Week1: SQL basics + S3 lake structure"
git push
```

---

## Session C (2 hours) — Excel Fundamentals + Mini Dashboard

### Objective
- Build an Excel mini dashboard from the dataset:
  - Clean dataset table (`tbl_data`)
  - Add calculated fields
  - Demonstrate analyst formulas (XLOOKUP, SUMIFS, IF, TEXT/DATE)
  - Create PivotTables + Slicers
- Save proof (screenshot) and commit changes.

---

### Step C1 — Create Excel workbook + import data
**Workbook created:**
- `excel/week1_dashboard.xlsx`

**Data source used:**
- `data/processed/car_prices_clean.csv`

**Excel steps:**
1. Excel → Blank workbook
2. Data → **Get Data → From Text/CSV**
3. Select `data/processed/car_prices_clean.csv`
4. Load as a Table into a new worksheet
5. Rename the sheet to: `Data`

---

### Step C1.1 — Convert to Table + name it
1. Click inside the dataset
2. Ctrl + T → OK
3. Table Design → **Table Name**: `tbl_data`

✅ The Table Name must not contain spaces or special characters.

---

### Step C2 — Add calculated columns (inside the table)
Add new columns to `tbl_data` (these support analysis + pivots).

#### KM_Band
```excel
=IF([@[Kilometers_Driven]]<50000;"<50k";
IF([@[Kilometers_Driven]]<100000;"50k-100k";
IF([@[Kilometers_Driven]]<150000;"100k-150k";"150k+")))
```

#### Price_Band
```excel
=IF([@[Price_USD]]>=87089;"High";
IF([@[Price_USD]]>=56807;"Mid";"Low"))
```

#### Auto_Flag
```excel
=IF([@[Transmission]]="Automatic";"Auto";"Manual")
```

---

### Important: Numeric conversion for Price_USD
During import, **Price_USD was detected as text**, which caused:
- SUMIFS returning 0
- calculations failing

✅ Fix: Create a numeric helper column `Price_USD_Num`:

```excel
=NUMBERVALUE([@[Price_USD]];".";",")
```

Now calculations should use `Price_USD_Num`.

#### Price_per_CC
```excel
=[@[Price_USD_Num]]/[@[Engine_CC]]
```

---

### Step C2.1 — Calc sheet (XLOOKUP + SUMIFS examples)
Create a sheet named `Calc` and set up input cells (example):
- B2: Car_ID input
- E2: Brand input (or use a dropdown list)

#### XLOOKUP (Price by Car_ID)
```excel
=XLOOKUP($B$2;tbl_data[Car_ID];tbl_data[Price_USD_Num];"Not found")
```

#### XLOOKUP (Brand by Car_ID)
```excel
=XLOOKUP($B$2;tbl_data[Car_ID];tbl_data[Brand];"Not found")
```

#### SUMIFS (Total Price for Brand)
```excel
=SUMIFS(tbl_data[Price_USD_Num];tbl_data[Brand];TRIM($E$2))
```

#### AVERAGEIFS (Safe from #DIV/0!)
```excel
=IFERROR(AVERAGEIFS(tbl_data[Price_USD_Num];tbl_data[Brand];TRIM($E$2));0)
```

---

### Step C3 — PivotTables + Slicers
Create a sheet named `Dashboard`.

#### Pivot 1: Average price by Brand
- Rows: `Brand`
- Values: **Average** of `Price_USD_Num`

#### Pivot 2: Count by Fuel_Type and Transmission
- Rows: `Fuel_Type`
- Columns: `Transmission`
- Values: **Count** of `Car_ID`

#### Slicers (recommended)
Add slicers for:
- Brand
- Fuel_Type
- Transmission
- Model_Year
- Price_Band

Connect slicers to both pivots:
- Slicer → **Report Connections** → tick both PivotTables

---

### Step C4 — Proof screenshot
Save a screenshot of the Dashboard to:
- `docs/week1_excel_dashboard.png`

---

### Step C5 — Git commit (Session C)
Commit either the Excel file + screenshot, or only screenshots (to keep repo small).

**Commit (with Excel file):**
```powershell
git add excel/week1_dashboard.xlsx docs/week1_excel_dashboard.png
git commit -m "Week1: Excel pivot dashboard + slicers"
git push
```

**Commit (screenshot only):**
```powershell
git add docs/week1_excel_dashboard.png
git commit -m "Week1: Excel dashboard screenshot"
git push
```

---

## Done Definition (Sessions B & C)
✅ Session B:
- SQL file created and queries executed
- SQLite DB created (optional but recommended)
- S3 bucket + prefixes created
- Raw dataset uploaded to Bronze layer
- Proof screenshots saved + committed

✅ Session C:
- Excel workbook created with `tbl_data`
- Calculated fields added (with numeric conversion where needed)
- XLOOKUP + SUMIFS working
- Pivot dashboard + slicers created
- Screenshot proof saved + committed
