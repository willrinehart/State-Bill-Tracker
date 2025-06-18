# State-Bill-Tracker

This project extracts and tracks US state bills related to artificial intelligence using two different legislative APIs: LegiScan and OpenStates.

## Features
- Search all US states for bills mentioning "artificial intelligence"
- Organize and export results to Excel, grouped by state
- Supports both LegiScan and OpenStates APIs

## Requirements
- Python 3.7+
- `requests`, `pandas`, and `openpyxl` libraries
- API keys for LegiScan and/or OpenStates

## Setup
Install dependencies:
```bash
pip install requests pandas openpyxl
```

## Usage

### 1. LegiScan AI Bill Extractor
Extracts AI-related bills from all US states using the [LegiScan API](https://legiscan.com/gaits/documentation/legiscan).

- **API Key:** Set your LegiScan API key in `legiscan_ai_bill_extractor.py`.
- **Run:**
```bash
python legiscan_ai_bill_extractor.py
```
- **Output:** `ai_bills_legiscan.xlsx`

*Issue: No description for bills provided*

### 2. OpenStates AI Bill Extractor
Extracts AI-related bills from all US state jurisdictions using the [OpenStates API](https://docs.openstates.org/api-v3/).

- **API Key:** Set your OpenStates API key in `openstates_ai_bill_extractor.py`.
- **Run:**
```bash
python openstates_ai_bill_extractor.py
```
- **Output:** `ai_bills_openstates.xlsx`

*Issue: Default API rate limit is set to 500 daily request*

## Notes
- Both scripts will create an Excel file with all relevant bill data, including descriptions.
- You may need to adjust API rate limits or add delays if you encounter errors.
- For large-scale or repeated use, consider caching API results to avoid rate limits.

## License
MIT


