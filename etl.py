import snowflake.connector
import pandas as pd
from sklearn.ensemble import IsolationForest
from fancyimpute import KNN  # KNN Imputation for missing/incorrect values

db_config = {
    "user": "bhargavap99",
    "password": "'xkMTd'rqrx7gq,",
    "account": "xz76745.ap-south-1.aws"
}

def get_sf_connection():
    conn = snowflake.connector.connect(
        user= db_config["user"],
        password=db_config["password"],
        account=db_config['account']
    )

    return conn    


def load_data(conn):
    # Create a cursor object
    cursor = conn.cursor()

    # Use COPY INTO to load data
    cursor.execute("""
        COPY INTO my_database.my_schema.my_table
        FROM @my_stage
        FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"');
    """)

    # Close the cursor and connection
    cursor.close()
    conn.close()


# Step 1: Fetch Data from Snowflake
def fetch_data_from_snowflake(conn):
    # conn = get_sf_connection()
    
    query = "SELECT * FROM my_database.my_schema.my_table"
    df = pd.read_sql(query, conn)
    
    conn.close()
    return df

# Step 2: Find and Impute Anomalies using KNN
def impute_anomalies(df):
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    isolation_forest = IsolationForest(contamination=0.05)
    df['anomaly_isolation_forest'] = isolation_forest.fit_predict(numeric_df)

    anomalous_rows = df['anomaly_isolation_forest'] == -1
    numeric_df_cleaned = numeric_df.copy()
    numeric_df_cleaned[anomalous_rows] = float('nan')

    # KNN Imputation
    numeric_df_imputed = pd.DataFrame(KNN(k=5).fit_transform(numeric_df_cleaned), columns=numeric_df.columns)
    df.update(numeric_df_imputed)

    return df

# Step 3: Load Cleaned Data to a New Table in Snowflake
def load_cleaned_data_to_snowflake(conn, df, table_name):
    # conn = get_sf_connection()
    cursor = conn.cursor()

    # Create the new table if it doesn't exist
    create_table_query = f"""
    CREATE OR REPLACE TABLE {table_name} (
        {', '.join([f'{col} {get_column_type(df[col])}' for col in df.columns])}
    );
    """
    cursor.execute(create_table_query)
    
    # Insert data row by row into the new table
    for i, row in df.iterrows():
        insert_query = f"""
        INSERT INTO {table_name} VALUES ({', '.join([format_value(val) for val in row])});
        """
        cursor.execute(insert_query)

    conn.commit()
    cursor.close()
    conn.close()

# Utility functions
def get_column_type(column):
    if column.dtype == 'int64':
        return 'INTEGER'
    elif column.dtype == 'float64':
        return 'FLOAT'
    elif column.dtype == 'object':
        return 'STRING'
    else:
        return 'STRING'  # Fallback for unsupported types

def format_value(value):
    if pd.isnull(value):
        return 'NULL'
    elif isinstance(value, str):
        return f"'{value}'"
    else:
        return str(value)

# Step 4: Main Execution
if __name__ == "__main__":

    conn = get_sf_connection()

    cursor = conn.cursor()
    # # Fetch data from Snowflake
    # data = fetch_data_from_snowflake(conn)
    
    # # Find and impute anomalies
    # cleaned_data = impute_anomalies(data)
    
    # # Load cleaned data to a new Snowflake table
    # load_cleaned_data_to_snowflake(conn, cleaned_data, "my_cleaned_table")
    
    # print("Cleaned data has been loaded to 'my_cleaned_table'.")
    query = "SELECT * FROM OUR_FIRST_DB.PUBLIC.ORDERS LIMIT 10;"
    df = pd.read_sql(query, conn)
    print(df)
    returned_df = impute_anomalies(df)
    # query = "SELECT * FROM OUR_FIRST_DB.PUBLIC.ORDERS LIMIT 10;"
    # df = pd.read_sql(query, conn)
    print(returned_df)