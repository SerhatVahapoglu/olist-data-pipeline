# Resmi Airflow imajını temel alıyoruz
FROM apache/airflow:2.8.1

# Databricks provider paketini yüklüyoruz
RUN pip install --no-cache-dir apache-airflow-providers-databricks