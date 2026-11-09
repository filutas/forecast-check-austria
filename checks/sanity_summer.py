import pandas as pd
from src.observations import fetch_station
from src.forecasts import fetch_forecasts

LAT, LON = 48.24861, 16.35639
obs = fetch_station('5904', '2025-07-01', '2025-07-31')
fc = fetch_forecasts('5904', LAT, LON, 'ecmwf_ifs025', '2025-07-01', '2025-09-30')
fc1 = fc[fc['lead_days'] == 1]

o = obs.set_index('time')['t_obs']
f = fc1.set_index('time')['t_fc']
print('Alignment test (mean absolute error by hour shift):')
for k in (-2, -1, 0, 1, 2):
    s = o.copy()
    s.index = s.index - pd.Timedelta(hours=k)
    x = pd.concat([s, f], axis=1, join='inner').dropna()
    print(k, len(x), round((x['t_fc'] - x['t_obs']).abs().mean(), 2))
