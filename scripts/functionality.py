import os
import allel
import pandas
from werkzeug.utils import secure_filename
from Database.connect_to_mysql_database import DatabaseInterface


def check_ext(vcf_file):
    if os.path.splitext(vcf_file.filename)[1].lower() == '.vcf':
        return True


def save_input_file(vcf_file):
    vcf_file.save(secure_filename('input_file'))


def vcf_to_dataframe():
    return allel.vcf_to_dataframe('input_file', fields='*', alt_number=2)


def parse_all_data_from_database_to_data_frame():
    db_interface = DatabaseInterface()
    db_interface.create_connection()
    conn = db_interface.get_connection()

    data_frame = pandas.read_sql("SELECT * FROM variant;", conn)
    return data_frame
