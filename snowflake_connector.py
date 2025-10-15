"""
Snowflake Database Connector
Handles connection and query execution for Snowflake data warehouse
"""

import os
import pandas as pd
import snowflake.connector
from snowflake.connector import DictCursor
from dotenv import load_dotenv
from typing import Optional, Dict, Any, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SnowflakeConnector:
    """A class to manage Snowflake database connections and operations"""
    
    def __init__(self, config: Optional[Dict[str, str]] = None):
        """
        Initialize Snowflake connector
        
        Args:
            config: Dictionary with connection parameters. If None, loads from .env file
                   For SSO, include 'authenticator': 'externalbrowser'
        """
        if config is None:
            load_dotenv()
            self.config = {
                'account': os.getenv('SNOWFLAKE_ACCOUNT'),
                'user': os.getenv('SNOWFLAKE_USER'),
                'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
                'database': os.getenv('SNOWFLAKE_DATABASE'),
                'schema': os.getenv('SNOWFLAKE_SCHEMA'),
                'role': os.getenv('SNOWFLAKE_ROLE')
            }
            
            # Check for SSO/external browser authentication
            authenticator = os.getenv('SNOWFLAKE_AUTHENTICATOR')
            if authenticator and authenticator.lower() == 'externalbrowser':
                self.config['authenticator'] = 'externalbrowser'
                logger.info("Using SSO authentication (external browser)")
            else:
                # Only use password if not using SSO
                password = os.getenv('SNOWFLAKE_PASSWORD')
                if password:
                    self.config['password'] = password
        else:
            self.config = config
            
        self.connection = None
        self.cursor = None
        
    def connect(self) -> bool:
        """
        Establish connection to Snowflake
        Supports both password and SSO authentication
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Build connection parameters, only including non-None values
            conn_params = {
                'account': self.config['account'],
                'user': self.config['user'],
            }
            
            # Add optional parameters if they exist
            if self.config.get('warehouse'):
                conn_params['warehouse'] = self.config['warehouse']
            if self.config.get('database'):
                conn_params['database'] = self.config['database']
            if self.config.get('schema'):
                conn_params['schema'] = self.config['schema']
            if self.config.get('role'):
                conn_params['role'] = self.config['role']
            
            # Handle authentication
            if self.config.get('authenticator') == 'externalbrowser':
                conn_params['authenticator'] = 'externalbrowser'
                logger.info("Opening browser for SSO authentication...")
            elif self.config.get('password'):
                conn_params['password'] = self.config['password']
            
            self.connection = snowflake.connector.connect(**conn_params)
            self.cursor = self.connection.cursor()
            logger.info("Successfully connected to Snowflake")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Snowflake: {e}")
            return False
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[tuple]:
        """
        Execute a SQL query and return results
        
        Args:
            query: SQL query string
            params: Optional parameters for parameterized queries
            
        Returns:
            List of tuples containing query results
        """
        if not self.cursor or not self.connection:
            raise ConnectionError(
                "Not connected to Snowflake. Please call connect() first or use context manager."
            )
        
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            results = self.cursor.fetchall()
            logger.info(f"Query executed successfully, returned {len(results)} rows")
            return results
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    def query_to_dataframe(self, query: str, params: Optional[tuple] = None) -> pd.DataFrame:
        """
        Execute query and return results as pandas DataFrame
        
        Args:
            query: SQL query string
            params: Optional parameters for parameterized queries
            
        Returns:
            pandas DataFrame with query results
        """
        if not self.cursor or not self.connection:
            raise ConnectionError(
                "Not connected to Snowflake. Please call connect() first.\n"
                "For SSO: Make sure you completed the browser authentication!\n"
                "Example:\n"
                "  sf = SnowflakeConnector()\n"
                "  sf.connect()  # Browser will open for SSO\n"
                "  df = sf.query_to_dataframe(query)\n"
            )
        
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            # Fetch results and column names
            results = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            
            # Create DataFrame
            df = pd.DataFrame(results, columns=columns)
            logger.info(f"Query returned DataFrame with shape {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Failed to create DataFrame from query: {e}")
            raise
    
    def execute_from_file(self, filepath: str) -> List[tuple]:
        """
        Execute SQL query from a file
        
        Args:
            filepath: Path to SQL file
            
        Returns:
            Query results
        """
        try:
            with open(filepath, 'r') as f:
                query = f.read()
            return self.execute_query(query)
        except Exception as e:
            logger.error(f"Failed to execute query from file: {e}")
            raise
    
    def get_table_info(self, table_name: str) -> pd.DataFrame:
        """
        Get information about a table's structure
        
        Args:
            table_name: Name of the table
            
        Returns:
            DataFrame with column information
        """
        if not self.cursor or not self.connection:
            raise ConnectionError("Not connected to Snowflake. Please call connect() first.")
        
        query = f"DESCRIBE TABLE {table_name}"
        return self.query_to_dataframe(query)
    
    def list_tables(self, schema: Optional[str] = None) -> pd.DataFrame:
        """
        List all tables in the current database/schema
        
        Args:
            schema: Optional schema name, uses current schema if None
            
        Returns:
            DataFrame with table information
        """
        if not self.cursor or not self.connection:
            raise ConnectionError("Not connected to Snowflake. Please call connect() first.")
        
        if schema:
            query = f"SHOW TABLES IN SCHEMA {schema}"
        else:
            query = "SHOW TABLES"
        return self.query_to_dataframe(query)
    
    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("Snowflake connection closed")
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


# Example usage
if __name__ == "__main__":
    # Example 1: Using context manager (recommended)
    with SnowflakeConnector() as sf:
        # List all tables
        tables = sf.list_tables()
        print("Available tables:")
        print(tables)
        
        # Execute a sample query
        # query = "SELECT * FROM your_table LIMIT 10"
        # df = sf.query_to_dataframe(query)
        # print(df.head())
    
    # Example 2: Manual connection management
    # sf = SnowflakeConnector()
    # if sf.connect():
    #     df = sf.query_to_dataframe("SELECT CURRENT_TIMESTAMP()")
    #     print(df)
    #     sf.close()

