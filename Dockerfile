FROM python:3.7

EXPOSE 5000

WORKDIR /data_integratie_project

COPY ./  /data_integratie_project

RUN pip install -r requirements.txt

CMD python3 app.py