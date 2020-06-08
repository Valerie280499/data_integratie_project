from Database.connect_to_mysql_database import DatabaseInterface


def create_database_record(query):
    try:
        db_interface = DatabaseInterface()
        db_interface.create_connection()
        db_interface.execute_query(query)
        record = db_interface.fetch_all()

        return record

    finally:
        db_interface.close_connection()


def check_if_database_is_empty():
    query = "SELECT * FROM variant;"
    record = create_database_record(query)

    if record is None:
        return False
