import pandas as pd
import numpy as np
# local retail orders dataset
df = pd.read_csv("retail-orders-raw.csv")

print("dataset loaded successfully!")

print("\nNum,ber of rows:",df.shape[0])
print("\nNumber of columns:",df.shape[1])

print("\ncolumn names:")
print(df.columns.tolist())

print("\nfirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

# ---------------------------------------
# DATA QUALITY CHECKS
# ---------------------------------------

# 1. Check duplicate Order IDs
print("\nDuplicate Order IDs:")

order_id_counts = df["order_id"].value_counts()

duplicate_order_ids = order_id_counts[order_id_counts > 1]

print(duplicate_order_ids)


# 2. Convert quantity to numeric
df["quantity_numeric"] = pd.to_numeric(
    df["quantity"],
    errors="coerce"
)

print("\nInvalid Quantity:")

invalid_quantity = df[
    (df["quantity_numeric"].isna()) |
    (df["quantity_numeric"] <= 0)
]

print(invalid_quantity[
    ["order_id", "quantity"]
])


# 3. Check invalid discount
print("\nInvalid Discount:")

invalid_discount = df[
    (df["discount_pct"].isna()) |
    (df["discount_pct"] < 0) |
    (df["discount_pct"] > 100)
]

print(invalid_discount[
    ["order_id", "discount_pct"]
])


# 4. Check invalid dates
print("\nInvalid or Missing Dates:")

df["order_date_clean"] = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)

invalid_dates = df[
    df["order_date_clean"].isna()
]

print(invalid_dates[
    ["order_id", "order_date"]
])


# 5. Check customer segment consistency
print("\nCustomer Segments:")

print(df["customer_segment"].value_counts())


# 6. Check payment status consistency
print("\nPayment Status:")

print(df["payment_status"].value_counts())


print("\nDATA QUALITY CHECK COMPLETED")

# ==========================================
# STEP 2 - DATA CLEANING
# ==========================================

# Create a copy of the raw dataset
clean_df = df.copy()


# 1. Remove exact duplicate rows
clean_df = clean_df.drop_duplicates()

print("After removing duplicate rows:", len(clean_df))


# 2. Clean Customer Segment
clean_df["customer_segment"] = (
    clean_df["customer_segment"]
    .str.strip()
    .str.title()
)


# 3. Clean Payment Status
clean_df["payment_status"] = (
    clean_df["payment_status"]
    .str.strip()
    .str.title()
)


# 4. Convert Quantity to numeric
clean_df["quantity"] = pd.to_numeric(
    clean_df["quantity"],
    errors="coerce"
)


# 5. Invalid quantity -> missing value
clean_df.loc[
    clean_df["quantity"] <= 0,
    "quantity"
] = np.nan


# 6. Convert Discount to numeric
clean_df["discount_pct"] = pd.to_numeric(
    clean_df["discount_pct"],
    errors="coerce"
)


# 7. Invalid discount -> missing value
clean_df.loc[
    (clean_df["discount_pct"] < 0) |
    (clean_df["discount_pct"] > 100),
    "discount_pct"
] = np.nan


# 8. Convert order date
clean_df["order_date"] = pd.to_datetime(
    clean_df["order_date"],
    errors="coerce"

)


# 9. Remove temporary columns created during profiling
columns_to_remove = [
    "quantity_numeric",
    "order_date_clean"
]

for column in columns_to_remove:
    if column in clean_df.columns:
        clean_df.drop(columns=column, inplace=True)


# ==========================================
# CLEANING SUMMARY
# ==========================================

print("\n========== CLEANING SUMMARY ==========")

print("\nMissing values after cleaning:")
print(clean_df.isnull().sum())

print("\nCustomer segments after cleaning:")
print(clean_df["customer_segment"].value_counts())

print("\nPayment status after cleaning:")
print(clean_df["payment_status"].value_counts())

print("\nCleaned dataset:")
print(clean_df)


print("\nCLEANING COMPLETED")
# ==========================================
# STEP 2B - DATE CLEANING
# ==========================================

# Convert dates using a fixed expected format
clean_df["order_date"] = pd.to_datetime(
    clean_df["order_date"],
    format="%Y-%m-%d",
    errors="coerce"
)

print("\nDate values after cleaning:")
print(clean_df[["order_id", "order_date"]])


# Count missing dates
missing_dates = clean_df["order_date"].isna().sum()

print("\nMissing dates:", missing_dates)


# ==========================================
# SAVE CLEAN DATASET
# ==========================================

