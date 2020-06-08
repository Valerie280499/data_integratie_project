from flask import Flask, render_template

import vcf
import mysql.connector as connector

import os
# import allel
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'many random bytes'


@app.route("/", methods=["GET", "POST"])
def upload_image():
    return render_template("./data_integratie_project/templates/public/home.html")



# @app.route('/upload_file', methods=['GET', 'POST'])
# def check_ext_of_input_file():
#     if request.method == 'POST':
#         vcf_file = request.files['file']
#
#         if check_ext(vcf_file):
#             save_input_file(vcf_file)
#             data_frame = vcf_to_dataframe(vcf_file)
#
#             return render_template('public/display_dataframe.html',
#                                    tables=[data_frame.to_html(classes='data')],
#                                    titles=data_frame.columns.values)
#         else:
#             return render_template("error/file_not_found_error.html")


@app.route('/update_database', methods=['GET', 'POST'])
def upload_to_database():
    vcf_file = open('input_file').readlines()
    process_file(vcf_file)

    return "file path was given to 'process_file'"


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
    connection = connector.connect(host='database', db='data_integratie', user='root', password='Annesql', port='3306')
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


def check_ext(vcf_file):
    if os.path.splitext(vcf_file.filename)[1].lower() == '.vcf':
        return True


def save_input_file(vcf_file):
    vcf_file.save(secure_filename('input_file'))


# def vcf_to_dataframe(vcf_file):
#     return allel.vcf_to_dataframe('input_file', fields='*', alt_number=2)




if __name__ == '__main__':
    app.run()
