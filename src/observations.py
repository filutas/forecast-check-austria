import time
from pathlib import Path
import pandas as pd
import requests

BASE = 'https://dataset.api.hub.geosphere.at/v1/station/historical/klima-v2-1h'
RAW = Path('data/raw')
PARAMS = ('tl', 'rr')


def month_ranges(start, end):
    for m in pd.period_range(start, end, freq='M'):
        yield m.start_time.strftime('%Y-%m-%dT00:00'), m.end_time.strftime('%Y-%m-%dT23:00')


def fetch_month(station_id, start, end):
    RAW.mkdir(parents=True, exist_ok=True)
    out = RAW / f'obs_{station_id}_{start[:7]}.parquet'
    if out.exists():
        return pd.read_parquet(out)
    query = {'parameters': ','.join(PARAMS), 'station_ids': station_id,
             'start': start, 'end': end, 'output_format': 'geojson'}
    response = None
    for attempt in range(3):
        try:
            response = requests.get(BASE, params=query, timeout=60)
            response.raise_for_status()
            break
        except requests.RequestException as err:
            print('retry', attempt + 1, err)
            time.sleep(5 * (attempt + 1))
    if response is None or not response.ok:
        raise RuntimeError(f'Download failed for {station_id} {start}')
    j = response.json()
    df = pd.DataFrame({'time': pd.to_datetime(j['timestamps'], utc=True)})
    values = j['features'][0]['properties']['parameters']
    for p in PARAMS:
        df[p] = pd.to_numeric(pd.Series(values[p]['data']), errors='coerce')
    df.to_parquet(out)
    time.sleep(1)
    return df


def fetch_station(station_id, start, end):
    parts = [fetch_month(station_id, s, e) for s, e in month_ranges(start, end)]
    df = pd.concat(parts).drop_duplicates('time').sort_values('time')
    return df.rename(columns={'tl': 't_obs', 'rr': 'p_obs'})


if __name__ == '__main__':
    d = fetch_station('5904', '2025-01-01', '2025-01-31')
    print(d.head())
    print(d.describe())