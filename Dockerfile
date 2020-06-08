FROM python:3.7

EXPOSE 5000

WORKDIR /VCF_parser/data_integratie_project

COPY requirements.txt /VCF_parser/data_integratie_project
RUN pip install -r requirements.txt

COPY app.py /VCF_parser/data_integratie_project
CMD python3 app.py