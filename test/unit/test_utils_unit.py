'''
Unit tests for functions in utils.helpers
'''
from utils.helpers import fill_missing_key_value


# Test fill_missing_key_value()
def test_fill_missing_key_value():
    data_dict: dict = {'idx': '1234', 'city_name': 'Test City'}
    expected_data_dict = {
        'idx': '1234',
        'city_name': 'Test City',
        'city_geo_0': 'Unknown',
        'city_geo_1': 'Unknown',
        'time_s': 'Unknown',
        'time_tz': 'Unknown',
        'iaqi_co_v': 'Unknown',
        'iaqi_h_v': 'Unknown',
        'iaqi_o3_v': 'Unknown',
        'iaqi_p_v': 'Unknown',
        'iaqi_pm10_v': 'Unknown',
        'iaqi_pm25_v': 'Unknown',
        'iaqi_so2_v': 'Unknown',
        'iaqi_t_v': 'Unknown',
        'iaqi_w_v': 'Unknown',
    }
    fill_missing_key_value(data_dict)
    assert expected_data_dict == data_dict
