"""
spark-submit --deploy-mode client --master local[*] examples/pyspark/iceberg_hive_metastore_minio.py
spark-submit --deploy-mode client --master spark://spark:7077 examples/pyspark/iceberg_hive_metastore_minio.py
"""

from pyspark.sql import SparkSession

spark = (
    SparkSession.builder.appName("IcebergIntegration")
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
    .config("spark.sql.catalog.localiceberg", "org.apache.iceberg.spark.SparkCatalog")
    .config("spark.sql.catalog.localiceberg.type", "hive")
    .config("spark.sql.catalog.localiceberg.uri", "thrift://hive-metastore:9083")
    .config("spark.sql.catalog.localiceberg.warehouse", "s3a://iceberg-warehouse/")
    .config("spark.sql.defaultCatalog", "localiceberg")
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
    .config("spark.hadoop.fs.s3a.access.key", "iceberg_user")
    .config("spark.hadoop.fs.s3a.secret.key", "iceberg_password")
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .config("spark.hadoop.fs.s3a.path.style.access", True)
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")

db = "devdb"
table = "my_iceberg_table"

print(f"--- create database: {db}")
spark.sql(f"CREATE DATABASE IF NOT EXISTS {db}")

print("--- show databases")
spark.sql("SHOW DATABASES").show(10, 0)

print(f"--- create table: {db}.{table}")
spark.sql(f"CREATE TABLE IF NOT EXISTS localiceberg.{db}.{table} (id int, name string) USING iceberg")

print(f"--- show tables in {db}")
spark.sql(f"SHOW TABLES IN {db}").show(10, 0)

print(f"--- insert data into {db}.{table}")
spark.sql(f"INSERT INTO localiceberg.{db}.{table} VALUES(1, 'Alice'), (2, 'Bob')")

print(f"--- show data from {db}.{table}")
spark.table(f"{db}.{table}").show(10, 0)


spark.stop()
