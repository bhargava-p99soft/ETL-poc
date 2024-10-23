# ETL-POC

Note: this is semi-automated ETL pipeline. To make it work, first you need to set up a few things in advance in your snowflake account

Go to worksheets in your snowflake account, and run the below commands

create database with name "ETL_DB"

```CREATE OR REPLACE DATABASE ETL_DB;```

create schema with name "EXTERNAL_STAGES"

```CREATE OR REPLACE SCHEMA external_stages;```

stage with name "UNCLEANED_STAGE"

```CREATE OR REPLACE STAGE ETL_DB.external_stages.uncleaned_stage;```


Now upload people.csv in sample_data folder to UNCLEANED_STAGE

Now create two tables with names "uncleaned_data" and "cleaned_data"

```
CREATE OR REPLACE TABLE uncleaned_table (
    INDEX_ID INT,
    USER_ID VARCHAR(30),
    FIRST_NAME VARCHAR(50),
    LAST_NAME VARCHAR(30),
    SEX VARCHAR(30),
    EMAIL VARCHAR(100),
    PHONE VARCHAR(30),
    JOB_TITLE VARCHAR(200));

CREATE OR REPLACE TABLE cleaned_table (
    INDEX_ID INT,
    USER_ID VARCHAR(30),
    FIRST_NAME VARCHAR(50),
    LAST_NAME VARCHAR(30),
    SEX VARCHAR(30),
    EMAIL VARCHAR(100),
    PHONE VARCHAR(30),
    JOB_TITLE VARCHAR(200));

```


While testing the pipeline multiple times, below commands may be helpful

### To empty the tables

```Truncate Table UNCLEANED_TABLE;```
```Truncate Table CLEANED_TABLE;```


### To drop the tables

```DROP TABLE UNCLEANED_TABLE;```
```DROP TABLE CLEANED_TABLE;```

Finally to run the ETL pipeline, run the below command

```python main.py```
