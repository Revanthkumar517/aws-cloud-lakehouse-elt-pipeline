FROM apache/airflow:2.11.0-python3.11

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

RUN pip install --no-cache-dir \
    "apache-airflow==2.11.0" \
    "apache-airflow-providers-amazon==9.29.0" \
    "dbt-core==1.8.5" \
    "dbt-athena-community==1.8.4" \
    "pandas==2.2.2" \
    "numpy==1.26.4" \
    "python-dotenv==1.0.1" \
    "great-expectations==0.18.21"
