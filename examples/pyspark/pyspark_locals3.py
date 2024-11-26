"""Execute by running this command in console:
spark-submit --deploy-mode client --master local[*] examples/pyspark/pyspark_locals3.py
spark-submit --deploy-mode client --master spark://spark:7077 examples/pyspark/pyspark_locals3.py
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import os

# Create minio_bucket_name, minio_access_key and minio_secret_key through WebUI or with mc cli
# export them as environment variables
minio_access_key = os.environ["MINIO_ACCESS_KEY"]
minio_secret_key = os.environ["MINIO_SECRET_KEY"]
minio_bucket_name = "dev-test-1"
spark = (
    SparkSession.builder.config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .config("spark.hadoop.fs.s3a.path.style.access", True)
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
    .config("spark.hadoop.fs.s3a.access.key", minio_access_key)
    .config("spark.hadoop.fs.s3a.secret.key", minio_secret_key)
    .getOrCreate()
)

# Create DataFrame
data = [
    ("Poland", 1),
    ("USA", 2),
    ("France", 3),
    ("UK", 4),
]
columns = ["country", "points"]
df = spark.createDataFrame(data=data, schema=columns)
df.show(10, 0)

# Save DataFrame to MinIO S3 bucket
s3_location = f"s3a://{minio_bucket_name}/country_data/"
df.coalesce(1).write.parquet(s3_location, mode="overwrite")

# Read DataFrame from MinIO S3 bucket
df_new = spark.read.parquet(s3_location)
total_points_df = df_new.groupby().agg(F.sum("points").alias("total_points"))
total_points = total_points_df.collect()[0]["total_points"]
print(f"TOTAL POINTS {total_points}\n")
