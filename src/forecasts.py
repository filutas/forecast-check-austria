import time
from pathlib import Path
import pandas as pd
import requests

URL = 'https://previous-runs-api.open-meteo.com/v1/forecast'
RAW = Path('data/raw')
LEADS = [1, 2, 3, 4, 5]


def quarter_ranges(start, end):
    for q in pd.period_range(start, end, freq='Q'):
        yield q.start_time.strftime('%Y-%m-%d'), q.end_time.strftime('%Y-%m-%d')


def fetch_chunk(sid, lat, lon, model, start, end):
    RAW.mkdir(parents=True, exist_ok=True)
    out = RAW / f'fc_{sid}_{model}_{start}.parquet'
    if out.exists():
        return pd.read_parquet(out)
    hourly = [f'{v}_previous_day{d}' for v in ('temperature_2m', 'precipitation') for d in LEADS]
    query = {'latitude': lat, 'longitude': lon, 'hourly': ','.join(hourly), 'models': model,
             'start_date': start, 'end_date': end, 'timezone': 'UTC'}
    response = None
    for attempt in range(3):
        try:
            response = requests.get(URL, params=query, timeout=90)
            response.raise_for_status()
            break
        except requests.RequestException as err:
            print('retry', attempt + 1, err)
            time.sleep(10 * (attempt + 1))
    if response is None or not response.ok:
        raise RuntimeError(f'Forecast download failed {sid} {model} {start}')
    df = pd.DataFrame(response.json()['hourly'])
    df.columns = [c.replace(f'_{model}', '') for c in df.columns]
    df['time'] = pd.to_datetime(df['time'], utc=True)
    parts = []
    for d in LEADS:
        t = df[['time', f'temperature_2m_previous_day{d}', f'precipitation_previous_day{d}']].copy()
        t.columns = ['time', 't_fc', 'p_fc']
        t['lead_days'] = d
        parts.append(t)
    res = pd.concat(parts)
    res.to_parquet(out)
    time.sleep(2)
    return res


def fetch_forecasts(sid, lat, lon, model, start, end):
    parts = [fetch_chunk(sid, lat, lon, model, s, e) for s, e in quarter_ranges(start, end)]
    return pd.concat(parts).drop_duplicates(['time', 'lead_days'])


if __name__ == '__main__':
    d = fetch_forecasts('5904', 48.2486, 16.3564, 'ecmwf_ifs025', '2025-01-01', '2025-03-31')
    print(d.head(10))
    print(d.groupby('lead_days').size())