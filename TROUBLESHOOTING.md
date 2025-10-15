# 🔧 Troubleshooting Guide

## Error: 'NoneType' object has no attribute 'execute'

This error means you tried to run a query before establishing a connection to Snowflake.

### ✅ Quick Fix (In Jupyter Notebook)

**Option 1: Restart and Reload (Recommended)**

If you modified the code, restart the kernel:

1. In Jupyter: Click **Kernel → Restart & Clear Output**
2. Run the cells in order:
   - Cell 1: Imports ✓
   - Cell 2: Connect (browser will open for SSO) ✓
   - Cell 3+: Your queries ✓

**Option 2: Reload the Module**

Add this cell at the top and run it:

```python
import importlib
import snowflake_connector
importlib.reload(snowflake_connector)
from snowflake_connector import SnowflakeConnector
```

Then re-run the connection cell.

### 📋 Proper Order in Jupyter

```python
# CELL 1: Imports
import pandas as pd
from snowflake_connector import SnowflakeConnector

# CELL 2: Connect (MUST RUN THIS FIRST!)
sf = SnowflakeConnector()
print("Connecting...")
if sf.connect():
    print("✅ Connected!")
else:
    print("❌ Connection failed!")
    
# CELL 3: Now you can query
df = sf.query_to_dataframe("SELECT * FROM PRODDB.PUBLIC.FACT_DEDUP_EXPERIMENT_EXPOSURE LIMIT 1")
print(df)
```

### 🔍 Common Causes

1. **Didn't run connect() cell**
   - Make sure you run the cell that calls `sf.connect()`
   - Wait for it to complete (browser SSO login)

2. **Connection failed silently**
   - Check if `connect()` returned `True`
   - Look for error messages in the output

3. **SSO timeout**
   - If you didn't complete browser login in time
   - Re-run the connect cell

4. **Using wrong variable**
   - Make sure you're using the same `sf` variable
   - Don't create multiple `SnowflakeConnector()` instances

### ✅ Better Pattern (Recommended)

Use this pattern to avoid the error:

```python
from snowflake_connector import SnowflakeConnector

# Create connector
sf = SnowflakeConnector()

# Connect and check
if sf.connect():
    print("✅ Connected successfully!")
    
    # Now safe to query
    df = sf.query_to_dataframe("""
        SELECT * FROM PRODDB.PUBLIC.FACT_DEDUP_EXPERIMENT_EXPOSURE LIMIT 10
    """)
    print(f"Retrieved {len(df)} rows")
    print(df.head())
    
    # Close when done
    sf.close()
else:
    print("❌ Failed to connect. Check your .env file and credentials.")
```

### 🎯 Best Pattern (Context Manager)

This automatically handles connection and cleanup:

```python
from snowflake_connector import SnowflakeConnector

# Automatically connects and closes
with SnowflakeConnector() as sf:
    df = sf.query_to_dataframe("""
        SELECT * FROM PRODDB.PUBLIC.FACT_DEDUP_EXPERIMENT_EXPOSURE LIMIT 10
    """)
    print(df.head())
# Connection automatically closed here
```

## Other Common Issues

### "SNOWFLAKE_ACCOUNT not found"

**Problem:** .env file not configured or not in the right location

**Fix:**
```bash
# Check if .env exists
ls -la .env

# If not, create it
cp .env.example .env
nano .env  # Fill in your credentials
```

### "Failed to connect to Snowflake"

**Check these:**

1. **.env file configured?**
   ```bash
   cat .env | grep SNOWFLAKE_
   ```

2. **Using SSO authentication?**
   ```bash
   # Should have this line:
   SNOWFLAKE_AUTHENTICATOR=externalbrowser
   ```

3. **Browser opened for SSO?**
   - A browser window should open automatically
   - Complete the login
   - Return to Jupyter

4. **Correct account identifier?**
   ```bash
   # From your Snowflake URL
   # https://abc123.us-east-1.snowflakecomputing.com
   # Use: abc123.us-east-1
   ```

### "Cannot find module snowflake"

**Problem:** Packages not installed

**Fix:**
```bash
# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Restart Jupyter
jupyter notebook data_analytics.ipynb
```

### Jupyter Kernel Issues

**Problem:** Changes not taking effect

**Fix:**
```
1. Jupyter menu: Kernel → Restart & Clear Output
2. Re-run all cells from the top
```

## 🆘 Still Having Issues?

### Check Your Setup

Run this diagnostic:

```bash
python test_connection.py
```

This will check:
- ✅ Python packages installed
- ✅ .env file configured
- ✅ Snowflake connection working

### Verify .env File

```bash
# Show your configuration (passwords hidden)
cat .env | grep -v PASSWORD
```

Should show:
```
SNOWFLAKE_ACCOUNT=...
SNOWFLAKE_USER=...
SNOWFLAKE_AUTHENTICATOR=externalbrowser
SNOWFLAKE_WAREHOUSE=...
SNOWFLAKE_DATABASE=PRODDB
SNOWFLAKE_SCHEMA=PUBLIC
SNOWFLAKE_ROLE=...
```

### Test Connection Manually

```bash
python -c "
from snowflake_connector import SnowflakeConnector
sf = SnowflakeConnector()
if sf.connect():
    print('SUCCESS')
    sf.close()
else:
    print('FAILED')
"
```

## 📚 Need More Help?

- Check **SETUP_FOR_SSO.md** for SSO setup instructions
- Check **README.md** for detailed documentation
- Run **test_connection.py** for diagnostic
- Run **quick_test.py** to test with your actual query

