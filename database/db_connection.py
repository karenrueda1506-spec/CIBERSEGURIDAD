# database/db_connection.py
import mysql.connector
from mysql.connector import Error
from app.config import config

class DatabaseConnection:
    def __init__(self):
        self.host = config.DB_HOST
        self.database = config.DB_NAME
        self.user = config.DB_USER
        self.password = config.DB_PASSWORD
        self.port = config.DB_PORT
        self.connection = None
    
    def get_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            return self.connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()