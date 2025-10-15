# 🚀 Quick Setup Guide for SSO Users

## Step-by-Step Instructions

### Step 1: Find Your Snowflake Account Details

1. **Open Snowflake in your browser** (via your company SSO)
   
2. **Look at the URL** - it will look like:
   ```
   https://xyz12345.us-east-1.snowflakecomputing.com
   ```
   Your account identifier is: `xyz12345.us-east-1`

3. **In Snowflake UI, run this query to get your settings:**
   ```sql
   SELECT 
       CURRENT_USER() as username,
       CURRENT_ROLE() as role,
       CURRENT_DATABASE() as database,
       CURRENT_SCHEMA() as schema,
       CURRENT_WAREHOUSE() as warehouse,
       CURRENT_ACCOUNT() as account;
   ```
   
   Copy these values - you'll need them!

### Step 2: Configure Your .env File

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the .env file:**
   ```bash
   nano .env
   # or
   code .env
   ```

3. **Fill in your values** (example based on your query):
   ```bash
   # Your account from the URL
   SNOWFLAKE_ACCOUNT=xyz12345.us-east-1
   
   # Your username (from the query above)
   SNOWFLAKE_USER=your.email@company.com
   
   # IMPORTANT: Use SSO authentication
   SNOWFLAKE_AUTHENTICATOR=externalbrowser
   
   # From the query results above
   SNOWFLAKE_WAREHOUSE=COMPUTE_WH
   SNOWFLAKE_DATABASE=PRODDB
   SNOWFLAKE_SCHEMA=PUBLIC
   SNOWFLAKE_ROLE=YOUR_ROLE
   ```

   **Note:** Do NOT set a password when using SSO!

### Step 3: Test Your Connection

Run the quick test script:

```bash
python quick_test.py
```

**What will happen:**
1. Script starts
2. Browser window opens automatically
3. You log in via your company SSO
4. Browser shows "Success" message
5. Return to terminal - your query will run!

### Step 4: Run Your Query in Jupyter

1. **Start Jupyter:**
   ```bash
   jupyter notebook data_analytics.ipynb
   ```

2. **Run the cells** - when you hit the "Connect" cell:
   - Browser will open for SSO login
   - Complete the login
   - Return to Jupyter
   - Continue running cells!

3. **Your specific query is already in the notebook:**
   ```python
   query = "SELECT * FROM PRODDB.PUBLIC.FACT_DEDUP_EXPERIMENT_EXPOSURE LIMIT 10"
   df = sf.query_to_dataframe(query)
   df.head()
   ```

## 📊 Direct Query Example (Copy & Run)

```python
from snowflake_connector import SnowflakeConnector

# Connect with SSO
with SnowflakeConnector() as sf:
    # Your query
    query = """
    SELECT * 
    FROM PRODDB.PUBLIC.FACT_DEDUP_EXPERIMENT_EXPOSURE 
    LIMIT 10
    """
    
    # Get results
    df = sf.query_to_dataframe(query)
    
    # Analyze
    print(f"Retrieved {len(df)} rows")
    print(f"Columns: {list(df.columns)}")
    print(df.head())
```

## ✅ Yes, You Can Run Queries Directly in Cursor!

You have several options:

### Option 1: Quick Test Script (Easiest)
```bash
python quick_test.py
```
Runs your exact query with SSO authentication!

### Option 2: Jupyter Notebook (Most Interactive)
```bash
jupyter notebook data_analytics.ipynb
```
Your query is already added - just run the cells!

### Option 3: Python Script
Create any `.py` file and use the connector:
```python
from snowflake_connector import SnowflakeConnector

with SnowflakeConnector() as sf:
    df = sf.query_to_dataframe("""
        SELECT * FROM PRODDB.PUBLIC.FACT_DEDUP_EXPERIMENT_EXPOSURE LIMIT 1
    """)
    print(df)
```

### Option 4: Interactive Python Shell
```bash
python3
>>> from snowflake_connector import SnowflakeConnector
>>> sf = SnowflakeConnector()
>>> sf.connect()  # Browser opens for SSO
>>> df = sf.query_to_dataframe("SELECT * FROM PRODDB.PUBLIC.FACT_DEDUP_EXPERIMENT_EXPOSURE LIMIT 1")
>>> print(df)
```

## 🔍 Common Questions

**Q: Where do I find my username?**
A: In Snowflake UI, click your profile (top right) or run `SELECT CURRENT_USER()`

**Q: What if I don't know my warehouse?**
A: Run `SHOW WAREHOUSES;` in Snowflake UI to see available warehouses

**Q: Do I need a password?**
A: No! With SSO (`SNOWFLAKE_AUTHENTICATOR=externalbrowser`), no password needed

**Q: What if the browser doesn't open?**
A: Make sure you're running from a terminal with GUI access (not SSH/remote)

**Q: Can I save my query results?**
A: Yes! 
```python
df.to_csv('results.csv', index=False)
df.to_excel('results.xlsx', index=False)
```

## 🎯 Your Exact Setup

Based on your query, here's your likely configuration:

```bash
SNOWFLAKE_ACCOUNT=<from_your_url>
SNOWFLAKE_USER=<your_email>
SNOWFLAKE_AUTHENTICATOR=externalbrowser
SNOWFLAKE_WAREHOUSE=COMPUTE_WH  # or whatever you use
SNOWFLAKE_DATABASE=PRODDB
SNOWFLAKE_SCHEMA=PUBLIC
SNOWFLAKE_ROLE=<your_role>
```

## 🚨 Troubleshooting

### "Cannot find table"
- Verify you have access: Run in Snowflake UI first
- Check capitalization: `PRODDB.PUBLIC.FACT_DEDUP_EXPERIMENT_EXPOSURE`
- Verify your role has permissions

### "Authentication failed"
- Check `SNOWFLAKE_AUTHENTICATOR=externalbrowser` is set
- Complete SSO login within 2 minutes
- Check browser isn't blocking popups

### "Warehouse not found"
- Run `SHOW WAREHOUSES;` in Snowflake
- Use an active warehouse
- Or start your warehouse: `ALTER WAREHOUSE <name> RESUME;`

## 🎉 Ready to Go!

1. Configure `.env` file ✓
2. Run `python quick_test.py` ✓
3. See your data! ✓

The notebook at `data_analytics.ipynb` is ready with your query pre-configured!

