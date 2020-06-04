import pyodbc


def connect_to_database():
    connection = pyodbc.connect('Driver={SQL Server};'
                                'Server=server_name;'
                                'Database=db_name;'
                                'Trusted_Connection=yes;')

    cursor = connection.cursor()
    return cursor, connection


def update_new_vcf_to_database(cursor, connection):
    cursor.execute('UPDATE Database_Name.Table_Name '
                   'SET Column1_Name = value1, '
                   '    Column2_Name = value2, '
                   'WHERE condition')

    connection.commit()
    return 'new vcf updated to database'


def get_everything_from_database(cursor):
    cursor.execute('SELECT * FROM db_name.Table')

    for row in cursor:
        return row

