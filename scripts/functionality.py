import os
import allel
from werkzeug.utils import secure_filename


def check_ext(vcf_file):
    if os.path.splitext(vcf_file.filename)[1].lower() == '.vcf':
        return True


def save_input_file(vcf_file):
    vcf_file.save(secure_filename('input_file'))


def vcf_to_dataframe(vcf_file):
    return allel.vcf_to_dataframe('input_file', fields='*', alt_number=2)


