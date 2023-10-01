'''
Database connection configurations
'''
import os

from utils.db import DBConnection


# Get database connection credentials from environment variables used by extract_load
def get_warehouse_creds() -> DBConnection:
    return DBConnection(
        user=os.getenv("POSTGRES_USER", ""),
        password=os.getenv("POSTGRES_PASSWORD", ""),
        db=os.getenv("WAREHOUSE_DB", ""),
        host=os.getenv("WAREHOUSE_HOST", ""),
        port=int(os.getenv("WAREHOUSE_PORT", 5432)),
    )
