'''
Test functions in ops.extract_load.py
'''
import unittest
from unittest.mock import patch

from dagster import build_op_context
from ops.extract_load import (construct_station_feed_urls, get_stations_in_us,
                              perform_requests)


# Class that contains test cases
class TestExtractLoad(unittest.TestCase):
    # test get_stations_in_us function
    def test_get_stations_in_us(self):
        # mock requests.get() function
        mock_get_patcher = patch('ops.extract_load.requests.get')

        # define requests.get() return value
        stations = {
            'data': [
                {
                    'lat': 11,
                    'long': 40,
                    'uid': 56,
                    'aqi': '100',
                    'station_name': 'NASA',
                },
                {
                    'lat': 13,
                    'long': 20,
                    'uid': 156,
                    'aqi': '120',
                    'station_name': 'Chicago, IL',
                },
            ]
        }
        # start mocking
        mock_get = mock_get_patcher.start()
        mock_get.return_value.json.return_value = stations

        # call get_stations_in_us() with given context
        context = build_op_context(
            config={'lat1': '49', 'long1': '50', 'lat2': '99', 'long2': '100'}
        )
        data = get_stations_in_us(context)

        # stop mocking
        mock_get_patcher.stop()

        self.assertEqual(data, stations['data'])

    # Test construct_station_feed_urls()
    def test_construct_station_feed_urls(self):
        # input data
        stations = [
            {
                'lat': 11,
                'long': 40,
                'uid': 56,
                'aqi': '100',
                'station_name': 'NASA',
            },
            {
                'lat': 13,
                'long': 20,
                'uid': 156,
                'aqi': '120',
                'station_name': 'Chicago, IL',
            },
        ]

        # expected output
        expected_urls = [
            'https://api.waqi.info/feed/@56/?token=d9b8e1ae92cfc70dc510bf3e8ada111cb9163afb',
            'https://api.waqi.info/feed/@156/?token=d9b8e1ae92cfc70dc510bf3e8ada111cb9163afb',
        ]

        # call construct_station_feed_urls()
        urls = construct_station_feed_urls(stations)

        self.assertEqual(urls, expected_urls)

    # Test perform_requests()
    def test_perform_requests(self):
        # input data
        urls = [
            'https://api.waqi.info/feed/@56/?token=d9b8e1ae92cfc70dc510bf3e8ada111cb9163afb'
        ]

        # mock requests.get()
        mock_get_patcher = patch('ops.extract_load.requests.get')

        # mock requests.get() return value
        station_feed_data = {
            'data': {
                'idx': 11,
                'iaqi_co_v': 56,
                'time_s': '2023-04-03 19:00:00',
                'time_tz': '-05:00',
            }
        }

        # start mocking
        mock_get = mock_get_patcher.start()
        mock_get.return_value.json.return_value = station_feed_data

        # call perform_requests()
        data = perform_requests(urls)

        # stop mocking
        mock_get_patcher.stop()

        expected_data = [
            {
                'idx': 11,
                'city_name': 'Unknown',
                'city_geo_0': 'Unknown',
                'city_geo_1': 'Unknown',
                'time_s': '2023-04-03 19:00:00',
                'time_tz': '-05:00',
                'iaqi_co_v': 56,
                'iaqi_h_v': 'Unknown',
                'iaqi_o3_v': 'Unknown',
                'iaqi_p_v': 'Unknown',
                'iaqi_pm10_v': 'Unknown',
                'iaqi_pm25_v': 'Unknown',
                'iaqi_so2_v': 'Unknown',
                'iaqi_t_v': 'Unknown',
                'iaqi_w_v': 'Unknown',
            }
        ]
        self.assertEqual(data, expected_data)
