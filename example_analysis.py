"""
Example Data Analysis Script
Demonstrates how to use the Snowflake connector to perform basic analytics
"""

from snowflake_connector import SnowflakeConnector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    """Main function to run the analysis"""
    
    print("=" * 60)
    print("Snowflake Data Analytics Example")
    print("=" * 60)
    print()
    
    # Initialize and connect
    print("📡 Connecting to Snowflake...")
    with SnowflakeConnector() as sf:
        print("✅ Connected successfully!")
        print()
        
        # Example 1: Get current database info
        print("📊 Current Database Context:")
        print("-" * 60)
        query = """
        SELECT 
            CURRENT_DATABASE() as database,
            CURRENT_SCHEMA() as schema,
            CURRENT_WAREHOUSE() as warehouse,
            CURRENT_ROLE() as role,
            CURRENT_USER() as user,
            CURRENT_TIMESTAMP() as timestamp
        """
        df_info = sf.query_to_dataframe(query)
        print(df_info.to_string(index=False))
        print()
        
        # Example 2: List available tables
        print("📋 Available Tables:")
        print("-" * 60)
        try:
            tables = sf.list_tables()
            if len(tables) > 0:
                print(f"Found {len(tables)} tables:")
                # Show first few columns
                display_cols = [col for col in tables.columns if col in ['name', 'database_name', 'schema_name', 'rows']]
                if display_cols:
                    print(tables[display_cols].head(10).to_string(index=False))
                else:
                    print(tables.head(10).to_string(index=False))
            else:
                print("No tables found in current schema")
        except Exception as e:
            print(f"Could not list tables: {e}")
        print()
        
        # Example 3: Sample query (uncomment and modify for your data)
        # print("🔍 Running Sample Query:")
        # print("-" * 60)
        # query = """
        # SELECT 
        #     column1,
        #     column2,
        #     COUNT(*) as count
        # FROM your_table
        # GROUP BY column1, column2
        # ORDER BY count DESC
        # LIMIT 10
        # """
        # df = sf.query_to_dataframe(query)
        # print(df.to_string(index=False))
        # print()
        
        # # Example 4: Create a simple visualization
        # print("📈 Creating Visualization...")
        # plt.figure(figsize=(10, 6))
        # df['column1'].value_counts().head(10).plot(kind='barh')
        # plt.title('Top 10 Categories')
        # plt.xlabel('Count')
        # plt.ylabel('Category')
        # plt.tight_layout()
        # plt.savefig('analysis_chart.png', dpi=300, bbox_inches='tight')
        # print("✅ Chart saved as 'analysis_chart.png'")
        # print()
        
        # # Example 5: Export data
        # print("💾 Exporting Results...")
        # df.to_csv('analysis_results.csv', index=False)
        # print("✅ Results saved as 'analysis_results.csv'")
        # print()
        
        print("=" * 60)
        print("✅ Analysis Complete!")
        print("=" * 60)


if __name__ == "__main__":
    main()

