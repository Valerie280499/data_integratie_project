from scripts.connect_to_mysql_database import DatabaseInterface


def create_database_record(query):
    db_interface = DatabaseInterface()

    try:
        db_interface.create_connection()
        db_interface.execute_query(query)
        record = db_interface.fetch_all()
        return record

    finally:
        db_interface.close_connection()


def check_if_database_is_not_empty():
    query = "SELECT * FROM variant;"
    record = create_database_record(query)

    if record is None:
        return False
    else:
        return True


def extract_all_data_from_database():
    query = "SELECT * FROM variant;"
    record = create_database_record(query)

    return record


