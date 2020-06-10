from flask import Flask, render_template, request
from scripts.functionality import check_ext, save_input_file
from scripts.parse_vcf_to_database import process_file

import allel

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
            data_frame = allel.vcf_to_dataframe(vcf_file)

            return render_template('public/display_dataframe.html',
                                   tables=[data_frame.to_html(classes='data')],
                                   titles=data_frame.columns.values)
        else:
            return render_template("error/file_not_found_error.html")


@app.route('/update_database', methods=['GET', 'POST'])
def upload_to_database():
    vcf_file = open('input_file').readlines()
    process_file(vcf_file)

    return "file path was given to 'process_file'"


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
