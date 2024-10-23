# import pandas as pd
# from sklearn.ensemble import IsolationForest
# from fancyimpute import KNN  # KNN Imputation for missing/incorrect values


# def impute_anomalies(df):
#     numeric_df = df.select_dtypes(include=['float64', 'int64'])
#     isolation_forest = IsolationForest(contamination=0.05)
#     df['anomaly_isolation_forest'] = isolation_forest.fit_predict(numeric_df)

#     anomalous_rows = df['anomaly_isolation_forest'] == -1
#     numeric_df_cleaned = numeric_df.copy()
#     numeric_df_cleaned[anomalous_rows] = float('nan')

#     # KNN Imputation
#     numeric_df_imputed = pd.DataFrame(KNN(k=5).fit_transform(numeric_df_cleaned), columns=numeric_df.columns)
#     df.update(numeric_df_imputed)

#     return df


import pandas as pd
import numpy as np
from fuzzywuzzy import process
# from collections import Counter
from fancyimpute import KNN  # For numeric imputation

# Step 1: Detect and Impute Anomalies for String Columns
def impute_string_anomalies(df, string_columns):
    for column in string_columns:
        # Get the most common value in the column
        most_common_value = df[column].mode()[0]

        # Replace missing values with the most common value
        df[column].fillna(most_common_value, inplace=True)

        # Use fuzzy matching to find and fix anomalies (potential typos)
        unique_values = df[column].dropna().unique()
        
        # Correct values that don't match the most common values
        for val in unique_values:
            # print("processing columns")
            if val != most_common_value:
                match, score = process.extractOne(val, unique_values)
                if score < 90:  # Threshold for fuzzy matching (adjustable)
                    df[column] = df[column].replace(val, most_common_value)

    return df

# Step 2: Detect and Impute Anomalies for Numeric Columns
def impute_numeric_anomalies(df):
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    numeric_df_imputed = pd.DataFrame(KNN(k=5).fit_transform(numeric_df), columns=numeric_df.columns)
    df.update(numeric_df_imputed)
    return df

# Step 3: Main Function to Impute Anomalies in Both String and Numeric Columns
def impute_anomalies(df):
    # Separate string and numeric columns
    string_columns = df.select_dtypes(include=['object']).columns.tolist()
    
    # Impute string anomalies
    df = impute_string_anomalies(df, string_columns)
    
    # Impute numeric anomalies
    df = impute_numeric_anomalies(df)
    
    return df

# # Example Usage
# df = pd.DataFrame({
#     'name': ['John', 'Jon', 'Jonn', 'Jane', None, 'Jon', 'John'],
#     'age': [25, 28, 27, np.nan, 22, 29, 30],
#     'city': ['New York', 'NewYork', 'new york', 'London', 'London', 'New York', None]
# })

# # Impute anomalies in the DataFrame
# cleaned_df = impute_anomalies(df)
# print(cleaned_df)