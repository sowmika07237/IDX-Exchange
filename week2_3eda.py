import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# WEEK 2-3: DATASET STRUCTURING, VALIDATION, AND EDA
# ============================================================


# ------------------------------------------------------------
# 1. LOAD WEEK 1 DATASETS
# ------------------------------------------------------------

sold = pd.read_csv(
    "combined_sold_residential.csv",
    low_memory=False
)

listings = pd.read_csv(
    "combined_listings_residential.csv",
    low_memory=False
)

print("\n================ DATASET SHAPES ================")

print("Sold dataset shape:", sold.shape)
print("Listings dataset shape:", listings.shape)


# ------------------------------------------------------------
# 2. INSPECT DATASET STRUCTURE
# ------------------------------------------------------------

print("\n================ SOLD FIRST 5 ROWS ================")
print(sold.head())

print("\n================ SOLD COLUMN NAMES ================")
print(sold.columns.tolist())

print("\n================ SOLD DATA TYPES ================")
print(sold.dtypes)

print("\n================ LISTINGS DATA TYPES ================")
print(listings.dtypes)


# ------------------------------------------------------------
# 3. PROPERTY TYPE VALIDATION
# ------------------------------------------------------------

print("\n================ SOLD PROPERTY TYPES ================")
print(sold["PropertyType"].value_counts(dropna=False))

print("\n================ LISTING PROPERTY TYPES ================")
print(listings["PropertyType"].value_counts(dropna=False))


# ------------------------------------------------------------
# 4. MISSING VALUE ANALYSIS - SOLD
# ------------------------------------------------------------

sold_missing = pd.DataFrame({
    "Missing_Count": sold.isnull().sum(),
    "Missing_Percent": (sold.isnull().sum() / len(sold)) * 100
})

sold_missing = sold_missing.sort_values(
    "Missing_Percent",
    ascending=False
)

print("\n================ SOLD MISSING VALUES ================")
print(sold_missing)


# ------------------------------------------------------------
# 5. MISSING VALUE ANALYSIS - LISTINGS
# ------------------------------------------------------------

listing_missing = pd.DataFrame({
    "Missing_Count": listings.isnull().sum(),
    "Missing_Percent": (listings.isnull().sum() / len(listings)) * 100
})

listing_missing = listing_missing.sort_values(
    "Missing_Percent",
    ascending=False
)

print("\n================ LISTING MISSING VALUES ================")
print(listing_missing)


# ------------------------------------------------------------
# 6. FLAG COLUMNS ABOVE 90% MISSING
# ------------------------------------------------------------

sold_over_90 = sold_missing[
    sold_missing["Missing_Percent"] > 90
]

listing_over_90 = listing_missing[
    listing_missing["Missing_Percent"] > 90
]

print("\n================ SOLD COLUMNS >90% MISSING ================")
print(sold_over_90)

print("\n================ LISTING COLUMNS >90% MISSING ================")
print(listing_over_90)


# ------------------------------------------------------------
# 7. SAVE MISSING VALUE REPORTS
# ------------------------------------------------------------

sold_missing.to_csv(
    "sold_missing_value_report.csv"
)

listing_missing.to_csv(
    "listing_missing_value_report.csv"
)

print("\nMissing value reports saved successfully.")


# ------------------------------------------------------------
# 8. NUMERIC DISTRIBUTION SUMMARY
# Required fields from internship handbook:
# ClosePrice, LivingArea, DaysOnMarket
# ------------------------------------------------------------

numeric_fields = [
    "ClosePrice",
    "LivingArea",
    "DaysOnMarket"
]

print("\n================ NUMERIC DISTRIBUTION SUMMARY ================")

numeric_summary = sold[numeric_fields].describe(
    percentiles=[0.25, 0.50, 0.75, 0.90, 0.95, 0.99]
).T

numeric_summary["median"] = sold[numeric_fields].median()

print(numeric_summary)

numeric_summary.to_csv(
    "numeric_distribution_summary.csv"
)

print("\nNumeric distribution summary saved successfully.")


# ------------------------------------------------------------
# 9. MEDIAN AND AVERAGE CLOSE PRICE
# ------------------------------------------------------------

