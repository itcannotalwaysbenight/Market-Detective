# 🕵️‍♂️ Market Detective: Lagos Real Estate Scraper

A **production-grade Python data pipeline** that intelligently scrapes PropertyPro Nigeria listings, deduplicates records, identifies market trends, and flags undervalued properties through statistical analysis.

## 🚀 Overview

**Market Detective** automatically scans property listings with smart page tracking, automatic deduplication, and batch processing. It:

✅ Scrapes PropertyPro Nigeria listings (houses only - no lands)
✅ Automatically deduplicates properties across batches
✅ Tracks scraped pages to avoid re-scraping
✅ Resumes from last scraped page seamlessly
✅ Saves data in intelligent batches (100 records per file)
✅ Calculates market averages by bedroom count
✅ Identifies deals **50% below market average**
✅ Extracts schema-compatible data (ready for database)

---

## 🛠️ Tech Stack

- **Language:** Python 3.12
- **Web Scraping:** BeautifulSoup4, Requests
- **Data Processing:** Pandas
- **Visualization:** Matplotlib
- **Data Cleaning:** Regex (Re)
- **Storage:** JSON (metadata), CSV (batches)

---

## 📁 Project Structure

```
Market-Detective/
├── brain.py                      # 🧠 Core analysis engine
├── scraper.py                    # 🕷️ Web scraper with schema extraction
├── cleaners.py                   # 🧹 Data cleaning utilities
├── plotter.py                    # 📊 Visualization (future)
├── requirements.txt              # Dependencies
├── README.md                      # This file
└── pulled-data/                  # 📁 Output directory
    ├── batch_001_*.csv           # Batch files (100 records each)
    ├── batch_002_*.csv
    ├── scrape_metadata.json      # Tracking file
    └── property_hashes.json      # Deduplication hashes
```

---

## 🎯 Key Features

### 1. **Intelligent Deduplication**
- Tracks all scraped property URLs in `property_hashes.json`
- Automatically removes duplicates across batches
- Uses URL as unique identifier (100% accurate)
- Shows duplicate count in output

### 2. **Smart Page Tracking**
- Records which pages have been scraped
- Never re-scrapes the same page unless forced
- Maintains cumulative statistics
- Stores metadata in `scrape_metadata.json`

### 3. **Batch Processing**
- Saves data in batches of 100 records
- One file per batch with timestamp
- Example: `batch_001_20260206_150508.csv`
- Zero duplicate records stored

### 4. **Schema-Ready Data**
Extracted fields ready for database insertion:
- Property Name & Type
- Description
- Price, Bedrooms, Baths, Toilets
- Location (Full, City, State, Country)
- Images URLs (array)
- Furnished Status (Fully/Partially/Unfurnished)
- Features/Amenities (array)
- Property URL

---

## 📊 Metadata Tracking

`scrape_metadata.json` contains:

```json
{
  "last_page": 2,
  "scraped_pages": [1, 2],
  "total_records": 26,
  "total_batches": 1,
  "duplicates_skipped": 13,
  "last_scrape_range": "1-2",
  "last_updated": "2026-02-06 15:05:08"
}
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.10+
- pip (Python package manager)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/TheProject0824/market-detective.git
   cd market-detective
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Usage Guide

### Basic Commands

#### 1. **Scrape a Specific Page Range**
```bash
# Scrape pages 1-5 (skips if already done)
python brain.py 1 5

# Scrape pages 10-20
python brain.py 10 20

# Scrape pages 50-100
python brain.py 50 100
```

**Output:**
```
Starting scrape for pages 1-5 (5 pages)...

Scanning Page 1...
  Found 22 listings on search page.
  [OK] Extracted: 5 Bedroom Detached Duplex...
  ...
Total listings scraped: 110
Deduplicating against 0 previously scraped properties...
  ⊘ Removed 13 duplicate(s)
  ✓ 97 unique new listings

Records after cleaning: 85
Saving data in batches of 100 records:
  ✓ Saved batch 1 (85 records) → pulled-data/batch_001_20260206_150508.csv

✓ Total files created: 1

MARKET ANALYSIS - Average Price by Bedroom Count
Bedrooms
3   130,000,000
4   514,583,333
5   546,666,667
```

---

#### 2. **Resume from Last Scraped Page**
```bash
# Continue where you left off (next 10 pages)
python brain.py resume
```

**How it works:**
- If last page was 5, scrapes pages 6-15
- If no previous scrape, starts at page 1
- Automatically deduplicates against previous records

---

#### 3. **Force Re-scrape Pages**
```bash
# Re-scrape pages 1-5 (overwrites duplicates check)
python brain.py force 1 5

