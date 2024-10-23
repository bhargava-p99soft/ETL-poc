from utilities.formatter import format_value

from utilities.db_connector import get_sf_connection



def load_data(conn):
    # Create a cursor object
    cursor = conn.cursor()

    # Use COPY INTO to load data
    cursor.execute("""
        COPY INTO ETL_DB.EXTERNAL_STAGES.uncleaned_table
        FROM @ETL_DB.EXTERNAL_STAGES.UNCLEANED_STAGE
        FILE_FORMAT = (TYPE = 'CSV' field_delimiter=',' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER=1)
        ON_ERROR = CONTINUE;
    """)

    cursor.close()




# Step 3: Get Table Column Names from Snowflake
def get_snowflake_table_columns(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"DESCRIBE TABLE {table_name}")
    columns_info = cursor.fetchall()
    column_names = [col[0] for col in columns_info]
    cursor.close()
    return column_names

# Step 4: Load Cleaned Data into Snowflake with Explicit Column Names
def load_cleaned_data_to_snowflake(conn, df, table_name):

    conn =get_sf_connection()

    # Get the table's columns from Snowflake
    table_columns = get_snowflake_table_columns(conn, table_name)

    
    # Ensure the DataFrame has the same columns in the correct order
    if set(df.columns) != set(table_columns):
        missing_columns = set(table_columns) - set(df.columns)
        extra_columns = set(df.columns) - set(table_columns)
        if missing_columns:
            print(f"Error: Missing columns in DataFrame: {missing_columns}")
        if extra_columns:
            print(f"Warning: Extra columns in DataFrame will be ignored: {extra_columns}")
        # Reorder and filter the DataFrame to match the table schema
        df = df[table_columns]  # Order the columns as in the table

    # conn =get_sf_connection()

    cursor = conn.cursor()
    
    # Insert each row into the Snowflake table with explicit column names
    for i, row in df.iterrows():
        values = ', '.join([format_value(val) for val in row])
        insert_query = f"""
        INSERT INTO {table_name} ({', '.join(table_columns)}) VALUES ({values});
        """
        print(i)
        print(insert_query)
        cursor.execute(insert_query)
        
    
    conn.commit()
    cursor.close()