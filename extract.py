import requests
from typing import Any, Dict, List, Optional
import pandas as pd
import pytz
from datetime import datetime

def get_station_data() -> List[Dict[str, Any]]:
    url = 'https://api.waqi.info/v2/map/bounds?latlng=49,-125,26,-62&networks=all&token=d9b8e1ae92cfc70dc510bf3e8ada111cb9163afb'
    resp = requests.get(url)
    return resp.json().get('data', [])

def _get_station_insert_query() -> str:
    return '''
    INSERT INTO StationDim (
        id,
        name,
        latitude,
        longitude,
        air_quality_index,
        time
    )
    VALUES (
        %(uid)s,
        %(station_name)s,
        %(latitude)s,
        %(longitude)s,
        %(air_quality_index)s,
        %(station_time)s
    );
    '''

data = get_station_data()
df = pd.json_normalize(data, sep='_')
# Parse data string to UTC datetime
df['station_time'] = pd.to_datetime(df['station_time'], utc=True)
# Format station time to remove +00:00 at the end
df['station_time'] = df['station_time'].dt.strftime('%Y-%m-%d %H:%M:%S')