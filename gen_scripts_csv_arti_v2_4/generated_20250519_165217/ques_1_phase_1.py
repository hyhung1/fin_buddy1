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

# Define the columns for Net profit/(loss) after tax for the years 2019-2023
net_profit_cols = [
    '18. Net profit/(loss) after tax\nYear: 2019\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2020\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2021\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2022\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2023\nUnit: Billions VND\n'
]

# Calculate the total net profit for the period 2019-2023 for each company
# Use .sum(axis=1) to sum across the specified columns for each row
df['Total Net Profit 2019-2023'] = df[net_profit_cols].sum(axis=1)

# Group the DataFrame by the 'Sector L2' column and sum the calculated total net profit
sector_net_profit_sum = df.groupby('Sector L2\n')['Total Net Profit 2019-2023'].sum()

# Sort the sectors by the total net profit in descending order
sorted_sectors = sector_net_profit_sum.sort_values(ascending=False)

# Get the top 5 sectors
top_5_sectors = sorted_sectors.head(5)

# Print the result
print("Top 5 sectors with highest total net profit from 2019 to 2023:")
for sector, total_profit in top_5_sectors.items():
    print(f"{sector}: {total_profit:.2f}")
