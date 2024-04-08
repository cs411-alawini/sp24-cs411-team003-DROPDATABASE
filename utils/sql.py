import os
import pymysql
from google.cloud.sql.connector import Connector, IPTypes
from .config_loader import Config
import sqlalchemy
import mysql.connector

config = Config().config


class GC_SQL:
    def __init__(self):
        ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC
        self.connector = Connector(ip_type)
        self.__engine = None
        self.connection = None  # This will hold the current connection

        def get_conn_callback():
            conn: pymysql.connections.Connection = self.connector.connect(
                config['google_cloud']['instance_connection_name'],
                "pymysql",
                user=config['google_cloud']['user'],
                password=config['google_cloud']['password'],
                db=config['google_cloud']['db_name'],
            )
            return conn

        try:
            self.__engine = sqlalchemy.create_engine(
                "mysql+pymysql://",
                creator=get_conn_callback,
                # ... (other parameters as needed)
            )
            self.connection = self.__engine.connect()
            print("Connection to the database was successful.")
        except Exception as e:
            print(f"Failed to connect to the database: {e}")
            raise e

    def execute(self, query, params=None):
        try:
            result = self.connection.execute(sqlalchemy.text(query), params)
            # For SELECT statements, fetch results
            if result.returns_rows:
                return result.fetchall()
            else:
                # For INSERT/UPDATE/DELETE, return affected rowcount
                return result.rowcount
        except Exception as e:
            print(f"Failed to execute query: {e}")
            self.connection.rollback()

    def commit(self):
        try:
            self.connection.commit()
            print("Transaction committed.")
        except Exception as e:
            print(f"Failed to commit transaction: {e}")

    def close(self):
        try:
            if self.connection:
                self.connection.close()
                print("Connection closed successfully.")
        except Exception as e:
            print(f"Failed to close the connection: {e}")
        finally:
            self.__engine.dispose()
            print("Engine disposed successfully.")


class LocalSQL:
    def __init__(self):
        self.__connection = None
        self.__cursor = None
        try:
            self.__connection = mysql.connector.connect(
                user=config['local_sql']['user'],
                password=config['local_sql']['password'],
                host=config['local_sql'].get('host', 'localhost'),
                database=config['local_sql']['db_name']
            )
            self.__cursor = self.__connection.cursor(dictionary=True)
        except mysql.connector.Error as err:
            print(f"Error connecting to the database: {err}")
            # Consider re-raising the exception or handling it as appropriate for your application

    def execute(self, query, params=None):
        if self.__cursor is None:
            print("Attempted to execute a query without a database connection.")
            return None
        try:
            self.__cursor.execute(query, params or ())
            return self.__cursor.fetchall()
        except mysql.connector.Error as err:
            raise err

    def commit(self):
        if self.__connection:
            self.__connection.commit()

    def rollback(self):
        if self.__connection:
            self.__connection.rollback()

    def close(self):
        if self.__cursor is not None:
            self.__cursor.close()
            self.__cursor = None
        if self.__connection is not None:
            self.__connection.close()
            self.__connection = None