# Force re-scrape pages 10-15
python brain.py force 10 15
```

⚠️ **Use Case:** Website content updated, data refresh needed

---

#### 4. **View Scraping History**
```bash
# Show all progress and statistics
python brain.py history
```

**Output:**
```
SCRAPING HISTORY & STATISTICS
============================================================
Pages scraped: 1, 2, 3, 4, 5
Last page: 5
Total unique records: 426
Total batches created: 4
Duplicates skipped: 87
Last updated: 2026-02-06 16:30:00

✓ Successfully scraped pages: 1-5
  (Total: 5 pages)
```

---

#### 5. **Default Scrape (Pages 1-5)**
```bash
# Scrape pages 1-5 if nothing specified
python brain.py
```

---

### 📋 Complete Command Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `python brain.py <start> <end>` | Scrape specific pages | `python brain.py 1 10` |
| `python brain.py force <start> <end>` | Force re-scrape pages | `python brain.py force 1 5` |
| `python brain.py resume` | Continue from last page | `python brain.py resume` |
| `python brain.py history` | Show progress stats | `python brain.py history` |
| `python brain.py` | Default (pages 1-5) | `python brain.py` |

---

## 📊 Understanding the Output

### Batch Files
Each batch file contains:
- **Filename:** `batch_001_20260206_150508.csv`
- **Format:** CSV with 15 columns
- **Size:** ~100 records per file
- **Uniqueness:** Zero duplicates

### Market Analysis
```
MARKET ANALYSIS - Average Price by Bedroom Count
Bedrooms
2   85,000,000
3   130,000,000
4   514,583,333
5   546,666,667
```

### Deal Detection
Properties listed **50% below average** for their bedroom count:

```
TOP 10 POTENTIAL DEALS
Property Name              Price       Bedrooms  Location
Luxury 4BR Bungalow        80,000,000  4         Lekki Lagos
4BR Terrace Duplex         150,000,000 4         Ibadan Oyo
5BR Semi Detached          210,000,000 5         Lekki Lagos
```

---

## 🔍 Data Quality

### Deduplication Strategy
- **Primary Key:** Property URL (unique identifier)
- **Scope:** Across all batches and sessions
- **Storage:** `property_hashes.json`
- **Efficiency:** O(1) lookup time

### Data Cleaning
Filters applied automatically:
- Price: ₦0 - ₦2,000,000,000 (valid range)
- Bedrooms: > 0 (filters out lands/plots)
- Property Type: Houses only (no commercial)

### Fields Extracted
```python
[
  'Property Name',      # e.g., "5 Bedroom Detached Duplex"
  'Property Type',      # e.g., "Detached Duplex"
  'Description',        # From JSON-LD schema
  'Price',              # In ₦ (Naira)
  'Bedrooms',           # From structured data
  'Baths',              # From structured data
  'Toilets',            # From structured data
  'Location',           # Full address
  'City',               # Parsed (e.g., "Lekki")
  'State',              # Parsed (e.g., "Lagos")
  'Country',            # Always "Nigeria"
  'Images',             # Array of URLs
  'Furnished',          # "Fully", "Partially", "Unfurnished"
  'Features',           # Array (e.g., ["Pool", "Security"])
  'URL'                 # PropertyPro listing URL
]
```

---

## 📈 Workflow Examples

### Example 1: Large-Scale Scraping (250 pages)

```bash
# Session 1: Scrape pages 1-50
python brain.py 1 50
# → Creates 5 batch files (500 records)

# Session 2: Resume from page 51
python brain.py resume
# → Scrapes pages 51-60 automatically (10 more pages)
# → Creates batch 6

# Session 3: Continue
python brain.py resume
# → Scrapes pages 61-70
# → Creates batch 7

# Repeat until all 250 pages done

# Anytime, check progress
python brain.py history
# Shows: Pages 1-60 scraped, 600 total records, 75 duplicates removed
```

### Example 2: Targeted Market Research

```bash
# Find deals in specific regions (pages 1-5)
python brain.py 1 5

# See results in brain.py output (market analysis)

# Continue deeper
python brain.py 6 15

# Compare between sessions - metadata tracks everything
python brain.py history
```

### Example 3: Data Refresh

```bash
# Original scrape
python brain.py 1 100

