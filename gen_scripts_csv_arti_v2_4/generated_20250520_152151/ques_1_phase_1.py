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

# Define target sectors - using the sectors identified in the previous step
# Assuming these are the sectors for which top companies are required
target_sectors = ['Banks', 'Real Estate', 'Food & Beverage']

# Define the relevant columns including newline characters as they appear
ticker_col = 'Ticker\n'
sector_col = 'Sector L2\n'

net_profit_cols = [
    '18. Net profit/(loss) after tax\nYear: 2019\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2020\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2021\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2022\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2023\nUnit: Billions VND\n'
]

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

# --- Step 1: Calculate Total Net Profit for Ranking ---
# Calculate total net profit for each company across the years 2019-2023
df['Total Net Profit 2019-2023'] = df[net_profit_cols].sum(axis=1)
total_net_profit_col = 'Total Net Profit 2019-2023' # Store column name for easy access

# --- Step 2: Find Top 3 Companies per Sector by Net Profit ---
# Filter the DataFrame to include only rows from the target sectors for ranking
# Use .str.strip() for comparison against clean sector names
filtered_df_for_ranking = df[df[sector_col].str.strip().isin(target_sectors)].copy()

# Find top 3 companies per sector based on the calculated total net profit
# Use group_keys=False to avoid adding the sector index level unnecessarily
top_companies_by_profit = filtered_df_for_ranking.groupby(sector_col, group_keys=False).apply(lambda x: x.nlargest(3, total_net_profit_col))

# Get the list of tickers for these top companies
top_tickers_list = top_companies_by_profit[ticker_col].tolist()

# --- Step 3: Calculate Parent Equity for 2019-2023 ---
# Calculate Parent Equity = Owner Equity - Minority Interests for each year
parent_equity_yearly_cols = []
years = range(2019, 2024)
for i, year in enumerate(years):
    # Define new column name for Parent Equity, including the year
    current_parent_equity_col_name = f'Parent Equity\nYear: {year}\nUnit: Billions VND\n'
    # Calculate Parent Equity for the current year and add it as a new column to the original df
    df[current_parent_equity_col_name] = df[owner_equity_cols[i]] - df[minority_interests_cols[i]]
    # Store the name of the newly created column
    parent_equity_yearly_cols.append(current_parent_equity_col_name)

# --- Step 4: Filter for Top Tickers and Select Output Columns ---
# Filter the original df (which now contains Parent Equity columns) to include only the top tickers
# Use .copy() to avoid potential SettingWithCopyWarning
final_output_df = df[df[ticker_col].isin(top_tickers_list)].copy()

# Select the Ticker column and the calculated Parent Equity columns for printing
output_columns = [ticker_col] + parent_equity_yearly_cols
final_output_df = final_output_df[output_columns]

# --- Step 5: Print the Results ---
# Iterate through rows of the final DataFrame containing the top companies
for index, row in final_output_df.iterrows():
    # Print the Ticker for the current company, stripping any whitespace
    print(f"Ticker: {row[ticker_col].strip()}")
    # Iterate through the list of calculated Parent Equity column names for each year
    for col_name in parent_equity_yearly_cols:
        # Extract the year from the column name string for printing
        # Assumes column name structure is 'Parent Equity\nYear: YYYY\nUnit: Billions VND\n'
        year_str = col_name.split('Year: ')[1].split('\n')[0]
        # Print the Parent Equity for the specific year, formatted to two decimal places
        print(f"Parent Equity {year_str}: {row[col_name]:.2f}")
