"""Execute this code by running:
spark-submit --deploy-mode client --master local[*] examples/pyspark/simple_pyspark_app.py
spark-submit --deploy-mode client --master spark://spark:7077 examples/pyspark/simple_pyspark_app.py
in devcontainer.
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("SimplePySparkApp").getOrCreate()

data = [
    ("Poland", 1),
    ("USA", 2),
    ("France", 3),
]

columns = ["country", "points"]

df = spark.createDataFrame(data=data, schema=columns)
total_points_df = df.groupby().agg(F.sum("points").alias("total_points"))
total_points = total_points_df.collect()[0]["total_points"]

df.show(10, 0)
print(f"TOTAL POINTS {total_points}\n")
