## Iphone_sales_analysis 
### Project Overview
This project presents a detailed exploratory analysis of transactional sales data using Python. The goal is to understand product performance, customer activity, and time-based purchasing patterns through structured data preprocessing and meaningful visualizations. The analysis focuses on transforming raw transaction records into actionable insights that can support business and retail decision-making. [SourceCode](https://github.com/ayshashama-portfolio/Iphone_sales_analysis/blob/main/main.py) 

### Data Sources
The dataset used in this project is a masked transactional CSV file containing sales records.It includes details such as transaction timestamps, customer names, emails and purchased products with 582 entries. Sensitive information has been anonymized while retaining the structure required for realistic analysis. 
* **Initial Data File:** [Source](https://github.com/ayshashama-portfolio/Iphone_sales_analysis/blob/main/initial_Order_details(masked).csv)
* **Processed Data File:** [Source](https://github.com/ayshashama-portfolio/Iphone_sales_analysis/blob/main/after_Order_details(masked).csv)

**Changes in the Processed Data File:**
The final, processed data file (`after_Order_details(masked).csv`) reflects the transformations applied in the preprocessing phase, which were critical for analysis reliability:
* **Noise Elimination (Temporal Data):** The removal of records where date conversion failed ensures all remaining transactions have a valid time stamp, eliminating **temporal noise** and guaranteeing the reliability of all hour, day, and week-based analyses.
* **Data Integrity (Duplicates):** The elimination of duplicate entries prevents statistical skew, ensuring that metrics like total sales counts and product frequency are not improperly inflated by redundant records.
* **Product Parsing Consistency:** Standardization of the product separator (e.g., replacing `|` with `,`) guarantees that products are consistently split and counted, which is fundamental for accurate Market Basket Analysis calculations.
* **Structural Readiness:** The underlying dataset structure is prepared for advanced analysis by converting the raw time string into a native datetime object, making all subsequent feature engineering (like extracting `Hour` or `Weekday`) robust and error-free.
### Tools Used
* Python – Core programming language
* Visual Studio Code – Development environment
* Pandas – Data cleaning, transformation, and aggregation
* NumPy – Supporting numerical operations
* Matplotlib & Seaborn – Data visualization
* Windows PowerShell – For running scripts and environment management
* CSV File – Source data format

### Data Preprocessing & Feature Engineering
The following steps were performed to prepare the raw transaction logs for analysis:
1. **Data Quality Enforcement:** Removed exact duplicate transaction entries and dropped records where the `Transaction Date` was invalid (missing or unconvertible).
2. **Field Standardization:** Cleaned column headers by stripping whitespace and harmonized product delimiters by replacing pipe characters `|` with commas `,` for uniform parsing.
3. **Temporal Feature Creation:** Converted the raw `Transaction Date` to a datetime object, then generated analytical features like Hour, Weekday Name, and ISO Week Number.
4. **Product Normalization:** Standardized the product list by converting all names to lowercase and stripping internal whitespace.
5. **Structural Transformation:** Unnested the dataset, converting the format from one row per transaction to one row per item, which is the foundational structure required for Market Basket Analysis.

### Exploratory Data Analysis
The analysis explores the following aspects of the data:
* Which products are sold most frequently?
* How transaction volume varies across different hours of the day?
* Differences in transaction counts across weekdays
* Commonly co-purchased product combinations
* Sales intensity by weekday and hour using a heatmap
* Distribution of basket sizes (items per transaction)
* Identification of the most active customers

### Data Analysis
Some interesting features worked during this project are:
* Temporal Segmentation: Analyzed sales frequency across different hours and days of the week to understand peak times.
* Product Performance Metrics: Calculated the frequency count for every individual product to identify top sellers.
* Market Basket Analysis: Used the Apriori algorithm foundation (by generating combinations) to find the Top 10 co-purchased product pairs.
* Basket Size Distribution: Calculated the number of items per transaction to visualize customer purchasing habits.
* Weekly/Hourly Sales Heatmap: Visualized the intensity of item sales across a Weekday vs. Hour grid to pinpoint critical operational windows.

### Results
The Analysis results are summarized as follows:
1. `Product_75` is the single most frequently purchased product. [See visualization](https://github.com/ayshashama-portfolio/Iphone_sales_analysis/blob/main/Visualizations/Top_15_Sold_Products.png)
2. Sales activity consistently peaks during `11am to 12pm` across most days. [See visualization](https://github.com/ayshashama-portfolio/Iphone_sales_analysis/blob/main/Visualizations/Transactions%20per%20Hour.png)
3. `Saturday` and `Wednesday` show the highest total number of transactions. [See visualization](https://github.com/ayshashama-portfolio/Iphone_sales_analysis/blob/main/Visualizations/Count%20of%20Transactions%20per%20Weekday.png)
4. The strongest co-purchase relationship exists between `Product_27` and `Product_63`, indicating a high potential for cross-selling. [See visualization](https://github.com/ayshashama-portfolio/Iphone_sales_analysis/blob/main/Visualizations/Top%2010%20Co-purchased%20Product%20Pairs.png)
5. Most customers engage in small transactions, with the majority of baskets containing `1 to 4` items. [See visualization](https://github.com/ayshashama-portfolio/Iphone_sales_analysis/blob/main/Visualizations/Distribution%20of%20Basket%20Size.png)
6. The highest combined volume of items sold occurs on Saturday between `22nd & 23rd Hour`. [See visualization](https://github.com/ayshashama-portfolio/Iphone_sales_analysis/blob/main/Visualizations/Items%20Sold%20by%20Weekday%20and%20Hour.png)
7. The customer `Person_470` is the most active shopper, accounting for 5 transactions, demonstrating a clear leader in purchase frequency. [See visualization](https://github.com/ayshashama-portfolio/Iphone_sales_analysis/blob/main/Visualizations/Top%2015%20Most%20Active%20Customers.png)

### Recommendations
Based on the findings from this analysis:
1. High-selling products should be prioritized for inventory planning.
2. Peak transaction hours can be targeted for staffing and promotions.
3. Frequently co-purchased products can be bundled to increase sales.
4. Active customers may be suitable candidates for loyalty programs.
5. Basket size patterns can guide upselling and cross-selling strategies.
   
