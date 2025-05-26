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

# Define the columns for Net profit after tax for the years 2019-2023
profit_columns = [
    '18. Net profit/(loss) after tax\nYear: 2019\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2020\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2021\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2022\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2023\nUnit: Billions VND\n'
]

# Define the sector column
sector_column = 'Sector L2\n'

# Select the relevant columns
df_sector_profit = df[[sector_column] + profit_columns]

# Group by sector and sum the net profit columns for each year
sector_yearly_profit_sum = df_sector_profit.groupby(sector_column)[profit_columns].sum()

# Calculate the total net profit for each sector across the years 2019-2023
sector_total_profit = sector_yearly_profit_sum.sum(axis=1)

# Sort sectors by total net profit in descending order
top_sectors = sector_total_profit.sort_values(ascending=False)

# Get the top 3 sectors
top_3_sectors = top_sectors.head(3)

# Print the top 3 sectors and their total net profit, rounded to two decimal places
for sector, total_profit in top_3_sectors.items():
    print(f"{sector}: {total_profit:.2f}")
