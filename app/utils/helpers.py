'''
Contain data transformation helper functions used by extract_load.py
'''


# Associate missing keys with 'Unknown' value to ensure listed keys exist in given dictionary
def fill_missing_key_value(data_dict: dict) -> None:
    keys = [
        'idx',
        'city_name',
        'city_geo_0',
        'city_geo_1',
        'time_s',
        'time_tz',
        'iaqi_co_v',
        'iaqi_h_v',
        'iaqi_o3_v',
        'iaqi_p_v',
        'iaqi_pm10_v',
        'iaqi_pm25_v',
        'iaqi_so2_v',
        'iaqi_t_v',
        'iaqi_w_v',
    ]
    for k in keys:
        data_dict.setdefault(k, 'Unknown')
