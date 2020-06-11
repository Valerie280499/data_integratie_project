"""
Description: app.py, this file links all the scripts together to one application
Author: Anne Manders and Valerie Verhalle
Date: 11-6-2020
Version: 8
"""

import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
from scripts.extract_data_from_database import check_if_database_is_not_empty, \
    extract_all_data_from_database
from scripts.parse_vcf_content_to_database import upload_vcf_content

app = Flask(__name__)
app.secret_key = 'many random bytes'


@app.route("/", methods=["GET", "POST"])
def upload_image():
    """
    :return template("public/home.html"). Start the application by returning the home page
    """

    return render_template("public/home.html")


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_input_file_to_database():
    """ When a file is uploaded, extract the file name and save it to the scope of the project.

    Check if the file extension is '.vcf' if this is True:
        The function 'upload_vcf_content' is called.

        When this function returns True (content was uploaded to the database):
            :return template("public/database_has_been_updated.html"). When the database has been updated.
        If the function returns False (no content was uploaded):
            :return template("error/database_error.html"). When the database has not been updated,
            or another error appeared.

    When any error occurs while opening/ saving the file,
    the error will be displayed in an error page:
    :return template("error/input_file_is_not_valid.html")
     """

    if request.method == 'POST':
        vcf_file = request.files['file']
        vcf_file.save(secure_filename(vcf_file.filename))

        try:
            if os.path.splitext(vcf_file.filename)[1].lower() == '.vcf':
                if upload_vcf_content(vcf_file):
                    return render_template("public/database_has_been_updated.html",
                                           text="Database has been updated")
                else:
                    return render_template("error/database_error.html",
                                           text="An error occurred, it could be:\n"
                                                "1. No data was committed to the database "
                                                "because no data passed the criteria.\n"
                                                "2. Or an unexpected database error "
                                                "showed up. \n Check the log!")
            else:
                return render_template("error/input_file_is_not_valid.html",
                                       text="File extension is not right, "
                                            "should be an VCF file")
        except Exception as error:
            return render_template("error/input_file_is_not_valid.html",
                                   text=error)


@app.route('/get_all_data', methods=['GET', 'POST'])
def get_all_data_from_database():
    """ When the user wants to display all the data available in the database,
    check first if the database is not empty.

    If the function 'check_if_database_is_not_empty' returns True (database has content):
        extract all it's content using the function 'extract_all_data_from_database', this function returns an list
        with all the available data in the database.
        :return template("public/record_to_interactive_html_table.html"). The created record is passed
        through to this page, here the data will be displayed in a html table.

    When the database has no content to display, the function 'check_if_database_is_not_empty' returns False, and a
    error page will be displayed.
    :return template("error/database_error.html"). Database is empty.
    """

    if check_if_database_is_not_empty():
        record = extract_all_data_from_database()
        return render_template("public/record_to_interactive_html_table.html",
                               record=record)
    else:
        return render_template("error/database_error.html",
                               text="database is empty")


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
