import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Loading existing Excel data
df = pd.read_excel(r"C:\Users\priya\OneDrive\Desktop\python\forecasted_mismatch.py\Reference Salary Data.xlsx")
df.columns = df.columns.str.strip()

# Creating 'Mismatch' column if not present
if 'Mismatch' not in df.columns:
    df['Mismatch'] = df['ACTUAL TDS (30%)'] - df['TDS DEDUCTED']

# Adding Month_Num based on index
df['Month_Num'] = df.index + 1  

# Preparing training data for regression
X = df[['Month_Num']]
y = df['Mismatch']

# Adding the regression model
model = LinearRegression()
model.fit(X, y)

# Forecasting for next 12 months
future_months = pd.DataFrame({
    'Month_Num': np.arange(df['Month_Num'].max() + 1, df['Month_Num'].max() + 13)
})
future_months['Forecasted_Mismatch'] = model.predict(future_months[['Month_Num']])

# Appending future forecast to original DataFrame
future_months['Mismatch'] = np.nan  # No actual mismatch yet
df['Forecasted_Mismatch'] = df['Mismatch']  # Copy known mismatches
df_forecasted = pd.concat([df, future_months], ignore_index=True)

# Calculating total projected shortfall (only using Forecasted_Mismatch)
projected_shortfall = df_forecasted['Forecasted_Mismatch'].sum()

# Outputing result
print(f"Projected TDS Shortfall by year-end: ₹{projected_shortfall:,.2f}")

# Saving full forecasted DataFrame
df_forecasted.to_excel("Reference Salary Data - Forecasted.xlsx", index=False)

# Save shortfall only and converting to csv
pd.DataFrame({'Forecasted_Shortfall': [projected_shortfall]}).to_csv('shortfall_output.csv', index=False)