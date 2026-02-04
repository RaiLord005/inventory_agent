import mysql.connector
from mysql.connector import Error

def get_connection():
    """
    Creates a central connection to the MySQL Warehouse database.
    Update the user and password to match your MySQL settings.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='',         # Your MySQL username
            password='', # Your MySQL password
            database=''
        )
        if connection.is_connected():
            return connection

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None
