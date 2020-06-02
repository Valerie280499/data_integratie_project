import os

import allel
from werkzeug.utils import secure_filename


def check_ext(f):
    if os.path.splitext(f.filename)[1].lower() == '.vcf':
        return True


def save_input_file(f):
    f.save(secure_filename(f.filename))


def vcf_to_dataframe(f):
    return allel.vcf_to_dataframe(f.filename, fields='*', alt_number=2)


