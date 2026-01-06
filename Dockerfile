FROM apache/airflow:2.7.0
USER root
RUN apt-get update && apt-get install -y default-libmysqlclient-dev gcc
USER airflow
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
RUN pip install --no-cache-dir pymysql cryptography