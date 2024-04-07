# Usgae

## Create database

`mysql -u <username> -p database < assets/create_db.sql`

## Use Python SQL Connector

Currently support Goole Cloud SQL connector and Local SQL connector

To use either connector, you need to include the `sql_server.ini` in your project root directory, the skeleton can be find in `sql_server_template.ini` and write the config to meet your demand
### Google Cloud Connector


**Step1: install google cloud CLI**: https://cloud.google.com/sdk/docs/install

**Step2: login your google account**: in your terminal, run command below to login your google account:


```bash
gcloud auth application-default login
```

**Step3: run SQL API**

run `examples/execute_sql.py`

### Local SQL Connector
write the config, then enjoy!