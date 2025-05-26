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

# Define the columns for net profit for each year
net_profit_cols = [
    '18. Net profit/(loss) after tax\nYear: 2019\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2020\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2021\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2022\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2023\nUnit: Billions VND\n',
]

# Calculate the sum of net profit for each company across all years (2019-2023)
# Use .sum(axis=1) to sum across columns for each row
# Ensure all specified columns exist before summing (though they are provided by the user).
# Let's create a temporary column for the total profit per company
df['Total Net Profit 2019-2023'] = df[net_profit_cols].sum(axis=1)

# Group by sector and sum the total net profit for each sector
sector_total_profit = df.groupby('Sector L2\n')['Total Net Profit 2019-2023'].sum()

# Sort the sectors by the total net profit in descending order and get the top 5
top_5_sectors = sector_total_profit.sort_values(ascending=False).head(5)

# Print the result
for sector, total_profit in top_5_sectors.items():
    print(f"{sector}: {total_profit:.2f}")

# Drop the temporary column to clean up the DataFrame if necessary (optional but good practice)
# df = df.drop(columns=['Total Net Profit 2019-2023']) # Not needed as per strict instructions not to alter df
