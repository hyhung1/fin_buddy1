import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
df = pd.read_csv(r"C:\Users\HP\Downloads\excel_bud\fin_buddy\python_backend\uploads\2023Q4_Sheet1_processed_header7.csv")
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

# Define the columns for Net Profit for each year from 2019 to 2023
net_profit_columns = [
    "18. Net profit/(loss) after tax\nYear: 2019\nUnit: Billions VND\n",
    "18. Net profit/(loss) after tax\nYear: 2020\nUnit: Billions VND\n",
    "18. Net profit/(loss) after tax\nYear: 2021\nUnit: Billions VND\n",
    "18. Net profit/(loss) after tax\nYear: 2022\nUnit: Billions VND\n",
    "18. Net profit/(loss) after tax\nYear: 2023\nUnit: Billions VND\n",
]

# Calculate the sum of Net Profit for each company across the years 2019-2023
# Use .sum(axis=1) to sum across columns for each row.
# .fillna(0) can be used if there's a concern about missing data affecting the sum,
# but .sum() by default skips NaNs, so it's often not strictly necessary unless NaNs should be treated as 0.
df_with_total_profit = df.copy() # Create a copy to add the helper column
df_with_total_profit['Total Net Profit 2019-2023'] = df_with_total_profit[net_profit_columns].sum(axis=1)

# Group by Sector and sum the total net profit
sector_net_profit = df_with_total_profit.groupby('Sector L2\n')['Total Net Profit 2019-2023'].sum()

# Sort the sectors by total net profit in descending order and get the top 5
top_5_sectors = sector_net_profit.sort_values(ascending=False).head(5)

# Print the top 5 sectors and their total net profit
print("Top 5 Sectors with Highest Total Net Profit (2019-2023):")
# Iterate through the resulting Series items (sector name and total profit)
for sector, total_profit in top_5_sectors.items():
    print(f"{sector}: {total_profit:.2f}")
