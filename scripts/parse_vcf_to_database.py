"""
Description: Script to parse a VCF file and store selected variants in a database.
Author: Anne Manders
Date: 3-06-2020
Version: 0.1
"""
from Database.connect_to_mysql_database import DatabaseInterface
import logging
import mysql.connector as connector

logger = logging.getLogger('database connector')
logging.info('Start connecting...')
logger.setLevel(logging.DEBUG)

# TODO vcf file will be retrieved from the webpage, in the future
vcf_file = '/home/anne/Desktop/Data_integratie/gnomad.exomes.r2.1.1.sites.Y.vcf'


def process_file(vcf_reader):
    """Accepts a file path to a VCF file and saved all the variants that qualify in a database.

    :param vcf_file. A string containing the path to a VCF file, obtained from the webpage.

    :return: None
    """

    data_interface = DatabaseInterface()
    data_interface.create_connection()

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
                data_interface.execute_query(query)
            else:
                pass

        except KeyError:
            # error_message = "One of the attributes is missing"
            pass

        except connector.errors.ProgrammingError:
            # error_message = "One of the attributes is None"
            pass

        except connector.errors.IntegrityError:
            # error_message = "The database has trailing data"
            pass

        except ZeroDivisionError:
            # error_message = "The variants have a total allele count of zero"
            pass

        except Exception as e:
            logging.error(e)

    data_interface.commit_query()
    data_interface.close_connection()


# if __name__ == '__main__':
#     process_file(vcf_file)