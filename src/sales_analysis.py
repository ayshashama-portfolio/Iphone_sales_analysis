"""
iPhone Store Sales Transaction Analysis
---------------------------------------
Cleans one week of masked order logs (1-7 March 2021) and answers:
  1. Which products sell most, and which are bought together?
  2. When do customers order (day and hour)?
  3. How big are baskets, and how many customers come back?

Run from the repository root:
    python src/sales_analysis.py
Outputs: data/processed/order_items_clean.csv and charts in screenshots/.
"""

from collections import Counter
from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "order_details_masked.csv"
PROCESSED = ROOT / "data" / "processed" / "order_items_clean.csv"
OUT = ROOT / "screenshots"
OUT.mkdir(exist_ok=True)
PROCESSED.parent.mkdir(parents=True, exist_ok=True)

# ---------- chart style ----------
BLUE, ORANGE, GREY = "#2a78d6", "#eb6834", "#c9c8c3"
INK, MUTED = "#0b0b0b", "#52514e"
plt.rcParams.update({
    "figure.dpi": 150, "savefig.bbox": "tight", "font.size": 10,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": GREY, "axes.labelcolor": MUTED, "xtick.color": MUTED,
    "ytick.color": MUTED, "axes.titleweight": "bold", "axes.titlesize": 12,
    "axes.titlecolor": INK, "axes.grid": True, "grid.color": "#ecebe8",
    "axes.axisbelow": True,
})


def highlight(values, top_n=1):
    order = np.argsort(values)[::-1][:top_n]
    return [BLUE if i in order else GREY for i in range(len(values))]


def save(fig, name):
    fig.savefig(OUT / name)
    plt.close(fig)
    print(f"saved screenshots/{name}")


# ---------- 1. load ----------
orders = pd.read_csv(RAW, encoding="utf-8-sig")
print(f"Raw orders: {len(orders)}")

# ---------- 2. clean ----------
orders.columns = orders.columns.str.strip()
orders = orders.drop_duplicates()
# Dates are day-first (01/03/2021 = 1 March 2021). Parsing them month-first would
# spread one week of orders across seven months and give wrong weekday results.
orders["Transaction Date"] = pd.to_datetime(
    orders["Transaction Date"], format="%d/%m/%Y %H:%M:%S", errors="coerce"
)
orders = orders.dropna(subset=["Transaction Date"]).reset_index(drop=True)
orders["Transaction_ID"] = orders.index + 1
orders["Customer_Domain"] = orders["Email"].str.split("@").str[1].str.lower()

# Product lists use ',', '|' or ';' as separators - standardise and split.
orders["Product_List"] = (
    orders["Product"].str.replace("|", ",", regex=False).str.replace(";", ",", regex=False)
    .str.split(",")
    .apply(lambda items: [p.strip().upper() for p in items if p.strip()])
)
orders["Basket_Size"] = orders["Product_List"].str.len()

# Time features
orders["Date"] = orders["Transaction Date"].dt.date
orders["Hour"] = orders["Transaction Date"].dt.hour
orders["Weekday"] = orders["Transaction Date"].dt.day_name()

# One row per item: the structure needed for product counts and basket analysis.
items = orders.explode("Product_List").rename(columns={"Product_List": "Item"})
items[["Transaction_ID", "Name", "Item", "Transaction Date", "Date", "Hour", "Weekday",
       "Basket_Size"]].to_csv(PROCESSED, index=False)
print(f"Clean orders: {len(orders)}, item rows: {len(items)} -> {PROCESSED.relative_to(ROOT)}")

# ---------- 3. charts ----------
# 3.1 Top 15 products
top = items["Item"].value_counts().head(15).sort_values()
fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(top.index, top.values, color=highlight(top.values, 3))
ax.set_title("Three products lead sales by a clear margin")
ax.set_xlabel("Units sold")
ax.grid(axis="y", visible=False)
for y, v in enumerate(top.values):
    ax.text(v + 1, y, str(v), va="center", color=MUTED, fontsize=8)
save(fig, "top_15_products.png")

# 3.2 Orders per hour
hourly = orders["Hour"].value_counts().reindex(range(24), fill_value=0)
fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(hourly.index, hourly.values, color=BLUE, lw=2, marker="o", ms=5)
ax.set_xticks(range(0, 24, 2))
ax.set_title("Orders peak at midday and again late at night")
ax.set_xlabel("Hour of day")
ax.set_ylabel("Orders")
save(fig, "orders_per_hour.png")

# 3.3 Orders per day
daily = orders.groupby("Date").size()
labels = [pd.Timestamp(d).strftime("%a\n%d Mar") for d in daily.index]
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(labels, daily.values, color=highlight(daily.values))
ax.set_title("Sunday 7 March was the busiest day of the week")
ax.set_ylabel("Orders")
ax.grid(axis="x", visible=False)
for x, v in enumerate(daily.values):
    ax.text(x, v + 2, str(v), ha="center", color=MUTED, fontsize=9)
