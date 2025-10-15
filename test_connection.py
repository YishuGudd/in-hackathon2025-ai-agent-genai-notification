"""
Test Snowflake Connection
Quick script to verify your Snowflake setup is working correctly
"""

import os
import sys
from snowflake_connector import SnowflakeConnector


def test_environment():
    """Test if environment variables are set"""
    print("🔍 Checking environment variables...")
    print("-" * 60)
    
    required_vars = [
        'SNOWFLAKE_ACCOUNT',
        'SNOWFLAKE_USER',
        'SNOWFLAKE_PASSWORD',
        'SNOWFLAKE_WAREHOUSE',
        'SNOWFLAKE_DATABASE',
        'SNOWFLAKE_SCHEMA',
        'SNOWFLAKE_ROLE'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith('your_'):
            missing_vars.append(var)
            print(f"❌ {var}: Not configured")
        else:
            # Show only first 3 chars for security
            display_value = value[:3] + "***" if len(value) > 3 else "***"
            print(f"✅ {var}: {display_value}")
    
    print()
    
    if missing_vars:
        print("⚠️  Please configure the following variables in your .env file:")
        for var in missing_vars:
            print(f"   - {var}")
        print()
        return False
    
    print("✅ All environment variables are configured!")
    print()
    return True


def test_connection():
    """Test Snowflake connection"""
    print("🔌 Testing Snowflake connection...")
    print("-" * 60)
    
    try:
        sf = SnowflakeConnector()
        if sf.connect():
            print("✅ Successfully connected to Snowflake!")
            print()
            
            # Get connection details
            print("📊 Connection Details:")
            print("-" * 60)
            query = """
            SELECT 
                CURRENT_DATABASE() as database,
                CURRENT_SCHEMA() as schema,
                CURRENT_WAREHOUSE() as warehouse,
                CURRENT_ROLE() as role,
                CURRENT_USER() as user,
                CURRENT_VERSION() as version
            """
            df = sf.query_to_dataframe(query)
            
            for col in df.columns:
                print(f"{col.upper()}: {df[col].iloc[0]}")
            
            print()
            
            # Test query execution
            print("🧪 Testing query execution...")
            print("-" * 60)
            test_query = "SELECT 1 as test_value, 'Hello Snowflake!' as message"
            result = sf.query_to_dataframe(test_query)
            print(f"Test query result: {result['MESSAGE'].iloc[0]}")
            print("✅ Query execution successful!")
            print()
            
            sf.close()
            return True
        else:
            print("❌ Failed to connect to Snowflake")
            print("Please check your credentials and network connection")
            print()
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {str(e)}")
        print()
        print("Common issues:")
        print("  1. Incorrect account identifier")
        print("  2. Wrong username or password")
        print("  3. Warehouse is suspended or doesn't exist")
        print("  4. Network connectivity issues")
        print("  5. IP not whitelisted in Snowflake")
        print()
        return False


def test_packages():
    """Test if required packages are installed"""
    print("📦 Checking Python packages...")
    print("-" * 60)
    
    packages = [
        'snowflake.connector',
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'plotly',
        'dotenv'
    ]
    
    all_installed = True
    for package in packages:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Not installed")
            all_installed = False
    
    print()
    
    if not all_installed:
        print("⚠️  Some packages are missing. Run:")
        print("   pip install -r requirements.txt")
        print()
        return False
    
    print("✅ All required packages are installed!")
    print()
    return True


def main():
    """Run all tests"""
    print()
    print("=" * 60)
    print("Snowflake Connection Test")
    print("=" * 60)
    print()
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print()
        print("Please create a .env file:")
        print("  1. Copy .env.example to .env")
        print("     cp .env.example .env")
        print("  2. Edit .env with your Snowflake credentials")
        print()
        sys.exit(1)
    
    # Run tests
    tests_passed = 0
    tests_total = 3
    
    if test_packages():
        tests_passed += 1
    
    if test_environment():
        tests_passed += 1
    
    if test_connection():
        tests_passed += 1
    
    # Summary
    print("=" * 60)
    print(f"Test Results: {tests_passed}/{tests_total} passed")
    print("=" * 60)
    print()
    
    if tests_passed == tests_total:
        print("🎉 All tests passed! Your setup is ready to use.")
        print()
        print("Next steps:")
        print("  1. Open the Jupyter notebook:")
        print("     jupyter notebook data_analytics.ipynb")
        print()
        print("  2. Or run the example analysis:")
        print("     python example_analysis.py")
        print()
    else:
        print("⚠️  Some tests failed. Please fix the issues above and try again.")
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()

