import pandas as pd

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
        # Escape single quotes by replacing ' with ''
        escaped_value = value.replace("'", "''")
        return f"'{escaped_value}'"
    else:
        return str(value)
