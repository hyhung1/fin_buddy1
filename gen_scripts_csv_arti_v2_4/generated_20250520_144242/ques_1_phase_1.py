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

# Define the net profit columns for the years 2019 to 2023, using the exact column names
net_profit_cols = [
    "18. Net profit/(loss) after tax\nYear: 2019\nUnit: Billions VND\n",
    "18. Net profit/(loss) after tax\nYear: 2020\nUnit: Billions VND\n",
    "18. Net profit/(loss) after tax\nYear: 2021\nUnit: Billions VND\n",
    "18. Net profit/(loss) after tax\nYear: 2022\nUnit: Billions VND\n",
    "18. Net profit/(loss) after tax\nYear: 2023\nUnit: Billions VND\n",
]

# Define the sector column, using the exact column name
sector_col = "Sector L2\n"

# Select the sector column and net profit columns from the DataFrame
df_subset = df[[sector_col] + net_profit_cols].copy()

# Calculate the total net profit for each row by summing across the specified years
df_subset['Total Net Profit'] = df_subset[net_profit_cols].sum(axis=1)

# Group the DataFrame by sector and sum the calculated total net profit for each sector
sector_total_net_profit = df_subset.groupby(sector_col)['Total Net Profit'].sum()

# Sort the sectors by their total net profit in descending order and select the top 3
top_3_sectors = sector_total_net_profit.sort_values(ascending=False).head(3)

# Print the result, formatting the sector name by removing trailing newline/space and rounding the profit
for sector_name, total_profit in top_3_sectors.items():
    print(f"{sector_name.strip()}: {total_profit:.2f}")
