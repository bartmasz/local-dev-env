from airflow import DAG
from airflow.hooks.base import BaseHook
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator


def check_spark_connection():
    try:
        connection = BaseHook.get_connection("spark_default")
        print(f"Connection to spark_default found: {connection}")
        if (
            connection.conn_type == "spark"
            and connection.host == "spark://spark"
            and connection.port == 7077
            and connection.extra_dejson["deploy-mode"] == "client"
            and connection.extra_dejson["spark-binary"] == "spark-submit"
        ):
            print("spark_default is properly configured.")
        else:
            print("conn_type", connection.conn_type)
            print("host", connection.host)
            print("port", connection.port)
            print("extra_dejson['deploy-mode']", connection.extra_dejson["deploy-mode"])
            print("extra_dejson['spark-binary']", connection.extra_dejson["spark-binary"])
            raise ValueError("spark_default is not properly configured.")
    except Exception as e:
        print(f"Error: {e}")
        raise


with DAG(
    dag_id="example_spark_submit_iceberg",
    schedule=None,
    tags=["example", "spark"],
):
    check_connection_task = PythonOperator(
        task_id="check_spark_connection",
        python_callable=check_spark_connection,
    )

    submit_job = SparkSubmitOperator(
        task_id="submit_job",
        conn_id="spark_default",
        application="/code/iceberg_hive_metastore_minio.py",
        deploy_mode="client",
    )


check_connection_task >> submit_job
