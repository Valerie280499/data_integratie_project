import os

def check_extension_of_input_file(vcf_file):
    if os.path.splitext(vcf_file.filename)[1].lower() == '.vcf':
        return True
