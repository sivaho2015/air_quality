'''
Dagster data pipline schedule
'''
from dagster import schedule
from jobs.data_ingestion import data_ingestion


# Function that runs pipeline at 00:00 CST each day and is called by Dagster repository
@schedule(
    cron_schedule="0 0 * * *",
    job=data_ingestion,
    execution_timezone="US/Central",
)
def data_ingestion_schedule(_context):
    return {}