# Later: Website content updated, need fresh data
python brain.py force 1 100
# ⚠️ Re-scrapes even if done before
# Creates new batch files with fresh data
```

---

## 🗂️ Output Structure

After scraping, your `pulled-data/` folder looks like:

```
pulled-data/
├── batch_001_20260206_150508.csv    (100 records)
├── batch_002_20260206_150610.csv    (100 records)
├── batch_003_20260206_150712.csv    (85 records)
├── scrape_metadata.json              (progress tracking)
└── property_hashes.json              (deduplication)
```

Each CSV is ready to:
- Load into your database
- Use for analysis
- Share with team
- Archive as backup

---

## 🎓 Understanding Deduplication

### Why Deduplication Matters
PropertyPro listings can appear across multiple pages. Without deduplication:
- Same property listed in multiple batches
- Inflated statistics
- Database bloat

### How It Works
```
1. First scrape (Pages 1-2): 44 raw listings
   → 13 are duplicates (same property)
   → 31 unique → Save to batch_001.csv
   → Store 31 URLs in property_hashes.json

2. Resume scrape (Pages 3-4): 44 raw listings
   → System checks against property_hashes.json
   → Removes any URLs already seen
   → Only NEW listings saved to batch_002.csv

3. Result: Zero duplicate records across batches
```

---

## 📱 Real-World Use Cases

### 1. **Real Estate Analyst**
```bash
# Monthly data refresh
python brain.py 1 50  # Get latest 50 pages
python brain.py history  # Track accumulation
```

### 2. **Investment Researcher**
```bash
# Find underpriced deals
python brain.py 1 100
# Output shows deals 50% below average
```

### 3. **Data Team**
```bash
# Large-scale historical collection
python brain.py 1 10
python brain.py resume    # 10 more
python brain.py resume    # 10 more
# ... repeat until 250+ pages collected
```

### 4. **API Integration**
```python
from brain import run_analysis

# Call programmatically
df, avg_prices = run_analysis(start_page=1, end_page=10)

# Now df contains all your data
# avg_prices has market analysis
```

---

## 🚨 Troubleshooting

### "All pages have been scraped already!"
```bash
# Solution 1: Scrape new pages
python brain.py 51 100

# Solution 2: Force re-scrape
python brain.py force 1 10

# Solution 3: Resume (auto continues)
python brain.py resume
```

### "Scraper returned nothing"
```bash
# Check your internet connection
# Check if PropertyPro is online
# Verify scraper.py HTML selectors haven't changed
```

### Duplicates still appearing?
```bash
# Check property_hashes.json exists
cat pulled-data/property_hashes.json | head -20

# Force re-scrape to regenerate hashes
python brain.py force 1 5
```

---

## 📝 Sample Insights

Once you've scraped 100+ pages, you'll see:

```
MARKET ANALYSIS - Average Price by Bedroom Count
Bedrooms
2    85,000,000      ₦
3   130,000,000      ₦
4   514,583,333      ₦
5   546,666,667      ₦
6   700,000,009      ₦

TOP 10 POTENTIAL DEALS
- 4BR for ₦80M (vs ₦515M average)
- 5BR for ₦145M (vs ₦547M average)
- Properties in emerging markets
```

---

## 🔐 Data Privacy & Ethics

- **Scraping:** Respects PropertyPro's robots.txt
- **Rate Limiting:** Built-in delays between requests (0.3s per page)
- **User-Agent:** Identifies as legitimate browser
- **Storage:** Local CSV files (no external uploads)
- **Use:** Personal research, business intelligence

---

## 📦 Requirements

```
requests>=2.31.0
beautifulsoup4>=4.12.0
pandas>=2.0.0
matplotlib>=3.7.0
```

Install all:
```bash
pip install -r requirements.txt
```

---

## 📝 License

MIT License - Free to use for personal and commercial projects.

---

## 🤝 Contributing

Found a bug or have a feature request?

1. Check existing issues
2. Create a new issue with details
3. Submit pull request

---

## 📞 Support

Need help? Check:
- ✅ `python brain.py history` - View your progress
- ✅ Look at `pulled-data/scrape_metadata.json` - Understand what's been scraped
- ✅ Check `pulled-data/property_hashes.json` - See unique properties found

---

## 🎉 Quick Start

```bash
# 1. Install
pip install -r requirements.txt

# 2. Scrape pages 1-5
python brain.py 1 5

# 3. Check results
python brain.py history

# 4. Continue scraping
python brain.py resume

# 5. Analyze batch files in pulled-data/
```

Done! You now have production-grade real estate market data. 🚀

---

**Made with ❤️ for data enthusiasts and real estate professionals**
