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

# Define column names carefully, including potential hidden characters
ticker_col = 'Ticker\n'
company_col = 'Company Name\n'
sector_col = 'Sector L2\n'

# Net Profit columns for 2019-2023
net_profit_cols = [
    '18. Net profit/(loss) after tax\nYear: 2019\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2020\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2021\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2022\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2023\nUnit: Billions VND\n'
]

# Owner's Equity columns for 2019-2023
owner_equity_cols = [
    "II. OWNER'S EQUITY\nYear: 2019\nUnit: Billions VND\n",
    "II. OWNER'S EQUITY\nYear: 2020\nUnit: Billions VND\n",
    "II. OWNER'S EQUITY\nYear: 2021\nUnit: Billions VND\n",
    "II. OWNER'S EQUITY\nYear: 2022\nUnit: Billions VND\n",
    "II. OWNER'S EQUITY\nYear: 2023\nUnit: Billions VND\n"
]

# Minority Interests columns for 2019-2023
minority_interests_cols = [
    '1.13. Minority interests\nYear: 2019\nUnit: Billions VND\n',
    '1.13. Minority interests\nYear: 2020\nUnit: Billions VND\n',
    '1.13. Minority interests\nYear: 2021\nUnit: Billions VND\n',
    '1.13. Minority interests\nYear: 2022\nUnit: Billions VND\n',
    '1.13. Minority interests\nYear: 2023\nUnit: Billions VND\n'
]

# Calculate Total Net Profit for 2019-2023 for ranking
df['Total Net Profit 2019-2023'] = df[net_profit_cols].sum(axis=1)

# Calculate Parent Equity for each year 2019-2023
parent_equity_years = ['2019', '2020', '2021', '2022', '2023']
parent_equity_cols_calculated = []

for i, year in enumerate(parent_equity_years):
    parent_equity_col_name = f'Parent Equity {year}'
    df[parent_equity_col_name] = df[owner_equity_cols[i]] - df[minority_interests_cols[i]]
    parent_equity_cols_calculated.append(parent_equity_col_name)


# Group by sector and find the top 3 companies by Total Net Profit
top_companies_per_sector = df.groupby(sector_col, group_keys=False).apply(
    lambda x: x.nlargest(3, 'Total Net Profit 2019-2023')
)

# Select the columns for the final output
output_cols = [sector_col, company_col, ticker_col] + parent_equity_cols_calculated
final_output_df = top_companies_per_sector[output_cols]

# Print the results
# Sort by sector for cleaner output, although not strictly required by prompt
final_output_df = final_output_df.sort_values(by=sector_col)

for index, row in final_output_df.iterrows():
    print(f"Sector: {row[sector_col].strip()}")
    print(f"Company: {row[company_col].strip()} ({row[ticker_col].strip()})")
    for col in parent_equity_cols_calculated:
        year = col.split(' ')[-1] # Extract year from column name
        print(f"  Parent Equity {year}: {row[col]:.2f}")
