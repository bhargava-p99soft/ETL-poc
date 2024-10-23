
import pandas as pd
  
from utilities.db_connector import get_sf_connection
from utilities.data_cleaner import impute_anomalies
from utilities.data_loader import load_data, load_cleaned_data_to_snowflake
from utilities.extractor import fetch_data_from_snowflake

if __name__ == "__main__":

    try:
        # comment: 

        conn =get_sf_connection()
        cursor = conn.cursor()
        #  Load uncleaned data
        load_data(conn)
        print(conn)
        # fetch data from uncleaned table
        uncleaned_data = fetch_data_from_snowflake(conn)
        print(uncleaned_data)

        # # Find and impute anomalies

        cleaned_data = impute_anomalies(uncleaned_data)

        print("data cleaned")

        load_cleaned_data_to_snowflake(conn, cleaned_data, "ETL_DB.EXTERNAL_STAGES.cleaned_table")

        
    except Exception as e:
        raise e
    # end try
    