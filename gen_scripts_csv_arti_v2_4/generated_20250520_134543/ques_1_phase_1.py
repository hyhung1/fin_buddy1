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

# Define necessary column names, handling potential whitespace/newlines
sector_col = "Sector L2\n"
company_col = "Company Name\n"

net_profit_cols_yearly = [
    "18. Net profit/(loss) after tax\nYear: 2019\nUnit: Billions VND\n",
    "18. Net profit/(loss) after tax\nYear: 2020\nUnit: Billions VND\n",
    "18. Net profit/(loss) after tax\nYear: 2021\nUnit: Billions VND\n",
    "18. Net profit/(loss) after tax\nYear: 2022\nUnit: Billions VND\n",
    "18. Net profit/(loss) after tax\nYear: 2023\nUnit: Billions VND\n",
]

owner_equity_cols_yearly = [
    "II. OWNER'S EQUITY\nYear: 2019\nUnit: Billions VND\n",
    "II. OWNER'S EQUITY\nYear: 2020\nUnit: Billions VND\n",
    "II. OWNER'S EQUITY\nYear: 2021\nUnit: Billions VND\n",
    "II. OWNER'S EQUITY\nYear: 2022\nUnit: Billions VND\n",
    "II. OWNER'S EQUITY\nYear: 2023\nUnit: Billions VND\n",
]

minority_interests_cols_yearly = [
    "1.13. Minority interests\nYear: 2019\nUnit: Billions VND\n",
    "1.13. Minority interests\nYear: 2020\nUnit: Billions VND\n",
    "1.13. Minority interests\nYear: 2021\nUnit: Billions VND\n",
    "1.13. Minority interests\nYear: 2022\nUnit: Billions VND\n",
    "1.13. Minority interests\nYear: 2023\nUnit: Billions VND\n",
]

# Create a copy to avoid modifying the original DataFrame while adding calculated columns
df_analysis = df.copy()

# Calculate Parent Equity for each year and store the new column names
parent_equity_cols_yearly = []
years = [2019, 2020, 2021, 2022, 2023]
for i, year in enumerate(years):
    parent_equity_col_name = f"Parent Equity {year}"
    df_analysis[parent_equity_col_name] = df_analysis[owner_equity_cols_yearly[i]] - df_analysis[minority_interests_cols_yearly[i]]
    parent_equity_cols_yearly.append(parent_equity_col_name)

# Calculate total net profit across the years for ranking
df_analysis['Total Net Profit (2019-2023)'] = df_analysis[net_profit_cols_yearly].sum(axis=1)

# Select only the necessary columns for the final output plus the ranking column
output_cols = [sector_col, company_col, 'Total Net Profit (2019-2023)'] + net_profit_cols_yearly + parent_equity_cols_yearly
df_subset = df_analysis[output_cols]

# Get the top 3 companies in each sector based on total net profit
# Use group_keys=False to prevent the grouping column from becoming part of the index
top_companies_per_sector = df_subset.groupby(sector_col, group_keys=False).apply(
    lambda x: x.nlargest(3, 'Total Net Profit (2019-2023)')
)

# Print the results
for index, row in top_companies_per_sector.iterrows():
    print(f"Sector: {row[sector_col]}")
    print(f"Company: {row[company_col]}")

    # Print Net Profit for each year
    net_profit_output = "Net Profit:"
    for i, year in enumerate(years):
        net_profit_output += f" {year}: {row[net_profit_cols_yearly[i]]:.2f}"
    print(net_profit_output)

    # Print Parent Equity for each year
    parent_equity_output = "Parent Equity:"
    for i, year in enumerate(years):
         parent_equity_output += f" {year}: {row[parent_equity_cols_yearly[i]]:.2f}"
    print(parent_equity_output)

    print("-" * 20) # Separator for readability
