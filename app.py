import vcf

from flask import Flask, render_template, request
from scripts.functionality import check_ext, save_input_file, vcf_to_dataframe, \
    parse_all_data_from_database_to_data_frame
from scripts.parse_vcf_to_database import process_file
from Database.extract_data_from_database import check_if_database_is_empty

app = Flask(__name__)
app.secret_key = 'many random bytes'


@app.route("/", methods=["GET", "POST"])
def upload_image():
    return render_template("public/home.html")


@app.route('/upload_file', methods=['GET', 'POST'])
def check_ext_of_input_file():
    if request.method == 'POST':
        vcf_file = request.files['file']

        if check_ext(vcf_file):
            save_input_file(vcf_file)
        else:
            return render_template("error/file_not_found_error.html")


@app.route('/update_database', methods=['GET', 'POST'])
def upload_to_database():
    vcf_reader = vcf.Reader(open('input_file', 'r'))
    process_file(vcf_reader)
    return render_template("public/display_all_or_filtered_data_from_database.html",
                           text="Database has been updated")


@app.route('/get_all_data', methods=['GET', 'POST'])
def get_all_data_from_database():
    message = check_if_database_is_empty()

    if message:
        return render_template("error/database_error.html", text="database is empty")
    else:
        data_frame = vcf_to_dataframe()
        return render_template("public/display_all_data_from_database.html",
                               tables=[data_frame.to_html(classes='data')],
                               titles=data_frame.columns.values)


@app.route('/get_filtered_data', methods=['GET', 'POST'])
def get_filtered_data_from_database():
    pass


if __name__ == '__main__':
    app.run(debug=True)