clean_df.to_csv(
    "retail-orders-cleaned.csv",
    index=False
)

print("\nCleaned dataset saved as: retail-orders-cleaned.csv")

# ==========================================
# STEP 3 - KPI CALCULATION
# ==========================================

print("\n========== KPI CALCULATION ==========")


# Make sure numeric columns are numeric
clean_df["unit_price"] = pd.to_numeric(
    clean_df["unit_price"],
    errors="coerce"
)

clean_df["quantity"] = pd.to_numeric(
    clean_df["quantity"],
    errors="coerce"
)

clean_df["discount_pct"] = pd.to_numeric(
    clean_df["discount_pct"],
    errors="coerce"
)


# Calculate Sales for each order
clean_df["sales"] = (
    clean_df["quantity"]
    * clean_df["unit_price"]
    * (1 - clean_df["discount_pct"].fillna(0) / 100)
)


# KPI 1: Total Orders
total_orders = clean_df["order_id"].nunique()


# KPI 2: Total Quantity
total_quantity = clean_df["quantity"].sum()


# KPI 3: Total Sales
total_sales = clean_df["sales"].sum()


# KPI 4: Average Order Value
average_order_value = total_sales / total_orders


# KPI 5: Average Unit Price
average_unit_price = clean_df["unit_price"].mean()


# KPI 6: Average Discount
average_discount = clean_df["discount_pct"].mean()


# KPI 7: Paid Orders
paid_orders = (
    clean_df["payment_status"]
    .eq("Paid")
    .sum()
)


