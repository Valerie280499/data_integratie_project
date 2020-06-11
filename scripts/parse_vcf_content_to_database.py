"""
Description: Script to parse a VCF file and store selected variants in a database.
Author: Anne Manders
Date: 3-06-2020
Version: 0.1
"""
import vcf
import logging
import mysql.connector as connector
from scripts.connect_to_mysql_database import DatabaseInterface


logger = logging.getLogger('database connector')
logging.info('Start connecting...')
logger.setLevel(logging.DEBUG)


def upload_vcf_content(vcf_file):
    """Accepts a file path to a VCF file and saved all the variants that qualify in a database.

    :param vcf_file. A string containing the path to a VCF file, obtained from the webpage.

    :return: None
    """

    data_interface = DatabaseInterface()
    data_interface.create_connection()
    a_query_was_committed = False

    vcf_reader = vcf.Reader(open(vcf_file.filename, 'r'))

    for record in vcf_reader:

        try:
            # To determine the cancer alternative allele frequency
            alt_count = record.INFO['AC'][0]
            non_cancer_alt_count = record.INFO['non_cancer_AC'][0]
            all_alleles = record.INFO['AN']
            cancer_alt_frequency = (alt_count - non_cancer_alt_count) / all_alleles

            if cancer_alt_frequency > 0:
                chromosome = record.CHROM
                position = record.POS
                variant_id = record.ID
                reference = record.REF[0]
                alternative = record.ALT[0].sequence
                variant_type = record.ALT[0].type

                a_query_was_committed = True
                values = (variant_id, chromosome, position, reference, alternative, variant_type, cancer_alt_frequency)
                query = "INSERT INTO variant VALUES {}".format(values)
                data_interface.execute_query(query)
                data_interface.commit_query()

        except KeyError:
            # One of the attributes is missing
            pass

        except connector.errors.ProgrammingError:
            # One of the attributes is None
            pass

        except connector.errors.IntegrityError:
            # The database has trailing data
            pass

        except ZeroDivisionError:
            # The variants have a total allele count of zero
            pass

        except Exception as error:
            logging.error(error)
            return False

    data_interface.close_connection()
    if a_query_was_committed:
        return True
    else:
        logger.error("no data was commited to the database because the input did not pass the criteria")
        return False
