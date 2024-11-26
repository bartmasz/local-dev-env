"""Execute this code by running:
spark-submit --deploy-mode client --master local[*] examples/pyspark/cpu_heavy_pyspark_app.py
spark-submit --deploy-mode client --master spark://spark:7077 examples/pyspark/cpu_heavy_pyspark_app.py
in devcontainer.
"""

import random

from pyspark.sql import SparkSession


def compute_sqrt(num_iterations):
    """Function to compute square roots of random numbers"""
    nums = [random.random() for _ in range(num_iterations)]
    sqrt_nums = [n**0.5 for n in nums]
    return sum(sqrt_nums)


def main(i):
    spark = SparkSession.builder.appName("CPUHeavyPySparkApp").getOrCreate()

    # Number of random numbers to generate (example: 10 million)
    num_iterations = 10000000

    # Use Spark to distribute the computation
    rdd = spark.sparkContext.parallelize([num_iterations] * 10, numSlices=10)
    result = rdd.map(compute_sqrt).collect()

    # Print the results
    print(f"{i}: sum of computed square roots: {sum(result)}")

    # Stop the SparkSession
    spark.stop()


if __name__ == "__main__":
    for i in range(1):
        main(i)
