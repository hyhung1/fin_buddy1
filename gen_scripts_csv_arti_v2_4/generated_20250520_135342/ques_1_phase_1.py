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

import pandas as pd

# Define column names, handling potential extra whitespace/newlines
ticker_col = 'Ticker\n'
sector_col = 'Sector L2\n'

net_profit_cols = {}
owner_equity_cols = {}
minority_interest_cols = {}
years = range(2019, 2024)

for year in years:
    net_profit_cols[year] = f'18. Net profit/(loss) after tax\nYear: {year}\nUnit: Billions VND\n'
    owner_equity_cols[year] = f'II. OWNER\'S EQUITY\nYear: {year}\nUnit: Billions VND\n'
    minority_interest_cols[year] = f'1.13. Minority interests\nYear: {year}\nUnit: Billions VND\n'

# Calculate total net profit for ranking
net_profit_column_list = [net_profit_cols[year] for year in years]
df['Total_Net_Profit_2019_2023'] = df[net_profit_column_list].sum(axis=1)

# Calculate Parent Equity for each year
parent_equity_cols_names = {}
for year in years:
    parent_equity_col_name = f'Parent_Equity_{year}'
    df[parent_equity_col_name] = df[owner_equity_cols[year]] - df[minority_interest_cols[year]]
    parent_equity_cols_names[year] = parent_equity_col_name

# Group by sector and find top 3 companies based on Total_Net_Profit_2019_2023
top_companies_per_sector = df.groupby(sector_col, group_keys=False).apply(
    lambda g: g.nlargest(3, 'Total_Net_Profit_2019_2023')
)

# Select and reorder columns for printing
output_columns = [ticker_col, sector_col]
for year in years:
    output_columns.append(net_profit_cols[year])
for year in years:
    output_columns.append(parent_equity_cols_names[year])

# Sort by sector and then by total profit within each sector for cleaner output
top_companies_per_sector_sorted = top_companies_per_sector.sort_values(
    by=[sector_col, 'Total_Net_Profit_2019_2023'], ascending=[True, False]
)[output_columns]

# Print the results
for index, row in top_companies_per_sector_sorted.iterrows():
    ticker = row[ticker_col].strip()
    sector = row[sector_col].strip()
    print(f"Ticker: {ticker}, Sector: {sector}")

    # Print Net Profit per year
    net_profit_output = "  Net Profit (Billions VND):"
    for year in years:
        net_profit_output += f" {year}: {row[net_profit_cols[year]]:.2f}"
    print(net_profit_output)

    # Print Parent Equity per year
    parent_equity_output = "  Parent Equity (Billions VND):"
    for year in years:
        parent_equity_output += f" {year}: {row[parent_equity_cols_names[year]]:.2f}"
    print(parent_equity_output)

    print("-" * 30) # Separator for readability
