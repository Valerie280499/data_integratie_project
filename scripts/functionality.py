import os
import pandas
from scripts.connect_to_mysql_database import DatabaseInterface


def check_extension_of_input_file(vcf_file):
    if os.path.splitext(vcf_file.filename)[1].lower() == '.vcf':
        return True


def parse_all_data_from_database_to_data_frame():
    db_interface = DatabaseInterface()
    db_interface.create_connection()
    conn = db_interface.get_connection()

    data_frame = pandas.read_sql("SELECT * FROM variant;", conn)
    return data_frame
