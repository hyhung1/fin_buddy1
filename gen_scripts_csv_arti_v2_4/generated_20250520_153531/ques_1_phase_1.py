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

# Define the columns for net profit from 2019 to 2023
net_profit_cols = [
    '18. Net profit/(loss) after tax\nYear: 2019\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2020\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2021\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2022\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2023\nUnit: Billions VND\n'
]

# Define the columns for Owner's Equity and Minority Interests from 2019 to 2023
owner_equity_cols = [
    'II. OWNER\'S EQUITY\nYear: 2019\nUnit: Billions VND\n',
    'II. OWNER\'S EQUITY\nYear: 2020\nUnit: Billions VND\n',
    'II. OWNER\'S EQUITY\nYear: 2021\nUnit: Billions VND\n',
    'II. OWNER\'S EQUITY\nYear: 2022\nUnit: Billions VND\n',
    'II. OWNER\'S EQUITY\nYear: 2023\nUnit: Billions VND\n'
]

minority_interests_cols = [
    '1.13. Minority interests\nYear: 2019\nUnit: Billions VND\n',
    '1.13. Minority interests\nYear: 2020\nUnit: Billions VND\n',
    '1.13. Minority interests\nYear: 2021\nUnit: Billions VND\n',
    '1.13. Minority interests\nYear: 2022\nUnit: Billions VND\n',
    '1.13. Minority interests\nYear: 2023\nUnit: Billions VND\n'
]

# Define key columns
ticker_col = 'Ticker\n'
sector_col = 'Sector L2\n'

# Calculate total net profit for each company across the years 2019-2023
# Use fillna(0) to handle potential missing values for summation
df['Total Net Profit 2019-2023'] = df[net_profit_cols].fillna(0).sum(axis=1)

# Define the target sectors based on the previous result (Banks, Real Estate, Food & Beverage)
target_sectors = ['Banks', 'Real Estate', 'Food & Beverage']

# Filter the DataFrame to include only the target sectors
# Make a copy to avoid SettingWithCopyWarning
filtered_df = df[df[sector_col].isin(target_sectors)].copy()

# Find the top 3 companies in each sector by total net profit
# Use group_keys=False to prevent adding an extra index level from the group key
top_companies_per_sector = filtered_df.groupby(sector_col, group_keys=False).apply(
    lambda g: g.nlargest(3, 'Total Net Profit 2019-2023')
)

# Get the tickers of these top companies
top_company_tickers = top_companies_per_sector[ticker_col].unique().tolist()

# Filter the original DataFrame to get the rows for only these top companies across all years
final_companies_df = df[df[ticker_col].isin(top_company_tickers)].copy()

# Calculate Parent Equity for each year for the selected companies
parent_equity_years = {}
for i, year in enumerate(range(2019, 2024)):
    owner_col = owner_equity_cols[i]
    minority_col = minority_interests_cols[i]
    parent_equity_col_name = f'Parent Equity {year}'
    # Use fillna(0) for calculation to handle potential NaN values gracefully
    final_companies_df[parent_equity_col_name] = final_companies_df[owner_col].fillna(0) - final_companies_df[minority_col].fillna(0)
    parent_equity_years[year] = parent_equity_col_name

# Select columns to print: Ticker and Parent Equity for each year
output_cols = [ticker_col] + [parent_equity_years[year] for year in range(2019, 2024)]

# Sort the final companies DataFrame for cleaner output (optional but good practice)
# Sort by total profit calculated earlier to show top companies first within their original sector
# Need to merge or join the total profit back or sort based on the top_companies_per_sector order
# A simpler approach is to iterate through the found top companies
# Let's collect the results for printing in the order of the top companies found
print_data = []
for sector in target_sectors:
    companies_in_sector = top_companies_per_sector[top_companies_per_sector[sector_col] == sector]
    for index, row in companies_in_sector.iterrows():
        ticker = row[ticker_col].strip()
        # Find this row in the final_companies_df to get parent equity
        company_row = final_companies_df[final_companies_df[ticker_col] == row[ticker_col]].iloc[0]
        parent_eq_values = [company_row[parent_equity_years[year]] for year in range(2019, 2024)]
        print_data.append({
            'Ticker': ticker,
            'Parent_Equity_2019': parent_eq_values[0],
            'Parent_Equity_2020': parent_eq_values[1],
            'Parent_Equity_2021': parent_eq_values[2],
            'Parent_Equity_2022': parent_eq_values[3],
            'Parent_Equity_2023': parent_eq_values[4]
        })

# Print the header
header = ['Ticker'] + [f'Parent Eq {y}' for y in range(2019, 2024)]
print(f"{header[0]:<10} | {' | '.join([f'{h:<15}' for h in header[1:]])}")
print("-" * (10 + len(' | '.join([f'{h:<15}' for h in header[1:]]))))

# Print the data rows
for data_row in print_data:
    ticker = data_row['Ticker']
    values = [data_row[f'Parent_Equity_{y}'] for y in range(2019, 2024)]
    print(f"{ticker:<10} | {' | '.join([f'{val:<15.2f}' for val in values])}")
