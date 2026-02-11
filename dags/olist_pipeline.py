from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from datetime import datetime

default_args = {
    'owner': 'serhat',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 0,
}

with DAG(
    'olist_end_to_end_pipeline',
    default_args=default_args,
    description='Olist ETL Pipeline: Bronze -> Quality Check -> Silver -> Gold',
    schedule_interval=None,
    start_date=datetime(2026, 2, 10),
    catchup=False,
    tags=['databricks', 'etl', 'olist', 'quality'],
) as dag:

    # 1. GÖREV: Bronze (Veriyi Çek)
    ingest_task = DatabricksRunNowOperator(
        task_id='1_ingest_bronze',
        databricks_conn_id='databricks_default',
        job_id= 404053805771974 # <--- MEVCUT BRONZE ID'Nİ YAZ
    )

    # ---------------------------------------------------------
    # 🆕 2. YENİ GÖREV: Kalite Kontrol (Bekçi)
    # ---------------------------------------------------------
    quality_check_task = DatabricksRunNowOperator(
        task_id='2_quality_check_bronze',
        databricks_conn_id='databricks_default',
        job_id= 694496822226620 # <--- YENİ ALDIĞIN 'CHECK' JOB ID'SİNİ BURAYA YAZ
    )

    # 3. GÖREV: Silver (Veriyi Temizle)
    transform_silver_task = DatabricksRunNowOperator(
        task_id='3_transform_silver',
        databricks_conn_id='databricks_default',
        job_id= 25465186672948 # <--- MEVCUT SILVER ID'Nİ YAZ
    )

    # 4. GÖREV: Gold (Raporla)
    transform_gold_task = DatabricksRunNowOperator(
        task_id='4_transform_gold',
        databricks_conn_id='databricks_default',
        job_id= 776776186787950 # <--- MEVCUT GOLD ID'Nİ YAZ
    )

    # =========================================================
    # 🔗 YENİ ZİNCİR YAPISI
    # Bronze biter -> Bekçi kontrol eder -> Silver başlar -> Gold biter
    # =========================================================
    ingest_task >> quality_check_task >> transform_silver_task >> transform_gold_task