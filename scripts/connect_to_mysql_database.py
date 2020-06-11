import logging
import mysql
import mysql.connector as connector
from mysql.connector import Error

logger = logging.getLogger('database connector')
logging.info('Start connecting...')
logger.setLevel(logging.DEBUG)


class DatabaseInterface:

    def __init__(self):
        self.conn = mysql.connector.connection_cext
        self.cursor = mysql.connector.cursor_cext

    def create_connection(self):
        try:
            logger.info("create connection")
            self.conn = connector.connect(host='localhost',
                                          db='data_integratie',
                                          user='root',
                                          password='Annesql')

            if self.conn.is_connected():
                logger.info("create cursor")
                self.cursor = self.conn.cursor()

        except Error as e:
            logger.error("Error while connecting to MySQL ", e)
            exit()

    def get_connection(self):
        return self.conn

    def get_cursor(self):
        return self.cursor

    def execute_query(self, query):
        logger.info("executing query")
        self.cursor.execute(query)

    def fetch_all(self):
        logger.info("fetch all")
        record = self.cursor.fetchall()
        return record

    def commit_query(self):
        logger.info("commit query")
        self.conn.commit()

    def close_connection(self):
        logger.info("closing connection and cursor")
        self.cursor.close()
        self.conn.close()
