from __future__ import annotations

import os
import time
from datetime import datetime

import boto3
from airflow import DAG
from airflow.exceptions import AirflowException
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


AWS_REGION = "us-east-1"
S3_BUCKET = os.environ["S3_BUCKET"]
RAW_CRAWLER_NAME = "ecommerce-raw-crawler"
CURATED_CRAWLER_NAME = "ecommerce-curated-crawler"
GLUE_JOB_NAME = "ecommerce-raw-to-curated-job"


def run_glue_crawler(
    crawler_name: str,
    timeout_seconds: int = 1200,
) -> None:
    """Start an existing Glue crawler and wait for successful completion."""

    glue = boto3.client("glue", region_name=AWS_REGION)

    existing = glue.get_crawler(Name=crawler_name)["Crawler"]
    previous_start_time = (
        existing.get("LastCrawl", {}).get("StartTime")
        if existing.get("LastCrawl")
        else None
    )

    try:
        glue.start_crawler(Name=crawler_name)
        started_new_run = True
        print(f"Started Glue crawler: {crawler_name}")
    except glue.exceptions.CrawlerRunningException:
        started_new_run = False
        print(f"Glue crawler is already running: {crawler_name}")

    deadline = time.time() + timeout_seconds

    while time.time() < deadline:
        crawler = glue.get_crawler(Name=crawler_name)["Crawler"]
        state = crawler["State"]
        last_crawl = crawler.get("LastCrawl")

        print(f"Crawler {crawler_name} state: {state}")

        if state == "READY" and last_crawl:
            current_start_time = last_crawl.get("StartTime")

            completed_expected_run = (
                not started_new_run
                or previous_start_time is None
                or current_start_time != previous_start_time
            )

            if completed_expected_run:
                status = last_crawl.get("Status")

                if status != "SUCCEEDED":
                    raise AirflowException(
                        f"Crawler {crawler_name} finished with status {status}"
                    )

                print(f"Crawler completed successfully: {crawler_name}")
                return

        time.sleep(15)

    raise AirflowException(
        f"Crawler {crawler_name} did not finish within {timeout_seconds} seconds"
    )


def run_glue_job(
    bucket_name: str,
    timeout_seconds: int = 2400,
) -> str:
    """Start the existing Glue PySpark job and wait for completion."""

    glue = boto3.client("glue", region_name=AWS_REGION)

    response = glue.start_job_run(
        JobName=GLUE_JOB_NAME,
        Arguments={
            "--S3_BUCKET": bucket_name,
            "--RAW_PREFIX": "raw/ecommerce",
            "--CURATED_PREFIX": "curated/ecommerce",
        },
    )

    run_id = response["JobRunId"]
    print(f"Started Glue job {GLUE_JOB_NAME}, run ID: {run_id}")

    deadline = time.time() + timeout_seconds
    terminal_states = {
        "SUCCEEDED",
        "FAILED",
        "STOPPED",
        "TIMEOUT",
        "ERROR",
        "EXPIRED",
    }

    while time.time() < deadline:
        job_run = glue.get_job_run(
            JobName=GLUE_JOB_NAME,
            RunId=run_id,
            PredecessorsIncluded=False,
        )["JobRun"]

        state = job_run["JobRunState"]
        print(f"Glue job state: {state}")

        if state in terminal_states:
            if state != "SUCCEEDED":
                error_message = job_run.get(
                    "ErrorMessage",
                    "No Glue error message returned",
                )
                raise AirflowException(
                    f"Glue job failed with state {state}: {error_message}"
                )

            print(f"Glue job completed successfully: {run_id}")
            return run_id

        time.sleep(20)

    raise AirflowException(
        f"Glue job did not finish within {timeout_seconds} seconds"
    )


default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "retries": 0,
}


with DAG(
    dag_id="aws_cloud_lakehouse_elt_pipeline",
    default_args=default_args,
    description="AWS cloud lakehouse ELT pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    tags=["aws", "lakehouse", "elt", "glue", "athena", "dbt"],
) as dag:

    generate_mock_data = BashOperator(
        task_id="generate_mock_data",
        bash_command="""
        set -e
        cd /usr/local/airflow/project
        python data_generator/generate_mock_data.py
        """,
    )

    validate_raw_data = BashOperator(
        task_id="validate_raw_data",
        bash_command="""
        set -e
        cd /usr/local/airflow/project
        python quality/validate_raw_orders.py
        """,
    )

    upload_raw_files = BashOperator(
    task_id="upload_raw_files_to_s3",
    bash_command="""
    set -e
    cd /usr/local/airflow/project
    python scripts/upload_to_s3.py
    """,
    env={
        "S3_BUCKET": S3_BUCKET,
        "AWS_REGION": "us-east-1",
        "RAW_PREFIX": "raw/ecommerce",
        "CURATED_PREFIX": "curated/ecommerce",
    },
    append_env=True,
)

    run_raw_crawler = PythonOperator(
        task_id="run_raw_crawler",
        python_callable=run_glue_crawler,
        op_kwargs={
            "crawler_name": RAW_CRAWLER_NAME,
        },
    )

    run_glue_transform = PythonOperator(
        task_id="run_glue_transform_job",
        python_callable=run_glue_job,
        op_kwargs={
            "bucket_name": S3_BUCKET,
        },
    )

    run_curated_crawler = PythonOperator(
        task_id="run_curated_crawler",
        python_callable=run_glue_crawler,
        op_kwargs={
            "crawler_name": CURATED_CRAWLER_NAME,
        },
    )

    run_dbt_models = BashOperator(
    task_id="run_dbt_models_and_tests",
    bash_command="""
    set -e
    cd /usr/local/airflow/project/dbt/aws_lakehouse_dbt_project

    rm -rf target logs

    dbt --no-partial-parse run --full-refresh
    dbt --no-partial-parse test
    """,
)

    run_athena_validation = BashOperator(
    task_id="run_athena_validation_queries",
    bash_command="""
    set -e
    cd /usr/local/airflow/project
    python scripts/run_athena_validation.py
    """,
    env={
        "AWS_REGION": "us-east-1",
        "ATHENA_DATABASE": "ecommerce_lakehouse",
        "ATHENA_OUTPUT_LOCATION": (
            f"s3://{S3_BUCKET}/athena-results/"
        ),
    },
    append_env=True,
)

    (
        generate_mock_data
        >> validate_raw_data
        >> upload_raw_files
        >> run_raw_crawler
        >> run_glue_transform
        >> run_curated_crawler
        >> run_dbt_models
        >> run_athena_validation
    )