# Usage

## Setup Virtual Environment

```
pip install pipenv
pipenv install
```

## Create database

initialize the database structure by running

`mysql -u <username> -p database < assets/create_db.sql`

## Push data into database
- Firstly, create a new config file called `sql_server.ini`,copy paste template from   `sql_server_template.ini`, set the config `dir=./assets/data` in `[data]` section (don't leave space between characters)
- fill `[local_sql]` section with information about your database 
- Secondly, save and run the `push_data.py` in utils file



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

