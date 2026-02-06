# brain.py - Intelligent Property Scraper with Deduplication & Resume

from scraper import scrape_properties
import pandas as pd
import os
import json
import hashlib
from datetime import datetime

pd.options.display.max_columns = None
pd.options.display.float_format = '{:,.0f}'.format

# Create pulled-data folder if it doesn't exist
PULLED_DATA_DIR = "pulled-data"
METADATA_FILE = f"{PULLED_DATA_DIR}/scrape_metadata.json"
DEDUPE_FILE = f"{PULLED_DATA_DIR}/property_hashes.json"  # Track all property URLs we've seen

if not os.path.exists(PULLED_DATA_DIR):
    os.makedirs(PULLED_DATA_DIR)
    print(f"Created '{PULLED_DATA_DIR}' folder")

def load_metadata():
    """Load scraping metadata (pages scraped, total records, etc.)"""
    if os.path.exists(METADATA_FILE):
        try:
            with open(METADATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return None
    return None

def save_metadata(metadata):
    """Save scraping metadata."""
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f, indent=2)

def load_property_hashes():
    """Load all property URLs we've previously scraped."""
    if os.path.exists(DEDUPE_FILE):
        try:
            with open(DEDUPE_FILE, 'r') as f:
                data = json.load(f)
                return set(data.get('urls', []))
        except:
            return set()
    return set()

def save_property_hashes(urls_set):
    """Save all unique property URLs."""
    with open(DEDUPE_FILE, 'w') as f:
        json.dump({'urls': list(urls_set)}, f)

def get_metadata_summary():
    """Print current scraping progress."""
    metadata = load_metadata()
    if not metadata:
        print("No scraping history found. Starting fresh!")
        return

    print("\n" + "="*70)
    print("SCRAPING HISTORY & STATISTICS")
    print("="*70)
    print(f"Pages scraped: {', '.join(map(str, sorted(metadata.get('scraped_pages', []))))}")
    print(f"Last page: {metadata.get('last_page', 'N/A')}")
    print(f"Total unique records: {metadata.get('total_records', 0)}")
    print(f"Total batches created: {metadata.get('total_batches', 0)}")
    print(f"Duplicates skipped: {metadata.get('duplicates_skipped', 0)}")
    print(f"Last updated: {metadata.get('last_updated', 'N/A')}")

    # Show available pages to scrape
    if metadata.get('scraped_pages'):
        scraped = set(metadata.get('scraped_pages', []))
        print(f"\n✓ Successfully scraped pages: {min(scraped)}-{max(scraped)}")
        print(f"  (Total: {len(scraped)} pages)")
    print("="*70 + "\n")

def deduplicate_listings(listings, seen_urls):
    """
    Remove duplicate listings based on URL.
    Returns: (deduplicated_list, duplicates_count, new_urls_set)
    """
    unique_listings = []
    duplicate_count = 0

    for listing in listings:
        url = listing.get('URL', '')
        if url not in seen_urls:
            unique_listings.append(listing)
            seen_urls.add(url)
        else:
            duplicate_count += 1

    return unique_listings, duplicate_count, seen_urls

