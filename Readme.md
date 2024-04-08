# Usgae

## Create database

initialize the database structure by running

`mysql -u <username> -p database < assets/create_db.sql`

then, we start to push the data into the database, the first step is to download the original csv data from google drive, and put all the csv in one folder, let's call it
`./data`. the next step is to set the config `data_dir=./data`, and lastly, run the data pushing script: `assets/push_data.py`


## Python SQL Connector

Currently support Google Cloud SQL connector and Local SQL connector

To use either connector, you need to include the `sql_server.ini` in your project root directory, the skeleton can be find in `sql_server_template.ini` and write the config to meet your demand

### Local SQL Connector
write the config, then enjoy!
```python
from utils import LocalSQL

db_manager = LocalSQL()

insert_query = "INSERT INTO album (AlbumTitle, ReleaseDate) VALUES (%s, %s)"
db_manager.execute(insert_query, ("Time", "1973"))
db_manager.commit()
```

### Google Cloud Connector
> We will use local sql connection for our project, so just ignore this part


**Step1: install google cloud CLI**: https://cloud.google.com/sdk/docs/install

**Step2: login your google account**: in your terminal, run command below to login your google account:


```bash
gcloud auth application-default login
```

**Step3: run SQL API**

run `examples/execute_sql.py`

