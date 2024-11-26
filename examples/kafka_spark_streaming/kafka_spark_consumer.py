"""
spark-submit --deploy-mode client --master local[*] examples/kafka_spark_streaming/kafka_spark_consumer.py
spark-submit --deploy-mode client --master spark://spark:7077 examples/kafka_spark_streaming/kafka_spark_consumer.py
"""

from pyspark.sql import SparkSession

BOOTSTRAP_SERVERS = "kafka0:9092"
TOPIC_NAME = "streaming-sink"
CATALOG_NAME = "localiceberg"
DATABASE_NAME = "devdb"
TABLE_NAME = "streaming_sink"
FULL_TABLE_NAME = f"{CATALOG_NAME}.{DATABASE_NAME}.{TABLE_NAME}"

spark = (
    SparkSession.builder.appName("KafkaSparkConsumer")
    .config(
        "spark.sql.extensions",
        "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
    )
    .config("spark.sql.catalog.localiceberg", "org.apache.iceberg.spark.SparkCatalog")
    .config("spark.sql.catalog.localiceberg.type", "hive")
    .config("spark.sql.catalog.localiceberg.uri", "thrift://hive-metastore:9083")
    .config("spark.sql.catalog.localiceberg.warehouse", "s3a://iceberg-warehouse/")
    .config("spark.sql.defaultCatalog", CATALOG_NAME)
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
    .config("spark.hadoop.fs.s3a.access.key", "iceberg_user")
    .config("spark.hadoop.fs.s3a.secret.key", "iceberg_password")
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .config("spark.hadoop.fs.s3a.path.style.access", True)
    .getOrCreate()
)

spark.sql(f"CREATE DATABASE IF NOT EXISTS {CATALOG_NAME}.{DATABASE_NAME}")
spark.sql(f"DROP TABLE IF EXISTS {FULL_TABLE_NAME} PURGE")

sql = f"""
CREATE TABLE {FULL_TABLE_NAME} (
    key binary,
    value binary,
    topic string,
    partition int,
    offset long,
    timestamp timestamp,
    timestampType int,
    headers array<string>
)
USING iceberg;
"""
spark.sql(sql)


checkpointPath = "/tmp/spark_checkpoints"

kafka_params = {
    "kafka.bootstrap.servers": BOOTSTRAP_SERVERS,
    "subscribe": TOPIC_NAME,
    "startingOffsets": "latest",
    "failOnDataLoss": "false",
}

streaming_df = spark.readStream.format("kafka").options(**kafka_params).load()
query = (
    streaming_df.writeStream.format("iceberg")
    .outputMode("append")
    .trigger(processingTime="1 minute")
    .option("checkpointLocation", checkpointPath)
    .toTable(FULL_TABLE_NAME)
)
query.awaitTermination()
spark.stop()