def save_batch(batch_data, batch_number):
    """Save a batch of 100 records to a CSV file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{PULLED_DATA_DIR}/batch_{batch_number:03d}_{timestamp}.csv"

    df_batch = pd.DataFrame(batch_data)
    df_batch.to_csv(filename, index=False)
    print(f"  ✓ Saved batch {batch_number} ({len(batch_data)} records) → {filename}")
    return filename

def run_analysis(start_page=None, end_page=None, resume=False, force=False):
    """
    Intelligently scrape properties with deduplication and page tracking.

    Parameters:
    -----------
    start_page : int, optional
        First page to scrape
    end_page : int, optional
        Last page to scrape
    resume : bool, optional
        Resume from the last scraped page
    force : bool, optional
        Force scrape pages even if they've been scraped before (default: False)

    Examples:
    ---------
    # Scrape pages 1-5 (skip if already scraped)
    run_analysis(start_page=1, end_page=5)

    # Force scrape pages 1-5 (even if scraped before)
    run_analysis(start_page=1, end_page=5, force=True)

    # Resume from last page
    run_analysis(resume=True)

    # Show progress
    python brain.py history
    """

    # Handle page range logic
    metadata = load_metadata()
    seen_urls = load_property_hashes()

    if resume:
        if not metadata:
            print("No previous scraping found. Starting from page 1.")
            start_page = 1
            end_page = 10
        else:
            last_page = metadata.get('last_page', 1)
            print(f"Resuming from page {last_page + 1}...")
            start_page = last_page + 1
            end_page = last_page + 10  # Scrape next 10 pages
    else:
        if start_page is None:
            start_page = 1
        if end_page is None:
            end_page = start_page

    # Validate page range
    if start_page > end_page:
        print("Error: start_page cannot be greater than end_page")
        return pd.DataFrame(), pd.Series()

    # Check which pages have already been scraped
    previously_scraped = set(metadata.get('scraped_pages', [])) if metadata else set()
    pages_to_scrape = []

    for page in range(start_page, end_page + 1):
        if page in previously_scraped and not force:
            print(f"⊘ Skipping page {page} (already scraped)")
        else:
            pages_to_scrape.append(page)

    if not pages_to_scrape:
        print("\nAll pages have been scraped already!")
        print("Use force=True to re-scrape or choose different pages.")
        get_metadata_summary()
        return pd.DataFrame(), pd.Series()

    num_pages = len(pages_to_scrape)
    print(f"\nStarting scrape for {num_pages} new page(s): {pages_to_scrape}...\n")

    # Scrape only new pages
    all_listings = []
    for page_num in pages_to_scrape:
        all_listings.extend(scrape_properties(pages=1, start_page=page_num))

    print(f"\nTotal listings scraped: {len(all_listings)}")

    if not all_listings:
        print("Scraper returned nothing. Check class names in scraper.py!")
        return pd.DataFrame(), pd.Series()

    # Deduplicate: Remove any listings we've already seen
    print(f"\nDeduplicating against {len(seen_urls)} previously scraped properties...")
    all_listings, duplicates_found, seen_urls = deduplicate_listings(all_listings, seen_urls)

    if duplicates_found > 0:
        print(f"  ⊘ Removed {duplicates_found} duplicate(s)")
    print(f"  ✓ {len(all_listings)} unique new listings")

    if not all_listings:
        print("\nNo new unique listings found. All were duplicates!")
        return pd.DataFrame(), pd.Series()

    # Create dataframe for analysis
    df = pd.DataFrame(all_listings)
    print(f"\nColumns: {df.columns.tolist()}\n")

    # 1. Basic Cleaning
    df_clean = df[(df['Price'] > 0) & (df['Price'] < 2_000_000_000)].copy()
    df_clean = df_clean.dropna(subset=['Bedrooms'])
    df_clean = df_clean[df_clean['Bedrooms'] > 0]  # Filter out plots/lands

    print(f"Records after cleaning: {len(df_clean)}\n")

    # 2. Save data in batches of 100
    if len(df_clean) > 0:
        print("Saving data in batches of 100 records:\n")

        # Get current batch number from metadata
        current_metadata = load_metadata()
        batch_number = (current_metadata.get('total_batches', 0) if current_metadata else 0) + 1
        batch_size = 100
        saved_files = []

        for i in range(0, len(df_clean), batch_size):
            batch = df_clean.iloc[i:i + batch_size]
            if len(batch) > 0:
                filename = save_batch(batch.to_dict('records'), batch_number)
                saved_files.append(filename)
                batch_number += 1

        print(f"\n✓ Total files created: {len(saved_files)}")

        # 3. Update metadata
        scraped_pages = list(previously_scraped.union(set(pages_to_scrape)))
        total_records = (current_metadata.get('total_records', 0) if current_metadata else 0) + len(df_clean)
        total_dups = (current_metadata.get('duplicates_skipped', 0) if current_metadata else 0) + duplicates_found

        new_metadata = {
            'last_page': max(pages_to_scrape),
            'scraped_pages': sorted(scraped_pages),
            'total_records': total_records,
            'total_batches': batch_number - 1,
            'duplicates_skipped': total_dups,
            'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'last_scrape_range': f"{min(pages_to_scrape)}-{max(pages_to_scrape)}"
        }
        save_metadata(new_metadata)

        # Save updated property hashes
        save_property_hashes(seen_urls)

        # 4. Market Analysis: Average Price by Bedroom Count
        avg_prices = df_clean.groupby('Bedrooms')['Price'].mean()

        print("\n" + "="*70)
        print("MARKET ANALYSIS - Average Price by Bedroom Count")
        print("="*70)
        print(avg_prices)

        # 5. Deal Detection Logic
        def find_deals(row):
            avg = avg_prices.get(row['Bedrooms'])
            if avg and row['Price'] < (avg * 0.5):
                return True
            return False

        df_clean['Is_Deal'] = df_clean.apply(find_deals, axis=1)

        # 6. Show interesting deals
        print("\n" + "="*70)
        print("TOP 10 POTENTIAL DEALS (50% below average)")
        print("="*70)
        deals = df_clean[df_clean['Is_Deal'] == True].sort_values('Price')
        if len(deals) > 0:
            print(deals[['Property Name', 'Price', 'Bedrooms', 'Location']].head(10).to_string())
            print(f"\nTotal deals found: {len(deals)}")
        else:
            print("No deals found (properties below 50% of average price)")

        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        print(f"Pages scraped this session: {pages_to_scrape}")
        print(f"New records added: {len(df_clean)}")
        print(f"Duplicates removed: {duplicates_found}")
        print(f"Total unique records so far: {total_records}")
        print(f"Total batches: {batch_number - 1}")
        print(f"Data saved to: {PULLED_DATA_DIR}/")
        print("="*70)

        return df_clean, avg_prices
    else:
        print("No data to analyze after cleaning!")
        return pd.DataFrame(), pd.Series()

if __name__ == "__main__":
    import sys

    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == 'resume':
            run_analysis(resume=True)
        elif sys.argv[1] == 'history':
            get_metadata_summary()
        elif sys.argv[1] == 'force' and len(sys.argv) >= 4:
            try:
                start = int(sys.argv[2])
                end = int(sys.argv[3])
                run_analysis(start_page=start, end_page=end, force=True)
            except ValueError:
                print("Usage: python brain.py force <start_page> <end_page>")
        elif len(sys.argv) >= 3:
            try:
                start = int(sys.argv[1])
                end = int(sys.argv[2])
                run_analysis(start_page=start, end_page=end)
            except ValueError:
                print("Usage:")
                print("  python brain.py <start_page> <end_page>")
                print("  python brain.py force <start_page> <end_page>  # Re-scrape pages")
                print("  python brain.py resume                         # Continue from last page")
                print("  python brain.py history                        # Show progress")
                print("\nExamples:")
                print("  python brain.py 1 10      # Scrape pages 1-10 (skip if already done)")
                print("  python brain.py force 1 5 # Force re-scrape pages 1-5")
                print("  python brain.py resume    # Resume from where you left off")
                print("  python brain.py history   # Show scraping progress")
    else:
        # Default: scrape pages 1-5
        run_analysis(start_page=1, end_page=5)
