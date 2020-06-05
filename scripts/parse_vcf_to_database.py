"""
Description: Script to parse a VCF file and store selected variants in a database.
Author: Anne Manders
Date: 3-06-2020
Version: 0.1
"""

import vcf
import mysql.connector as connector

# TODO vcf file will be retrieved from the webpage, in the future
vcf_file = '/home/anne/Desktop/Data_integratie/gnomad.exomes.r2.1.1.sites.Y.vcf'


def process_file(vcf_file):
    """Accepts a file path to a VCF file and saved all the variants that qualify in a database.

    :param vcf_file. A string containing the path to a VCF file, obtained from the webpage.

    :return: None
    """
    vcf_reader = vcf.Reader(open(vcf_file, 'r'))
    conn = create_connection()
    cursor = conn.cursor()

    for record in vcf_reader:
        try:
            chromosome = record.CHROM
            position = record.POS
            variant_id = record.ID
            reference = record.REF[0]
            alternative = record.ALT[0].sequence
            variant_type = record.ALT[0].type

            # To determine the cancer alternative allele frequency
            alt_count = record.INFO['AC'][0]
            non_cancer_alt_count = record.INFO['non_cancer_AC'][0]
            all_alleles = record.INFO['AN']
            cancer_alt_frequency = (alt_count - non_cancer_alt_count) / all_alleles

            if cancer_alt_frequency > 0:
                values = (variant_id, chromosome, position, reference, alternative, variant_type, cancer_alt_frequency)

                query = "INSERT INTO variant VALUES {}".format(values)

                cursor.execute(query)

        except KeyError:
            # In case one of the attributes is missing
            pass

        except connector.errors.ProgrammingError:
            # In case one of the attributes is None
            pass

        except connector.errors.IntegrityError:
            # In case the database has trailing data
            pass

        except ZeroDivisionError:
            # In case variants have a total allele count of zero
            pass

    cursor.close()
    conn.commit()
    close_connection(conn)


def create_connection():
    """Makes a connection to the database and returns the created connection. # cursor

    :return A connection to the database.
    """
    connection = connector.connect(host='127.0.0.1', db='data_integratie', user='root', password='####')
    # host is 'localhost'/'127.0.0.1' when running the script locally
    # db is the name of the database (I named it data_integratie when creating it)
    # user is i.a.c. 'root' when running the script locally, how this will work in Docker, I'm not yet sure
    # password is the password for your mysql account

    return connection


def close_connection(connection):
    """Closes the established connection to the database.

    :param connection: A object containing the connection to the database.
    """
    connection.close()