save(fig, "orders_per_day.png")

# 3.4 Top 10 co-purchased pairs
pairs = Counter()
for basket in orders["Product_List"]:
    for pair in combinations(sorted(set(basket)), 2):
        pairs[pair] += 1
top_pairs = pd.DataFrame(pairs.most_common(10), columns=["Pair", "Count"])
top_pairs["Pair"] = top_pairs["Pair"].apply(lambda p: f"{p[0]} + {p[1]}")
top_pairs = top_pairs.iloc[::-1]
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(top_pairs["Pair"], top_pairs["Count"], color=highlight(top_pairs["Count"].values))
ax.set_title("Products most often bought together")
ax.set_xlabel("Orders containing both products")
ax.grid(axis="y", visible=False)
save(fig, "top_10_product_pairs.png")

# 3.5 Heatmap: items sold by day and hour
pivot = items.pivot_table(index="Date", columns="Hour", values="Item", aggfunc="count")
pivot = pivot.reindex(columns=range(24)).fillna(0)
pivot.index = [pd.Timestamp(d).strftime("%a %d Mar") for d in pivot.index]
fig, ax = plt.subplots(figsize=(12, 4))
sns.heatmap(pivot, cmap="Blues", linewidths=0.5, linecolor="white", ax=ax,
            cbar_kws={"label": "Items sold"})
ax.set_title("Items sold by day and hour")
ax.set_xlabel("Hour of day")
ax.set_ylabel("")
save(fig, "items_by_day_and_hour.png")

# 3.6 Basket size distribution (orders of 8+ products grouped as bulk orders)
bucket = orders["Basket_Size"].clip(upper=8).map(lambda n: "8+" if n == 8 else str(n))
order_labels = [str(n) for n in range(1, 8)] + ["8+"]
sizes = bucket.value_counts().reindex(order_labels, fill_value=0)
fig, ax = plt.subplots(figsize=(7, 4))
colors = [ORANGE if lab == "8+" else BLUE if lab == "1" else GREY for lab in order_labels]
ax.bar(order_labels, sizes.values, color=colors)
ax.set_title("Most orders hold one product; a few bulk orders hold many")
ax.set_xlabel("Products per order")
ax.set_ylabel("Orders")
ax.grid(axis="x", visible=False)
for x, v in enumerate(sizes.values):
    ax.text(x, v + 4, str(v), ha="center", color=MUTED, fontsize=9)
save(fig, "basket_size_distribution.png")

# 3.7 New vs repeat customers
per_customer = orders["Name"].value_counts()
dist = per_customer.value_counts().sort_index()
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(dist.index.astype(str), dist.values, color=highlight(dist.values))
ax.set_title("Most customers ordered only once this week")
ax.set_xlabel("Orders per customer")
ax.set_ylabel("Customers")
ax.grid(axis="x", visible=False)
for x, v in enumerate(dist.values):
    ax.text(x, v + 5, str(v), ha="center", color=MUTED, fontsize=9)
save(fig, "orders_per_customer.png")

# ---------- 4. summary numbers used in the README ----------
units = items["Item"].value_counts()
print("\n--- Summary ---")
print(f"Orders: {len(orders)}, items: {len(items)}, products: {units.size}, customers: {per_customer.size}")
print(f"Top 3 products: {units.head(3).to_dict()}, share of units: {units.head(3).sum() / len(items):.1%}")
print(f"Avg basket: {orders['Basket_Size'].mean():.2f}, single-product orders: {(orders['Basket_Size'] == 1).mean():.1%}")
print(f"Orders with 2+ products: {(orders['Basket_Size'] >= 2).sum()}")
bulk = orders[orders["Basket_Size"] >= 8]
print(f"Bulk orders (8+): {len(bulk)} ({len(bulk) / len(orders):.1%} of orders), "
      f"{bulk['Basket_Size'].sum() / len(items):.1%} of items, largest {bulk['Basket_Size'].max()}")
print(f"Repeat customers: {(per_customer > 1).mean():.1%}, top customer: {per_customer.idxmax()} ({per_customer.max()} orders)")
print(f"Orders per day: {dict(zip(labels, daily.values))}")
print(f"Busiest hours: {hourly.sort_values(ascending=False).head(4).to_dict()}")
print(f"Orders 11:00-12:59: {hourly[11:13].sum() / len(orders):.1%}, 21:00-23:59: {hourly[21:24].sum() / len(orders):.1%}, 00:00-07:59: {hourly[0:8].sum() / len(orders):.1%}")
print(f"Top pairs: {pairs.most_common(3)}")
print(f"Gmail share: {(orders['Customer_Domain'] == 'gmail.com').mean():.1%}")
