FROM apache/airflow:2.10.1
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" langdetect better_profanity google-generativeai nltk psycopg2-binary    
# NLTK punkt package
RUN python -m nltk.downloader punkt_tab