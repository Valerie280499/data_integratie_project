"""
Description: connect_to_mysql_database.py, This file is
             responsible for the interaction with the database.
Author: Valerie Verhalle
Date: 11-6-2020
Version: 8
"""

import logging
import mysql
import mysql.connector as connector
from mysql.connector import Error

logger = logging.getLogger('database connector')
logging.info('Start connecting...')
logger.setLevel(logging.DEBUG)


class DatabaseInterface:
    """ This class can:
            create a database connection
            :return the database connection
            :return the cursor
            execute a query
            fetch all records from the cursor
            commit a query to the database
            close the database connection.
    """
    def __init__(self):
        self.conn = mysql.connector.connection_cext
        self.cursor = mysql.connector.cursor_cext

    def create_connection(self):
        try:
            logger.info("create connection")
            # Create database connection
            self.conn = connector.connect(host='localhost',
                                          db='data_integratie',
                                          user='root',
                                          password='Annesql')

            # Check if connected
            if self.conn.is_connected():
                logger.info("create cursor")
                # Create the cursor
                self.cursor = self.conn.cursor()

        except Error as e:
            # when a error occurs, return an error and exit the code
            logger.error("Error while connecting to MySQL ", e)
            exit()

    def get_connection(self):
        return self.conn

    def get_cursor(self):
        return self.cursor

    def execute_query(self, query):
        logger.info("executing query")

        # Execute the given query
        self.cursor.execute(query)

    def fetch_all(self):
        logger.info("fetch all")

        # Fetch all the records from the cursor
        record = self.cursor.fetchall()
        return record

    def commit_query(self):
        logger.info("commit query")

        # Commit the query
        self.conn.commit()

    def close_connection(self):
        logger.info("closing connection and cursor")

        # Close the cursor
        self.cursor.close()

        # Close the connection with the database
        self.conn.close()
