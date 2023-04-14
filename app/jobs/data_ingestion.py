'''
Construct Dagster data pipeline and configure its run inputs
'''
from dagster import job
from dagster_dbt import dbt_cli_resource, dbt_run_op, dbt_test_op
from ops.extract_load import (construct_station_feed_urls, get_stations_in_us,
                              load_station_feed_data, perform_requests)

# Configure dbt project and profiles directories
dbt_resource = dbt_cli_resource.configured(
    {
        "project_dir": "./transform",
        "profiles_dir": "./transform",
    }
)

# Dagster data pipeline run configurations
run_config = {
    "ops": {
        "get_stations_in_us": {
            "config": {
                "lat1": "49",
                "long1": "-125",
                "lat2": "26",
                "long2": "-62",
            }
        }
    }
}


# Construct data pipeline
@job(resource_defs={"dbt": dbt_resource}, config=run_config)
def data_ingestion():
    dbt_test_op(
        dbt_run_op(
            [
                load_station_feed_data(
                    perform_requests(
                        construct_station_feed_urls(get_stations_in_us())
                    )
                )
            ]
        )
    )
