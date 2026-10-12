import pandas as pd
import glob

listing_files = sorted(glob.glob("CRMLSListing*.csv"))

print("Number of listing files:", len(listing_files))
print(listing_files)

listing_dfs = [pd.read_csv(file) for file in listing_files]
print("Number of listing DataFrames loaded:", len(listing_dfs))

listing_rows_before = sum(len(df) for df in listing_dfs)

print("Listing rows before concatenation:", listing_rows_before)
listings = pd.concat(listing_dfs, ignore_index=True)
print("Listing rows after concatenation:", len(listings))
print("Property types found:")
print(listings["PropertyType"].value_counts())
listings_residential = listings[listings["PropertyType"] == "Residential"].copy()
print("Listing rows before Residential filter:", len(listings))
print("Listing rows after Residential filter:", len(listings_residential))
listings_residential.to_csv("combined_listings_residential.csv", index=False)

print("Combined residential listings CSV saved successfully.")
# Find all monthly sold CSV files
sold_files = sorted(glob.glob("CRMLSSold*.csv"))

print("Number of sold files:", len(sold_files))
print(sold_files)
sold_dfs = [pd.read_csv(file) for file in sold_files]

print("Number of sold DataFrames loaded:", len(sold_dfs))
sold_rows_before = sum(len(df) for df in sold_dfs)

print("Sold rows before concatenation:", sold_rows_before)
# Combine all monthly sold datasets
sold = pd.concat(sold_dfs, ignore_index=True)

print("Sold rows after concatenation:", len(sold))

# Check property types
print("Sold property types found:")
print(sold["PropertyType"].value_counts())
# Filter sold dataset to Residential properties only
sold_residential = sold[sold["PropertyType"] == "Residential"].copy()

print("Sold rows before Residential filter:", len(sold))
print("Sold rows after Residential filter:", len(sold_residential))

# Save combined Residential sold dataset
sold_residential.to_csv("combined_sold_residential.csv", index=False)

print("Combined residential sold CSV saved successfully.")
