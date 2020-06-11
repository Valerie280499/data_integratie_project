"""
Description: extract_data_from_database.py, executes query's
Author: Valerie Verhalle
Date: 11-6-2020
Version: 8
"""

from scripts.connect_to_mysql_database import DatabaseInterface


def create_database_record(query):
    """ This function will create an database connection, execute a query, close the databse connection
    using the imported script above, and create a record based on the query it receives.

    :param query. Containing the query to be executed.
    :return record. Containing the query output.
    """

    db_interface = DatabaseInterface()

    try:
        db_interface.create_connection()
        db_interface.execute_query(query)
        record = db_interface.fetch_all()
        return record

    finally:
        db_interface.close_connection()


def check_if_database_is_not_empty():
    """ This function holds the query to check if the database has any content.
    It will pass this query to the 'create_database_record', and perform a check on the returned record.

    :return False. When the received record is None.
    :return True. When the received record is not None.
    """

    query = "SELECT * FROM variant;"
    record = create_database_record(query)

    if record is None:
        return False
    else:
        return True


def extract_all_data_from_database():
    """ This function holds the query to extract all the available data from the
    database and will return the record, received from the first explained function above.

    :return record. Query output.
    """

    query = "SELECT * FROM variant;"
    record = create_database_record(query)

    return record


