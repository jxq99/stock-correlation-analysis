import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

API_KEY = 'YOUR_KEY'  # Your Alpha Vantage API key
symbols = ['BABA', 'BIDU', 'AMZN', 'GOOGL']
dfs = []

for symbol in symbols:
    print(f"Fetching data for {symbol}...")
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json().get('Time Series (Daily)', {})
    if not data:
        print(f"Error fetching data for {symbol}. Response: {r.json()}")
        continue
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df[['4. close']].rename(columns={'4. close': symbol})
    df.index = pd.to_datetime(df.index)
    dfs.append(df)

if not dfs:
    print("No data was fetched for any symbol. Please check your API key or endpoint access.")
    exit()

# Merge all dataframes on the date index
df_merged = pd.concat(dfs, axis=1, join='inner')
df_merged = df_merged.sort_index()
df_merged = df_merged[df_merged.index >= pd.to_datetime('2024-01-01')]
df_merged = df_merged.apply(pd.to_numeric)

# Calculate correlation
correlation_matrix = df_merged.corr()
print("\nCorrelation Matrix:")
print(correlation_matrix)

# Visualize correlation matrix as a heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, linewidths=0.5)
plt.title('Stock Price Correlation Heatmap (2024-)')
plt.tight_layout()
plt.show() 
