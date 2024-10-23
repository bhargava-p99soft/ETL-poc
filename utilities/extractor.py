from utilities.db_connector import get_sf_connection

import pandas as pd


def fetch_data_from_snowflake(conn):
    conn = get_sf_connection()
    
    query = "SELECT * FROM ETL_DB.EXTERNAL_STAGES.uncleaned_table LIMIT 10"
    df = pd.read_sql(query, conn)
    
    # conn.close()
    return df