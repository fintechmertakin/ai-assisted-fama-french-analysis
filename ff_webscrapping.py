import requests
import zipfile
import io
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Download ZIP file
url = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_CSV.zip"
response = requests.get(url)

if response.status_code != 200:
    raise RuntimeError("Failed to download the ZIP file.")

# Step 2: Extract CSV from ZIP
with zipfile.ZipFile(io.BytesIO(response.content)) as z:
    csv_name = z.namelist()[0]  # Usually the first file is the data
    with z.open(csv_name) as f:
        df_raw = pd.read_csv(f, skiprows=3)

# Step 3: Clean the Data
# Drop rows after the "Annual Factors" section (look for row starting with " Annual")
df_raw = df_raw[~df_raw.iloc[:, 0].str.contains("Annual", na=False)]
df_raw.columns = ['Date', 'Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'RF']
df_raw = df_raw.dropna()
# Keep only rows with 6-digit dates (i.e., YYYYMM)
df_raw = df_raw[df_raw['Date'].str.len() == 6]

# Now convert safely
df_raw['Date'] = pd.to_datetime(df_raw['Date'], format='%Y%m')
for col in df_raw.columns[1:]:
    df_raw[col] = pd.to_numeric(df_raw[col], errors='coerce')

# Step 4: Analysis

## 1. Summarize Time Trends (Annual Averages)
df_raw.set_index('Date', inplace=True)
annual_trends = df_raw.resample('Y').mean()
print("\nAnnual Time Trends (Mean of each factor):")
print(annual_trends)

## 2. Visualizations
for factor in ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']:
    plt.figure(figsize=(10, 4))
    plt.plot(df_raw.index, df_raw[factor])
    plt.title(f"{factor} Over Time")
    plt.xlabel("Date")
    plt.ylabel("Monthly Return (%)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

## 3. Descriptive Statistics
desc_stats = df_raw[['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']].describe(percentiles=[.01, .5, .99])
print("\nDescriptive Statistics:")
print(desc_stats.loc[['mean', 'std', '50%', 'min', 'max', '1%', '99%']])

## 4. Correlation Matrix
corr_matrix = df_raw[['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']].corr()
print("\nCorrelation Matrix:")
print(corr_matrix)

# Optional: Visual correlation heatmap
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Matrix of Fama-French 5 Factors")
plt.tight_layout()
plt.show()
