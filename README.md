# Retail Data Analysis & Data Quality Project

## 1. Project Overview

This project focuses on analyzing retail order data and improving its data quality.

The project covers:

- Data profiling
- Data quality checks
- Data cleaning
- KPI calculation
- Business analysis
- Business recommendations
- KPI dictionary
- Data quality contract
- Freshness validation

The goal is to transform raw retail order data into clean, reliable, and useful information for business decision-making.

---

## 2. Business Decision Owner

**Decision Owner:** Retail/Sales Manager

The analysis is designed to help the Retail/Sales Manager understand:

- Sales performance
- Customer segment performance
- Product/category performance
- City-wise performance
- Payment status
- Data quality issues

These insights can support better sales and business decisions.

---

## 3. Project Objective

The main objectives of this project are:

1. Profile the raw retail dataset.
2. Identify data quality problems.
3. Clean and standardize the data.
4. Calculate important business KPIs.
5. Analyze customers, categories, cities, and payments.
6. Create a KPI dictionary.
7. Create a data quality contract.
8. Perform data freshness validation.
9. Provide actionable business recommendations.

---

## 4. Tools & Technologies

- Python
- Pandas
- NumPy
- PyCharm
- CSV files
- GitHub

---

## 5. Dataset

The project uses the following files:

### Raw Dataset

`retail-orders-raw.csv`

### Data Dictionary

`retail-data-dictionary.csv`

### Cleaned Dataset

`retail-orders-cleaned.csv`

### KPI Dictionary

`KPI_Dictionary_Final.csv`

### Data Quality Contract

`Data_Quality_Contract.csv`

---

## 6. Data Profiling

The raw dataset was profiled to understand:

- Number of rows
- Number of columns
- Column names
- Data types
- Missing values
- Duplicate records
- Customer segment values
- Payment status values

---

## 7. Data Quality Issues Identified

The raw dataset contained several quality issues.

### Duplicate Order IDs

Duplicate order ID:

- RT-1004

The duplicate record was removed during cleaning.

### Invalid Quantity

Examples:

- RT-1006 had quantity `-1`
- RT-1008 had quantity `two`

Invalid quantities were converted to missing values for investigation.

### Discount Issues

- RT-1003 had a missing discount.
- RT-1007 had a discount greater than 100%.

Invalid discount values were converted to missing values.

### Date Issues

The dataset contained:

- Different date formats
- An invalid date
- A missing date

Invalid or missing dates were converted to missing values for investigation.

### Category Consistency

Customer segment values such as:

- `student`
- `Student`

were normalized into a standard format.

### Payment Status Consistency

Payment status values such as:

- `paid`
- `Paid`

were standardized.

### Missing City

A missing city value was identified and flagged for investigation.

---

## 8. Data Cleaning

The following cleaning operations were performed:

- Removed duplicate records.
- Standardized customer segment values.
- Standardized payment status values.
- Converted quantity into numeric format.
- Converted invalid quantities into missing values.
- Converted discount into numeric format.
- Identified invalid discount values.
- Converted order dates into date format.
- Saved the cleaned dataset as:

`retail-orders-cleaned.csv`

---

## 9. Sales Calculation

Sales were calculated using the following formula:

**Sales = Quantity × Unit Price × (1 − Discount % / 100)**

For preliminary KPI calculation, missing discount values were treated as zero.

This assumption should be reviewed and confirmed with the business owner before using the metric for production reporting.

---

## 10. Key Performance Indicators (KPIs)

The project calculates at least 8 business KPIs.

### KPI 1 — Total Orders

**Formula:**

Number of unique Order IDs

**Business Meaning:**

Shows the total number of orders in the dataset.

---

### KPI 2 — Total Quantity

**Formula:**

Sum of valid quantities

**Business Meaning:**

Shows the total number of products/items ordered.

---

### KPI 3 — Total Sales

**Formula:**

Quantity × Unit Price × (1 − Discount % / 100)

**Business Meaning:**

Shows the total sales value generated from the orders.

---

### KPI 4 — Average Order Value

**Formula:**

Total Sales ÷ Total Orders

**Business Meaning:**

Shows the average sales value per order.