average_close_price = sold["ClosePrice"].mean()
median_close_price = sold["ClosePrice"].median()

print("\n================ CLOSE PRICE ================")

print("Average Close Price:", average_close_price)
print("Median Close Price:", median_close_price)


# ------------------------------------------------------------
# 10. DAYS ON MARKET ANALYSIS
# ------------------------------------------------------------

print("\n================ DAYS ON MARKET ================")

print(sold["DaysOnMarket"].describe())

print(
    "Median Days on Market:",
    sold["DaysOnMarket"].median()
)


# ------------------------------------------------------------
# 11. HOMES SOLD ABOVE / BELOW / AT LIST PRICE
# ------------------------------------------------------------

valid_price = sold[
    (sold["ClosePrice"].notna()) &
    (sold["ListPrice"].notna()) &
    (sold["ListPrice"] > 0)
].copy()

valid_price["Sale_vs_List"] = "At List"

valid_price.loc[
    valid_price["ClosePrice"] > valid_price["ListPrice"],
    "Sale_vs_List"
] = "Above List"

valid_price.loc[
    valid_price["ClosePrice"] < valid_price["ListPrice"],
    "Sale_vs_List"
] = "Below List"

sale_vs_list_counts = valid_price["Sale_vs_List"].value_counts()

sale_vs_list_percent = (
    valid_price["Sale_vs_List"].value_counts(normalize=True) * 100
)

print("\n================ SOLD VS LIST PRICE ================")

print("\nCounts:")
print(sale_vs_list_counts)

print("\nPercentages:")
print(sale_vs_list_percent)


# ------------------------------------------------------------
# 12. DATE CONSISTENCY CHECK
# Example: close date occurring before listing date
# ------------------------------------------------------------

sold["CloseDate"] = pd.to_datetime(
    sold["CloseDate"],
    errors="coerce"
)

sold["ListingContractDate"] = pd.to_datetime(
    sold["ListingContractDate"],
    errors="coerce"
)

close_before_listing = sold[
    sold["CloseDate"] < sold["ListingContractDate"]
]

print("\n================ DATE CONSISTENCY ================")

print(
    "Records where CloseDate is before ListingContractDate:",
    len(close_before_listing)
)


# ------------------------------------------------------------
# 13. COUNTY MEDIAN CLOSE PRICE
# ------------------------------------------------------------

county_median_price = (
    sold
    .groupby("CountyOrParish")["ClosePrice"]
    .median()
    .sort_values(ascending=False)
)

print("\n================ COUNTY MEDIAN CLOSE PRICES ================")

print(county_median_price.head(20))

county_median_price.to_csv(
    "county_median_close_prices.csv"
)


# ------------------------------------------------------------
# 14. HISTOGRAMS
# ------------------------------------------------------------

for column in numeric_fields:

    data = sold[column].dropna()

    plt.figure(figsize=(8, 5))

    plt.hist(
        data,
        bins=50
    )

    plt.title(f"Distribution of {column}")
    plt.xlabel(column)
    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(
        f"{column}_histogram.png"
    )

    plt.close()


print("\nHistograms saved successfully.")


# ------------------------------------------------------------
# 15. BOXPLOTS
# ------------------------------------------------------------

for column in numeric_fields:

    data = sold[column].dropna()

    plt.figure(figsize=(8, 4))

    plt.boxplot(
        data,
        vert=False
    )

    plt.title(f"Boxplot of {column}")
    plt.xlabel(column)

    plt.tight_layout()

    plt.savefig(
        f"{column}_boxplot.png"
    )

    plt.close()


print("Boxplots saved successfully.")


# ------------------------------------------------------------
# 16. SAVE FILTERED DATASET
# ------------------------------------------------------------

sold.to_csv(
    "week2_3_filtered_sold.csv",
    index=False
)

print("\nFiltered sold dataset saved successfully.")


# ------------------------------------------------------------
# FINAL MESSAGE
# ------------------------------------------------------------

print("\n====================================================")
print("WEEK 2-3 EDA AND VALIDATION COMPLETE")
print("====================================================")
