FROM python:3.6.3
# supervisord setup                       
RUN apt-get update && apt-get install -y supervisor

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# Airflow setup                       
ENV AIRFLOW_HOME=/app/airflow
RUN pip install apache-airflow                       
COPY ./*.py $AIRFLOW_HOME/dags/
RUN airflow initdb
EXPOSE 8080
CMD ["/usr/bin/supervisord"]