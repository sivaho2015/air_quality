'''
Dagster repository that combines Dagster ops, jobs, and pipeline schedule
'''
from dagster import repository
from jobs.data_ingestion import data_ingestion
from schedules.data_ingestion_schedule import data_ingestion_schedule


# Deploy Dagster repository
@repository
def deploy_docker_repository():
    return [data_ingestion, data_ingestion_schedule]
