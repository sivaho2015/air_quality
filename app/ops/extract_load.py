'''
Functions to extract and load air quality data
'''
import os
import queue
from threading import Thread
from typing import Any, Dict, List

import psycopg2.extras as p
import requests
from dagster import op
from dotenv import load_dotenv
from flatten_json import flatten
from utils.config import get_warehouse_creds
from utils.db import WarehouseConnection
from utils.helpers import fill_missing_key_value


# Get all the stations in the US given latitude and longitude bounds
@op(config_schema={"lat1": str, "long1": str, "lat2": str, "long2": str})
def get_stations_in_us(context) -> List[Dict[str, Any]]:
    lat1 = context.op_config["lat1"]
    long1 = context.op_config["long1"]
    lat2 = context.op_config["lat2"]
    long2 = context.op_config["long2"]
    api_token = os.getenv('AIR_QUALITY_API_TOKEN', '')
    url = f'''https://api.waqi.info/v2/map/bounds?latlng={lat1},{long1},{lat2},{long2}&networks=all&token={api_token}'''
    resp = requests.get(url)
    data = resp.json().get('data', [])
    return data


# Construct API URLs to get air quality feed data for each station
@op
def construct_station_feed_urls(stations: List[Dict[str, Any]]) -> List[str]:
    urls = []
    api_token = os.getenv('AIR_QUALITY_API_TOKEN', '')
    for s in stations:
        uid = s['uid']
        url = f'''https://api.waqi.info/feed/@{uid}/?token={api_token}'''
        urls.append(url)
    return urls


# Define Worker class that will be used by perform_requests
class Worker(Thread):
    def __init__(self, request_queue):
        Thread.__init__(self)
        self.queue = request_queue  # Queue that stores API URLs
        self.results = []  # List that stores API call results

    # Get a URL from queue and perform request
    def run(self):
        while True:
            content = self.queue.get()
            if content == "":
                break
            resp = requests.get(content)
            data = resp.json().get('data', [])
            data_flattened = flatten(data)
            # Associate missing keys with 'Unknown' value
            fill_missing_key_value(data_flattened)
            self.results.append(data_flattened)
            self.queue.task_done()


# Perform parallel API calls given a list of API URLs
@op
def perform_requests(urls: List[str]) -> List[Dict[str, Any]]:
    # Define the number of workers
    num_workers = 500
    # Create queue and add URLs
    q = queue.Queue()
    for url in urls:
        q.put(url)

    # Workers keep working until they receive an empty string
    for _ in range(num_workers):
        q.put("")

    # Create workers and add to the queue
    workers = []
    for _ in range(num_workers):
        worker = Worker(q)
        worker.start()
        workers.append(worker)
    # Join workers to wait until they finished
    for worker in workers:
        worker.join()

    # Combine results from all workers
    res = []
    for worker in workers:
        res.extend(worker.results)
    return res


# Load air quality feed data into database
@op
def load_station_feed_data(station_feed_data: List[Dict[str, Any]]) -> None:
    insert_query = """
    INSERT INTO air_quality.station_feed (
        station_id,
        city_name,
        latitude,
        longitude,
        local_measurement_time,
        local_measurement_timezone,
        carbon_monoxide,
        humidity,
        ozone,
        pressure,
        pm_10,
        pm_2_5,
        sulfur_dioxide,
        temperature,
        wind_speed
    )
    VALUES (
        %(idx)s,
        %(city_name)s,
        %(city_geo_0)s,
        %(city_geo_1)s,
        %(time_s)s,
        %(time_tz)s,
        %(iaqi_co_v)s,
        %(iaqi_h_v)s,
        %(iaqi_o3_v)s,
        %(iaqi_p_v)s,
        %(iaqi_pm10_v)s,
        %(iaqi_pm25_v)s,
        %(iaqi_so2_v)s,
        %(iaqi_t_v)s,
        %(iaqi_w_v)s
    )
    """
    with WarehouseConnection(get_warehouse_creds()).managed_cursor() as curr:
        p.execute_batch(curr, insert_query, station_feed_data)
