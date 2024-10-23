import snowflake.connector

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