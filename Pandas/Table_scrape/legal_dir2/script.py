import pandas as pd
import concurrent.futures
import time

def scrape_page(x, retries=3):
    url = f'https://www.mywsba.org/PersonifyEbusiness/LegalDirectory.aspx?ShowSearchResults=TRUE&LicenseType=Lawyer&EligibleToPractice=Y&Status=Active&Page={x}'
    
    attempts = 0
    while attempts < retries:
        try:
            tables = pd.read_html(url)
            
            if tables:
                df = tables[0]

                # df = df[~df.apply(lambda row: row.astype(str).str.contains('First|Prev|Next|Last').any(), axis=1)]
                df = df[~df.apply(lambda row: row.astype(str).str.contains('<< ').any(), axis=1)]
                df = df[~df.apply(lambda row: row.astype(str).str.contains('Next Page >Last >>').any(), axis=1)]
                # Count the number of rows in the current page
                row_count = len(df)

                # Check if this page has less than 20 rows
                if row_count < 20:
                    return df, x, row_count  # Return DataFrame, page number, and row count
                else:
                    return df, None, None  # Return DataFrame only

            else:
                print(f"No table found on page {x}")
                return None, None, None

        except Exception as e:
            print(f"Failed to scrape page {x}, attempt {attempts + 1}: {e}")
            attempts += 1
            time.sleep(2)  # Add a small delay before retrying
    
    print(f"Page {x} failed after {retries} attempts.")
    return None, None, None

# Lists to store data
all_tables = []
pages_with_less_data = []
total_rows = 0
failed_pages = []

# Use ThreadPoolExecutor for parallel scraping
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(scrape_page, x) for x in range(0, 1765)]
    
    for future in concurrent.futures.as_completed(futures):
        df, page, row_count = future.result()
        if df is not None:
            all_tables.append(df)
            total_rows += len(df)  # Update total rows counter
            print(f"Page scraped with {len(df)} rows.")
            if page is not None:
                pages_with_less_data.append((page, row_count))  # Store the page number and row count
        else:
            failed_pages.append(x)

# Concatenate all the dataframes into one
if all_tables:
    final_df = pd.concat(all_tables, ignore_index=True)
    
    # Save the final dataframe to an Excel file
    final_df.to_excel("output.xlsx", index=False)
    print("Data saved to output.xlsx")
else:
    print("No data found to save.")

# Print total number of rows scraped
print(f"Total rows scraped: {total_rows}")

# Print the pages with less than 20 rows
if pages_with_less_data:
    print("Pages with less than 20 rows:")
    for page, row_count in pages_with_less_data:
        print(f"Page {page} has {row_count} rows.")
else:
    print("All pages have 20 or more rows.")

# Print any pages that failed to scrape
if failed_pages:
    print(f"Failed to scrape the following pages: {failed_pages}")
else:
    print("No pages failed to scrape.")
