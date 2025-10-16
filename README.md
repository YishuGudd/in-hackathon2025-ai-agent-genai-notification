# hackathon2025-ai-agent-for-genai-notification

Snowflake Data Analytics Project for Hackathon 2025

## Overview
This project provides a complete setup for connecting to Snowflake and performing data analytics using Python and Jupyter notebooks in Cursor.

## Features
- ✅ Secure Snowflake connection management
- ✅ Python connector with helper methods
- ✅ Interactive Jupyter notebook for data exploration
- ✅ Data visualization with matplotlib, seaborn, and plotly
- ✅ Example SQL queries
- ✅ Environment-based configuration

## Notification Generator v1.3 (Locale-aware)

This repo includes a notification generator with pricing intelligence (v1.2) and locale-aware copy (v1.3). Supported locales: Spanish (`es`), French-Canada (`fr-CA`), English-Canada (`en-CA`), default English-US (`en-US`).

### Prerequisites
- Snowflake credentials in `.env` (External Browser SSO supported)
- `consumer_ids.csv` with a `CONSUMER_ID` column (examples in the MCP repo)

### One-command E2E generation (profiles + locales + localization)
Run from your MCP repo (where the scripts are):
```bash
uv run python e2e_generate_localized.py
```
Outputs: `notifications_e2e_localized.csv` with columns:
- consumer_id, rank, score, title, body, keyword, url
- cuisines_preference, foods_preference, taste_preference, dietary_preference
- dd_user_locale, language, locale_applied, title_localized, body_localized
- title_length, body_length, title_length_localized, body_length_localized

### Post-process localization for an existing CSV
If you already have a pricing CSV, you can localize it via:
```bash
uv run python localize_notifications.py
```
Inputs: `notifications_with_pricing.csv` and `locale_joined_for_consumers.csv`
Output: `notifications_with_pricing_localized.csv`

### How locale is applied
- Detects locale via `DD_USER_LOCALE` then falls back to `LANGUAGE`
- Spanish and French-CA use curated translations for common titles/bodies
- English-CA adjusts spelling (e.g., favourites/flavours)
- Character limits enforced: title < 35 chars, body ≤ 140 chars

### Results (scores)
- Pricing (v1.2) average: 88.95 (139 notifications)
- E2E localized (v1.3) average: 88.83 (142 notifications)

Localization improves relevance for Spanish/French-CA audiences, but average score remains comparable to pricing-only results due to unchanged scoring logic. Future work could include locale-aware scoring.

### Locale-aware score (separate, non-ranking)
- New column: `locale_score` (does not affect ranking)
- Heuristics:
  - Exact language match (es): +3
  - French-CA match: +2
  - English-CA variant match: +1
  - Non-English copy shown to English user (or mismatched language): −4
  - Truncation applied to fit 35/140 limits: −1
- Final ranking still uses `score` only; `locale_score` is for analysis/QA.

## Prerequisites
- Python 3.8 or higher
- Snowflake account with credentials
- Cursor IDE

## Setup Instructions

### 1. Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Snowflake Credentials
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your Snowflake credentials
# Use your favorite editor or:
nano .env
```

Fill in your Snowflake credentials:
```
SNOWFLAKE_ACCOUNT=your_account_identifier
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
SNOWFLAKE_ROLE=your_role
```

### 4. Test Connection
```bash
# Test the connection
python snowflake_connector.py
```

### 5. Start Jupyter Notebook
```bash
# Launch Jupyter
jupyter notebook data_analytics.ipynb
```

## Project Structure
```
.
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment variables
├── .env                       # Your credentials (gitignored)
├── .gitignore                 # Git ignore rules
├── snowflake_connector.py     # Snowflake connection class
├── data_analytics.ipynb       # Interactive analytics notebook
└── example_queries.sql        # Sample SQL queries
```

## Usage Examples

### Using the Python Connector
```python
from snowflake_connector import SnowflakeConnector

# Context manager (recommended)
with SnowflakeConnector() as sf:
    df = sf.query_to_dataframe("SELECT * FROM my_table LIMIT 10")
    print(df.head())
```

### Running in Jupyter Notebook
Open `data_analytics.ipynb` in Jupyter and follow the step-by-step examples for:
- Connecting to Snowflake
- Exploring tables
- Running queries
- Data visualization
- Exporting results

## Common Operations

### List All Tables
```python
tables = sf.list_tables()
print(tables)
```

### Get Table Information
```python
table_info = sf.get_table_info('your_table_name')
print(table_info)
```

### Query to DataFrame
```python
query = """
SELECT category, COUNT(*) as count
FROM your_table
GROUP BY category
"""
df = sf.query_to_dataframe(query)
```

## Troubleshooting

### Connection Issues
- Verify your Snowflake account identifier is correct
- Check that your IP is whitelisted in Snowflake
- Ensure your user has necessary permissions
- Verify warehouse is running

### Package Installation Issues
```bash
# Upgrade pip
pip install --upgrade pip

# Install with verbose output
pip install -v snowflake-connector-python
```

## Security Best Practices
- Never commit `.env` file to version control
- Use role-based access control in Snowflake
- Rotate credentials regularly
- Use service accounts for production

## Contributing
This is a hackathon project. Feel free to add more features and analytics!

## Resources
- [Snowflake Python Connector Documentation](https://docs.snowflake.com/en/user-guide/python-connector.html)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Plotly Documentation](https://plotly.com/python/)

## License
MIT License - Hackathon 2025
