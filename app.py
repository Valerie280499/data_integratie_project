from flask import Flask, render_template, request
from functionality import check_ext, save_input_file, vcf_to_dataframe

app = Flask(__name__)
app.secret_key = 'many random bytes'


@app.route("/", methods=["GET", "POST"])
def upload_image():
    return render_template("public/home.html")


@app.route('/upload_file', methods=['GET', 'POST'])
def check_ext_of_input_file():
    if request.method == 'POST':
        f = request.files['file']
        check = check_ext(f)

        if check:
            save_input_file(f)
            data_frame = vcf_to_dataframe(f)

            return render_template('public/display_dataframe.html',
                                   tables=[data_frame.to_html(classes='data')],
                                   titles=data_frame.columns.values)
        else:
            return render_template("error/file_not_found_error.html")


@app.route('/hey')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
