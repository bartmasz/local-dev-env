# Streaming Weather Project

This project demonstrates a streaming data pipeline for weather data. It collects and processes mock real-time temperature information.

## Technologies Used

- **Python** for mocking temperature sensor data and sending to Kafka.
- **Apache Kafka** for real-time data streaming.
- **Apache Spark** for real-time data consumption and sending to Iceberg.
- **Apache Iceberg** for storing raw data and medalion data architecture.
- **Apache Airflow** for data ochestration.
- **dbt** for data transformation.

## Getting Started

1. Clone the repository:

    ```sh
    git clone https://github.com/bartmasz/local-dev-env
    ```

2. Follow [instructions](../../README.md) to start Visual Studio Code DevContainers.

## Usage

### Generate mock temperature data

Open terminal in VS Code.

```bash
cd examples/streaming_weather_project/streaming/
./produce_weather_data.py
```

Open [Kafka UI](http://localhost:8083/ui/clusters/local-kafka/all-topics/weather-data) to watch incomming messages.

### Consume data from Kafka to Iceberg

Open the next terminal tab.

```bash
cd examples/streaming_weather_project/streaming/
./consume_weather_data.py
```

Open the [Spark UI](http://localhost:4040) to monitor the PySpark application.

Open [MinIO](http://localhost:9001/browser/iceberg-warehouse) to see how data is saved to Iceberg tables.

### Transform data

Copy `examples/streaming_weather_project/dags/weather_data_pipeline.py` to `airflow/dags/weather_data_pipeline.py`.

Open [Airflow](http://localhost:8080) (*credentials: airflow/airflow*) to monitor the PySpark application.

Open [MinIO](http://localhost:9001/browser/iceberg-warehouse) to see how data is saved to Iceberg tables in bronze, silver, and gold tiers.
