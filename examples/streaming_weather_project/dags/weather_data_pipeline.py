import pendulum
from cosmos import (
    DbtDag,
    ExecutionConfig,
    LoadMode,
    ProfileConfig,
    ProjectConfig,
    RenderConfig,
    ExecutionMode,
)

weather_dag = DbtDag(
    project_config=ProjectConfig(
        dbt_project_path="/examples/streaming_weather_project/dbt_weather/",
        seeds_relative_path="seeds",
        partial_parse=False,
    ),
    profile_config=ProfileConfig(
        profiles_yml_filepath="/examples/streaming_weather_project/dbt_weather/profiles.yml",
        profile_name="dbt_weather",
        target_name="dev",
    ),
    execution_config=ExecutionConfig(
        # dbt_executable_path="/home/airflow/.local/bin/dbt",
        execution_mode=ExecutionMode.LOCAL,
    ),
    render_config=RenderConfig(
        load_method=LoadMode.DBT_LS,
    ),
    operator_args={
        "dbt_cmd_global_flags": ["--use-colors"],
    },
    # normal dag parameters
    dag_id="weather-data-pipeline",
    start_date=pendulum.datetime(2024, 11, 1),
    schedule_interval="*/2 * * * *",  # every 2 minutes
    catchup=False,
    default_args={
        "retries": 0,
    },
    is_paused_upon_creation=False,
)

weather_dag