---

### KPI 5 — Average Unit Price

**Formula:**

Average of Unit Price

**Business Meaning:**

Shows the average selling price of products/services.

---

### KPI 6 — Average Discount

**Formula:**

Average Discount Percentage

**Business Meaning:**

Shows the average discount offered to customers.

---

### KPI 7 — Paid Orders

**Formula:**

Count of orders where Payment Status = Paid

**Business Meaning:**

Shows how many orders have successfully received payment.

---

### KPI 8 — Pending Orders

**Formula:**

Count of orders where Payment Status = Pending

**Business Meaning:**

Shows the number of orders where payment is still pending.

---

## 11. Business Analysis

The cleaned dataset was analyzed by:

- Product category
- Customer segment
- City
- Payment status

The analysis helps identify important business patterns and areas requiring attention.

---

## 12. Key Business Insights

### Top Category

**Course Access**

Course Access was identified as the top-performing category in the analysis.

### Top Customer Segment

**Professional**

Professional customers were identified as the top customer segment.

### Top City

**Chennai**

Chennai was identified as the top-performing city in the analysis.

---

## 13. Business Recommendations

### 1. Focus on Course Access

The business can explore additional promotion and marketing strategies for Course Access because it performed strongly in the analysis.

### 2. Target Professional Customers

The business can create targeted offers and campaigns for Professional customers.

### 3. Strengthen Chennai Market

The business can explore opportunities to increase sales and customer engagement in Chennai.

### 4. Monitor Pending Payments

Pending payments should be monitored regularly to reduce payment delays.

### 5. Improve Data Quality

Data entry and validation rules should be strengthened to prevent duplicate IDs, invalid quantities, incorrect discounts, missing cities, and date issues.

---

## 14. Data Quality Dimensions

The project evaluates the following data quality dimensions:

### Uniqueness

Order IDs should be unique.

### Completeness

Required fields should not contain missing values.

### Validity

Values should follow the defined business rules.

Examples:

- Quantity must be a positive whole number.
- Discount must be between 0 and 100.
- Order date must be valid.

### Consistency

Categorical values should follow standardized business values.

Examples:

- Student
- Fresher
- Professional

Payment statuses:

- Paid
- Pending
- Failed
- Refunded

### Freshness

The latest order date should be within the defined freshness threshold.

The current project uses a **30-day freshness threshold** as a validation rule.

---

## 15. Freshness Check

The project checks the latest available order date against the analysis date.

### Rule

Latest order date should be within 30 days of the analysis date.

### Failure Condition

If the latest order date is more than 30 days old, the freshness check is marked as failed.

### Action

Review and update the source data.

### Escalation Owner

Retail/Sales Manager

**Note:** `order_date` represents the business event date, so this is a freshness proxy. A production system should ideally contain a separate data ingestion or last-updated timestamp for a true freshness check.

---

## 16. KPI Dictionary

A separate file named:

`KPI_Dictionary_Final.csv`

contains:

- KPI Name
- Formula
- Grain
- Filters
- Owner
- Refresh Cadence
- Business Meaning

This provides a standardized definition for every KPI.

---

## 17. Data Quality Contract

A separate file named:

`Data_Quality_Contract.csv`

contains data quality rules for:

- Uniqueness
- Completeness
- Validity
- Consistency
- Freshness

Each rule includes:

- Data Quality Dimension
- Field
- Business Rule
- Failure Threshold
- Action If Failed
- Escalation Owner

---

## 18. Executable Data Quality Checks

The Python project performs executable checks for:

- Duplicate Order IDs
- Invalid quantities
- Invalid discounts
- Invalid/missing dates
- Customer segment consistency
- Payment status consistency
- Missing values
- Data freshness

---

## 19. Project Structure

```text
Retail-Data-Analysis/
│
├── retail-orders-raw.csv
├── retail-data-dictionary.csv
├── retail-orders-cleaned.csv
├── KPI_Dictionary_Final.csv
├── Data_Quality_Contract.csv
├── data_profiling.py
└── README.md

---

## 20. How to Run the Project

### Step 1

Install Python.

### Step 2

Install the required libraries:

```bash
pip install pandas numpy