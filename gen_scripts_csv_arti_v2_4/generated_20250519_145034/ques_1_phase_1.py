import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
df = pd.read_csv(r"C:\Users\HP\Downloads\excel_bud\fin_buddy\python_backend\uploads\2023Q4_Sheet1.csv")
# Make cleaned aliases for columns (whitespace variants) so any reference works
orig_cols = df.columns.tolist()
strip_cols = pd.Series(orig_cols).str.strip().tolist()
collapsed_cols = (pd.Series(orig_cols)
                 .str.replace(r"\s+", " ", regex=True)
                 .str.strip()
                 .tolist())
for orig, s, c in zip(orig_cols, strip_cols, collapsed_cols):
    if s not in orig_cols and s not in df.columns:
        df[s] = df[orig]
    if c not in orig_cols and c not in df.columns:
        df[c] = df[orig]
# Remove duplicate columns if any
df = df.loc[:, ~df.columns.duplicated()]
pd.set_option('display.float_format', '{:,.0f}'.format)

# Filter data for years 2019 to 2023
df_filtered_years = df[df['Year\n'].between(2019, 2023)]

# Group by Sector and sum Net Profit
sector_profit = df_filtered_years.groupby('Sector\n')['Net Profit\n'].sum()

# Get the top 5 sectors by total Net Profit
top_5_sectors = sector_profit.nlargest(5)

# Print the result
for sector, profit in top_5_sectors.items():
    print(f"{sector}: {profit:.2f}")
