"""
The observation file has one precipitation value per time stamp, for example 13:00 → 0.4 mm. 
That value could mean rain from 12:00 to 13:00 (stamp = end of the hour) or from 13:00 to 14:00 (stamp = start of the hour). 
Open-Meteos forecast at 13:00 means the sum over the preceding hour. 
If the two conventions differ, every forecast would be compared with the wrong hour, and the scores would be worse than they should be. 
Its an error nobody would notice without testing.
"""

import pandas as pd
from src.observations import fetch_station
from src.forecasts import fetch_forecasts

STATIONS = [
    ('5904', 'Wien', 48.24861, 16.35639),
    ('16414', 'Graz', 47.08, 15.448056),
    ('6300', 'Salzburg', 47.78944, 13.00861),
]
START, END = '2025-07-01', '2025-09-30'
MODEL = 'ecmwf_ifs025'
SHIFTS = [-2, -1, 0, 1, 2]

rows = []
for sid, name, lat, lon in STATIONS:
    obs = fetch_station(sid, START, END).set_index('time')['p_obs']
    fc = fetch_forecasts(sid, lat, lon, MODEL, START, END)
    fc = fc[fc['lead_days'] == 1].set_index('time')['p_fc']
    for k in SHIFTS:
        o = obs.copy()
        o.index = o.index - pd.Timedelta(hours=k)   # value at t+k is moved to t
        joined = pd.concat([o.rename('obs'), fc.rename('fc')], axis=1, join='inner').dropna()
        rows.append({'station': name, 'shift_hours': k, 'n': len(joined),
                     'corr': joined['obs'].corr(joined['fc'])})

res = pd.DataFrame(rows)
print(res.pivot(index='station', columns='shift_hours', values='corr').round(3))
print()
print('Mean over stations:')
print(res.groupby('shift_hours')['corr'].mean().round(3))