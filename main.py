
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

        

    # # Step 4: Main Execution
    # if __name__ == "__main__":

    #     conn = get_sf_connection()

    #     cursor = conn.cursor()
    #     # # Fetch data from Snowflake
    #     # data = fetch_data_from_snowflake(conn)
        
    #     # # Find and impute anomalies
    #     # cleaned_data = impute_anomalies(data)
        
    #     # # Load cleaned data to a new Snowflake table
    #     # load_cleaned_data_to_snowflake(conn, cleaned_data, "my_cleaned_table")
        
    #     # print("Cleaned data has been loaded to 'my_cleaned_table'.")
    #     query = "SELECT * FROM OUR_FIRST_DB.PUBLIC.ORDERS LIMIT 10;"
    #     df = pd.read_sql(query, conn)
    #     print(df)
    #     returned_df = impute_anomalies(df)
    #     # query = "SELECT * FROM OUR_FIRST_DB.PUBLIC.ORDERS LIMIT 10;"
    #     # df = pd.read_sql(query, conn)
    #     print(returned_df)
    except Exception as e:
        raise e
    # end try
    