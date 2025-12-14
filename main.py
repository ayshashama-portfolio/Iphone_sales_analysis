import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
from collections import Counter

Order_Details = pd.read_csv('Order_details(masked).csv')

#Data Preprocessing and Feature Engineering

Order_Details.columns = Order_Details.columns.str.strip()
Order_Details = Order_Details.drop_duplicates()
Order_Details['Product'] = Order_Details['Product'].str.replace('|', ',', regex=False)
Order_Details['Transaction Date'] = pd.to_datetime(
    Order_Details['Transaction Date'], errors='coerce'
)
Order_Details = Order_Details.dropna(subset=['Transaction Date'])
Order_Details['Transaction_ID'] = Order_Details.index

# Extract Time Features
Order_Details['Hour'] = Order_Details['Transaction Date'].dt.hour
Order_Details['Week'] = Order_Details['Transaction Date'].dt.isocalendar().week
Order_Details['Weekday'] = Order_Details['Transaction Date'].dt.day_name() # e.g., 'Monday'
Order_Details['Date'] = Order_Details['Transaction Date'].dt.date

# Split product column into clean lists
Order_Details['Product_List'] = (
    Order_Details['Product']
    .str.replace(';', ',')
    .str.split(',')
)
Order_Details['Product_List'] = Order_Details['Product_List'].apply(
    lambda x: [p.strip().lower() for p in x if p.strip()] # Clean, lowercase, and filter empty strings
)

df_items = Order_Details.copy()
df_items = df_items.explode('Product_List')
df_items['Product'] = df_items['Product_List']
df_items = df_items.drop(columns=['Product_List'])


#Data Visualization
# 1. Top 15 Sold Products (Uses df_items)
top_products = df_items['Product'].value_counts().head(15)
plt.figure(figsize=(10,5))
sns.barplot(x=top_products.values, y=top_products.index)
plt.title("Top 15 Sold Products")
plt.xlabel("Count")
plt.ylabel("Product")

# 2. Transactions per Hour (Uses Order_Details)
hourly = Order_Details['Hour'].value_counts().sort_index()
plt.figure(figsize=(10,5))
sns.lineplot(x=hourly.index, y=hourly.values, marker="o")
plt.title("Transactions per Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Transactions")
plt.grid(True)

# 3. Count of Transactions per Weekday 
weekly = Order_Details['Weekday'].value_counts()
full_day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
short_day_map = {
    'Monday': 'Mon', 'Tuesday': 'Tues', 'Wednesday': 'Wed', 'Thursday': 'Thurs',
    'Friday': 'Fri', 'Saturday': 'Sat', 'Sunday': 'Sun'
}
weekly = weekly.reindex(full_day_order)
weekly.index = weekly.index.map(short_day_map) 
plt.figure(figsize=(10,4))
sns.barplot(x=weekly.index, y=weekly.values)
plt.title("Count of Transactions per Weekday")
plt.xlabel("Weekday")
plt.ylabel("Transactions")

# 4. Top 10 Co-purchased Product Pairs
pair_counter = Counter()
for products in Order_Details['Product_List']:
    if len(set(products)) >= 2:
        unique_items = sorted(list(set(products)))
        for pair in combinations(unique_items, 2):
            pair_counter[pair] += 1
top_pairs = pair_counter.most_common(10)
pairs_df = pd.DataFrame(top_pairs, columns=['Pair', 'Count'])
plt.figure(figsize=(10,5))
sns.barplot(y=pairs_df['Pair'].astype(str), x=pairs_df['Count'])
plt.title("Top 10 Co-purchased Product Pairs")
plt.xlabel("Count")
plt.ylabel("Product Pair")
plt.tight_layout()

# 5. Heatmap: Items Sold by Weekday and Hour (Uses df_items)
pivot = df_items.pivot_table(
    index='Weekday',
    columns='Hour',
    values='Product',
    aggfunc='count'
).fillna(0)
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
pivot = pivot.reindex(weekday_order)
plt.figure(figsize=(12,5))
sns.heatmap(pivot, cmap="YlGnBu", linewidths=.5)
plt.title("Heatmap: Items Sold by Weekday and Hour")
plt.xlabel("Hour")
plt.ylabel("Weekday")
plt.tight_layout()

# 6. Distribution of Basket Size (Items per Transaction) (Uses df_items)
basket_sizes = df_items.groupby('Transaction_ID')['Product'].count()
plt.figure(figsize=(8,5))
sns.histplot(basket_sizes, bins=20, kde=True)
plt.title("Distribution of Basket Size")
plt.xlabel("Number of Items")
plt.ylabel("Frequency")
plt.tight_layout()

# 7. Top 15 Most Active Customers
top_customers = Order_Details['Name'].value_counts().head(15)
plt.figure(figsize=(10,5))
sns.barplot(x=top_customers.values, y=top_customers.index)
plt.title("Top 15 Most Active Customers")
plt.xlabel("Number of Transactions")
plt.ylabel("Customer Name")
plt.tight_layout()
plt.show()