# KPI 8: Pending Orders
pending_orders = (
    clean_df["payment_status"]
    .eq("Pending")
    .sum()
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("\n1. Total Orders:", total_orders)

print("2. Total Quantity:", total_quantity)

print("3. Total Sales:", round(total_sales, 2))

print("4. Average Order Value:", round(average_order_value, 2))

print("5. Average Unit Price:", round(average_unit_price, 2))

print("6. Average Discount:", round(average_discount, 2), "%")

print("7. Paid Orders:", paid_orders)

print("8. Pending Orders:", pending_orders)


print("\nKPI CALCULATION COMPLETED")

# ==========================================
# STEP 4 - KPI DICTIONARY
# ==========================================

kpi_dictionary = pd.DataFrame({
    "KPI Name": [
        "Total Orders",
        "Total Quantity",
        "Total Sales",
        "Average Order Value",
        "Average Unit Price",
        "Average Discount",
        "Paid Orders",
        "Pending Orders"
    ],

    "Formula": [
        "Count of unique order_id",
        "Sum of quantity",
        "quantity × unit_price × (1 - discount_pct/100)",
        "Total Sales ÷ Total Orders",
        "Average of unit_price",
        "Average of discount_pct",
        "Count of orders where payment_status = Paid",
        "Count of orders where payment_status = Pending"
    ],

    "Business Meaning": [
        "Shows the total number of unique orders",
        "Shows the total number of products/services ordered",
        "Shows the total revenue generated after discount",
        "Shows the average revenue generated per order",
        "Shows the average selling price",
        "Shows the average discount given to customers",
        "Shows how many orders have been paid",
        "Shows how many orders are still pending"
    ],

    "Data Source": [
        "order_id",
        "quantity",
        "quantity, unit_price, discount_pct",
        "Total Sales and Total Orders",
        "unit_price",
        "discount_pct",
        "payment_status",
        "payment_status"
    ]
})

print("\n========== KPI DICTIONARY ==========")
print(kpi_dictionary)

kpi_dictionary.to_csv(
    "KPI_Dictionary.csv",
    index=False
)

print("\nKPI Dictionary saved as: KPI_Dictionary.csv")
print("\nSTEP 4 COMPLETED")

# ==========================================
# STEP 5 - FINAL DATA QUALITY VALIDATION
# ==========================================

print("\n========== FINAL DATA QUALITY VALIDATION ==========")

# 1. Duplicate Order IDs
duplicate_orders = clean_df["order_id"].duplicated().sum()

# 2. Missing Order IDs
missing_order_ids = clean_df["order_id"].isna().sum()

# 3. Invalid Quantity
invalid_quantity = (
    clean_df["quantity"].notna() &
    (clean_df["quantity"] <= 0)
).sum()

# 4. Missing Quantity
missing_quantity = clean_df["quantity"].isna().sum()

# 5. Invalid Discount
invalid_discount = (
    clean_df["discount_pct"].notna() &
    (
        (clean_df["discount_pct"] < 0) |
        (clean_df["discount_pct"] > 100)
    )
).sum()

# 6. Missing City
missing_city = clean_df["city"].isna().sum()

# 7. Missing Order Date
missing_dates = clean_df["order_date"].isna().sum()

# 8. Invalid Payment Status
valid_status = ["Paid", "Pending", "Failed", "Refunded"]

invalid_payment_status = (
    ~clean_df["payment_status"].isin(valid_status)
).sum()

print("\nDuplicate Order IDs:", duplicate_orders)
print("Missing Order IDs:", missing_order_ids)
print("Invalid Quantity:", invalid_quantity)
print("Missing Quantity:", missing_quantity)
print("Invalid Discount:", invalid_discount)
print("Missing City:", missing_city)
print("Missing Order Date:", missing_dates)
print("Invalid Payment Status:", invalid_payment_status)

# Overall result
total_issues = (
    duplicate_orders
    + missing_order_ids
    + invalid_quantity
    + invalid_discount
    + missing_city
    + missing_dates
    + invalid_payment_status
)

print("\n--------------------------------")
print("Total Quality Issues:", total_issues)

if total_issues == 0:
    print("DATA QUALITY STATUS: PASSED")
else:
    print("DATA QUALITY STATUS: REVIEW REQUIRED")

print("--------------------------------")
print("\nSTEP 5 COMPLETED")


# ==========================================
# STEP 6 - BUSINESS ANALYSIS
# ==========================================

print("\n========== BUSINESS ANALYSIS ==========")

# Sales by Category
category_sales = (
    clean_df.groupby("category")["sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\nSales by Category:")
print(category_sales)

# Sales by Customer Segment
segment_sales = (
    clean_df.groupby("customer_segment")["sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\nSales by Customer Segment:")
print(segment_sales)

# Sales by City
city_sales = (
    clean_df.groupby("city")["sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\nSales by City:")
print(city_sales)

# Payment Status Summary
payment_summary = (
    clean_df["payment_status"]
    .value_counts()
)

print("\nPayment Status Summary:")
print(payment_summary)

# Top Category
top_category = category_sales.idxmax()

# Top Customer Segment
top_segment = segment_sales.idxmax()

# Top City
top_city = city_sales.idxmax()

print("\n========== KEY BUSINESS INSIGHTS ==========")

print("Top Category:", top_category)
print("Top Customer Segment:", top_segment)
print("Top City:", top_city)

print("\nBUSINESS ANALYSIS COMPLETED")


# ==========================================
# STEP 7 - BUSINESS RECOMMENDATIONS
# ==========================================

print("\n========== BUSINESS RECOMMENDATIONS ==========")

print("\n1. Focus on Course Access")
print(
    "Course Access is the top-performing category by sales. "
    "The business should continue promoting this category "
    "and explore ways to increase its sales further."
)

print("\n2. Target Professional Customers")
print(
    "Professionals generate the highest sales among customer segments. "
    "The business can create targeted offers and marketing campaigns "
    "for Professional customers."
)

print("\n3. Strengthen Chennai Market")
print(
    "Chennai is the highest-sales city in the dataset. "
    "The business should maintain its presence in Chennai "
    "and investigate opportunities to expand in other cities."
)

print("\n4. Monitor Pending Payments")
print(
    "Pending payments should be monitored regularly. "
    "The business can follow up with customers to improve "
    "successful payment completion."
)

print("\n5. Improve Data Quality")
print(
    "The dataset contains issues such as missing values, "
    "invalid quantities, inconsistent dates and duplicate orders. "
    "Regular data validation should be implemented."
)

print("\nBUSINESS RECOMMENDATIONS COMPLETED")
# ==========================================
# STEP 8 - FINAL KPI DICTIONARY
# ==========================================

kpi_dictionary_final = pd.DataFrame({
    "KPI Name": [
        "Total Orders",
        "Total Quantity",
        "Total Sales",
        "Average Order Value",
        "Average Unit Price",
        "Average Discount",
        "Paid Orders",
        "Pending Orders"
    ],

    "Formula": [
        "COUNT(DISTINCT order_id)",
        "SUM(quantity)",
        "quantity × unit_price × (1 - discount_pct / 100)",
        "Total Sales / Total Orders",
        "AVG(unit_price)",
        "AVG(discount_pct)",
        "COUNT(payment_status = Paid)",
        "COUNT(payment_status = Pending)"
    ],

    "Grain": [
        "Order",
        "Order",
        "Order",
        "Order",
        "Order",
        "Order",
        "Order",
        "Order"
    ],

    "Filters": [
        "All valid orders",
        "Valid quantity values",
        "Valid quantity and price values",
        "Valid orders",
        "Valid unit prices",
        "Valid discount values",
        "Payment status = Paid",
        "Payment status = Pending"
    ],

    "Owner": [
        "Sales Manager",
        "Sales Manager",
        "Sales Manager",
        "Sales Manager",
        "Sales Manager",
        "Sales Manager",
        "Finance Team",
        "Finance Team"
    ],

    "Refresh Cadence": [
        "Daily",
        "Daily",
        "Daily",
        "Daily",
        "Daily",
        "Daily",
        "Daily",
        "Daily"
    ],

    "Business Meaning": [
        "Total number of unique orders",
        "Total quantity ordered",
        "Revenue generated after discount",
        "Average revenue generated per order",
        "Average price of products/services",
        "Average discount given to customers",
        "Number of successfully paid orders",
        "Number of orders with pending payment"
    ]
})

kpi_dictionary_final.to_csv(
    "KPI_Dictionary_Final.csv",
    index=False
)

print("\nKPI Dictionary Final saved successfully.")


# ==========================================
# STEP 9 - DATA QUALITY CONTRACT
# ==========================================

data_quality_contract = pd.DataFrame({
    "Data Quality Dimension": [
        "Uniqueness",
        "Completeness",
        "Validity",
        "Validity",
        "Validity",
        "Consistency",
        "Consistency",
        "Completeness"
        "Freshness"
    ],

    "Field": [
        "order_id",
        "order_id",
        "quantity",
        "discount_pct",
        "order_date",
        "customer_segment",
        "payment_status",
        "city"
        "order_date"
    ],

    "Business Rule": [
        "Order ID must be unique.",
        "Order ID must not be missing.",
        "Quantity must be a positive whole number.",
        "Discount must be between 0 and 100.",
        "Order date must be a valid date.",
        "Customer segment must be Student, Fresher, or Professional.",
        "Payment status must be Paid, Pending, Failed, or Refunded.",
        "City must not be missing."
        "Latest order date should be within 30 days of analysis date."
    ],

    "Failure Threshold": [
        "0 duplicates allowed",
        "0 missing values allowed",
        "0 invalid values allowed",
        "0 invalid values allowed",
        "0 invalid/missing dates allowed",
        "0 invalid categories allowed",
        "0 invalid statuses allowed",
        "0 missing values allowed"
        "More than 30 days old"
    ],

    "Action If Failed": [
        "Remove duplicate record after investigation.",
        "Investigate source data and correct the missing ID.",
        "Convert invalid values to missing and investigate.",
        "Convert invalid values to missing and investigate.",
        "Correct date format or investigate missing date.",
        "Normalize category values.",
        "Normalize status values.",
        "Investigate source data and correct missing city."
        "Review/update source data."
    ],

    "Escalation Owner": [
        "Data Analyst",
        "Data Analyst",
        "Data Analyst",
        "Data Analyst",
        "Data Analyst",
        "Data Analyst",
        "Finance Team",
        "Operations Team"
        "Retail/Sales Manager"
    ]
})

data_quality_contract.to_csv(
    "Data_Quality_Contract.csv",
    index=False
)

print("Data Quality Contract saved successfully.")

print("\n========================================")
print("TASK 02 COMPLETED")
print("========================================")
print("\nFiles created:")
print("1. KPI_Dictionary_Final.csv")
print("2. Data_Quality_Contract.csv")
# ==========================================
# FRESHNESS CHECK
# ==========================================

print("\n========== FRESHNESS CHECK ==========")

from datetime import datetime

latest_order_date = clean_df["order_date"].max()
analysis_date = pd.Timestamp.today().normalize()

if pd.isna(latest_order_date):
    print("Freshness Status: FAIL")
    print("Reason: No valid order date available.")
else:
    data_age_days = (analysis_date - latest_order_date).days

    print("Latest Order Date:", latest_order_date.date())
    print("Analysis Date:", analysis_date.date())
    print("Data Age:", data_age_days, "days")

    freshness_threshold = 30

    if data_age_days <= freshness_threshold:
        print("Freshness Status: PASS")
    else:
        print("Freshness Status: FAIL")
        print(
            "Reason: Latest order date is older than",
            freshness_threshold,
            "days."
        )

print("FRESHNESS CHECK COMPLETED")


print("\n========================================")
print("TASK 02 COMPLETED")
print("========================================")