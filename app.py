from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
from scripts.extract_data_from_database import check_if_database_is_not_empty, extract_all_data_from_database
from scripts.functionality import check_extension_of_input_file
from scripts.parse_vcf_content_to_database import upload_vcf_content

app = Flask(__name__)
app.secret_key = 'many random bytes'


@app.route("/", methods=["GET", "POST"])
def upload_image():
    return render_template("public/home.html")


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_input_file_to_database():
    if request.method == 'POST':
        vcf_file = request.files['file']
        vcf_file.save(secure_filename(vcf_file.filename))

        try:
            if check_extension_of_input_file(vcf_file):
                if upload_vcf_content(vcf_file):
                    return render_template("public/database_has_been_updated.html", text="Database has been updated")
                else:
                    return render_template("error/database_error.html", text="An error occurred, it could be:\n"
                                                                             "1. No data was committed to the database "
                                                                             "because no data passed the criteria.\n"
                                                                             "2. Or an unexpected database error "
                                                                             "showed up. \n Check the log!")
            else:
                return render_template("error/input_file_is_not_valid.html", text="File extension is not right, "
                                                                                  "should be an VCF file")
        except FileNotFoundError:
            return render_template("error/input_file_is_not_valid.html", text="File not found")
        except Exception as error:
            return render_template("error/input_file_is_not_valid.html", text=error)


@app.route('/get_all_data', methods=['GET', 'POST'])
def get_all_data_from_database():

    if check_if_database_is_not_empty():
        record = extract_all_data_from_database()
        return render_template("public/record_to_interactive_html_table.html",
                               record=record)
    else:
        return render_template("error/database_error.html", text="database is empty")


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug='True')
