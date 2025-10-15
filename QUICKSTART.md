# Quick Start Guide

Get up and running with Snowflake data analytics in 5 minutes!

## Prerequisites
- Python 3.8 or higher installed
- Snowflake account with credentials ready
- Terminal access

## Step 1: Run Setup Script

The easiest way to get started is to run our automated setup script:

```bash
./setup.sh
```

This will:
- ✅ Create a Python virtual environment
- ✅ Install all required packages
- ✅ Create a `.env` file for your credentials

## Step 2: Configure Snowflake Credentials

Edit the `.env` file with your Snowflake credentials:

```bash
nano .env
```

Fill in your details:
```
SNOWFLAKE_ACCOUNT=abc12345.us-east-1
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=MY_DATABASE
SNOWFLAKE_SCHEMA=PUBLIC
SNOWFLAKE_ROLE=ACCOUNTADMIN
```

### Finding Your Snowflake Account Identifier

Your account identifier looks like: `abc12345.us-east-1`

You can find it in:
- Your Snowflake URL: `https://abc12345.us-east-1.snowflakecomputing.com`
- Take the part before `.snowflakecomputing.com`

## Step 3: Test Connection

Test that everything works:

```bash
python snowflake_connector.py
```

You should see:
```
✅ Successfully connected to Snowflake
```

## Step 4: Start Analyzing Data

### Option A: Use Jupyter Notebook (Recommended)

Launch the interactive notebook:

```bash
jupyter notebook data_analytics.ipynb
```

This opens a browser with an interactive notebook where you can:
- Run SQL queries
- Visualize data
- Export results
- All with a nice UI!

### Option B: Use Python Scripts

Create your own Python script:

```python
from snowflake_connector import SnowflakeConnector
import pandas as pd

# Connect to Snowflake
with SnowflakeConnector() as sf:
    # Run a query
    df = sf.query_to_dataframe("""
        SELECT * FROM your_table LIMIT 100
    """)
    
    # Analyze the data
    print(df.describe())
    
    # Export results
    df.to_csv('results.csv', index=False)
```

## Common First Queries

### See all available tables:
```python
tables = sf.list_tables()
print(tables)
```

### Get table structure:
```python
info = sf.get_table_info('YOUR_TABLE_NAME')
print(info)
```

### Query data:
```python
df = sf.query_to_dataframe("""
    SELECT * FROM your_table LIMIT 10
""")
print(df.head())
```

## Troubleshooting

### Error: "Failed to connect to Snowflake"
- Check your account identifier format
- Verify credentials are correct
- Ensure your warehouse is running in Snowflake
- Check if your IP is whitelisted

### Error: "No module named 'snowflake'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "Permission denied: ./setup.sh"
```bash
chmod +x setup.sh
./setup.sh
```

## Next Steps

Once you're connected:

1. **Explore your data** - Use the Jupyter notebook to run queries
2. **Create visualizations** - Examples included for charts and graphs
3. **Export results** - Save to CSV, Excel, or other formats
4. **Automate** - Create Python scripts for recurring analyses

## Need Help?

- Check the [README.md](README.md) for detailed documentation
- Review [example_queries.sql](example_queries.sql) for SQL examples
- Look at the Jupyter notebook for interactive examples

Happy analyzing! 📊🚀

