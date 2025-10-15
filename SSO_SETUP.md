# Snowflake SSO Configuration Guide

## Finding Your Snowflake Credentials

### 1. Find Your Snowflake Account Identifier

When you log in to Snowflake via SSO, look at the URL in your browser:

```
https://[ACCOUNT_IDENTIFIER].snowflakecomputing.com
```

**Example URLs:**
- `https://abc12345.us-east-1.snowflakecomputing.com` → Account: `abc12345.us-east-1`
- `https://mycompany.snowflakecomputing.com` → Account: `mycompany`

The account identifier is everything before `.snowflakecomputing.com`

### 2. Find Your Username

In Snowflake web UI:
1. Click on your profile (top right corner)
2. Your username is displayed there
3. Usually it's your email prefix or company username

### 3. Find Your Current Context

Once logged into Snowflake web UI, run these queries to see your current settings:

```sql
-- Get your current context
SELECT 
    CURRENT_USER() as username,
    CURRENT_ROLE() as role,
    CURRENT_DATABASE() as database,
    CURRENT_SCHEMA() as schema,
    CURRENT_WAREHOUSE() as warehouse,
    CURRENT_ACCOUNT() as account;

-- List available warehouses
SHOW WAREHOUSES;

-- List available databases
SHOW DATABASES;
```

## SSO Configuration for Python

### Option 1: Using .env file (Recommended)

Create/edit your `.env` file:

```bash
# Snowflake SSO Configuration
SNOWFLAKE_ACCOUNT=abc12345.us-east-1
SNOWFLAKE_USER=your.email@company.com
SNOWFLAKE_AUTHENTICATOR=externalbrowser
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=PRODDB
SNOWFLAKE_SCHEMA=PUBLIC
SNOWFLAKE_ROLE=YOUR_ROLE

# Note: No password needed for SSO!
```

### Option 2: Direct Configuration in Code

```python
from snowflake_connector import SnowflakeConnector

config = {
    'account': 'abc12345.us-east-1',
    'user': 'your.email@company.com',
    'authenticator': 'externalbrowser',  # This enables SSO
    'warehouse': 'COMPUTE_WH',
    'database': 'PRODDB',
    'schema': 'PUBLIC',
    'role': 'YOUR_ROLE'
}

sf = SnowflakeConnector(config)
sf.connect()  # This will open your browser for SSO login
```

## Quick Test

After configuration, test with:

```bash
python test_connection.py
```

When you run this with SSO:
1. A browser window will open automatically
2. Log in through your company's SSO
3. Return to the terminal - connection established!

## Running Your Queries

Yes! You can run queries like:

```python
from snowflake_connector import SnowflakeConnector

with SnowflakeConnector() as sf:
    query = "SELECT * FROM PRODDB.PUBLIC.FACT_DEDUP_EXPERIMENT_EXPOSURE LIMIT 1"
    df = sf.query_to_dataframe(query)
    print(df)
```

## Troubleshooting SSO

### Browser doesn't open?
- Check if you have a default browser set
- Try running from a terminal with GUI access
- Ensure you're not in a remote/headless session

### Connection timeout?
- Complete the SSO login within 2 minutes
- Check if browser pop-ups are blocked

### Access denied?
- Verify your user has access to the specified warehouse/database
- Check with your Snowflake admin for proper role assignment

