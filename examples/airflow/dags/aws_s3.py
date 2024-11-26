import boto3

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator


def list_s3_buckets():
    aws_profile_name = Variable.get("aws_profile_name")
    session = boto3.Session(profile_name=aws_profile_name)
    s3 = session.client("s3")
    response = s3.list_buckets()
    for bucket in response["Buckets"]:
        print(f"Bucket Name: {bucket['Name']}")


default_args = {
    "owner": "airflow",
}

with DAG(
    "example_aws_s3",
    default_args=default_args,
    schedule_interval=None,
    max_active_runs=1,
    catchup=False,
) as dag:
    list_buckets = PythonOperator(
        task_id="list_buckets",
        python_callable=list_s3_buckets,
    )
