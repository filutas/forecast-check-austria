import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from src.observations import fetch_station
from src.forecasts import fetch_forecasts

LAT, LON = 48.24861, 16.35639
obs = fetch_station('5904', '2025-01-01', '2025-01-31')
fc = fetch_forecasts('5904', LAT, LON, 'ecmwf_ifs025', '2025-01-01', '2025-03-31')
fc1 = fc[fc['lead_days'] == 1]
d = obs.merge(fc1, on='time', how='inner')
w = d[(d['time'] >= pd.Timestamp('2025-01-10', tz='UTC')) & (d['time'] < pd.Timestamp('2025-01-17', tz='UTC'))]

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(w['time'], w['t_obs'], label='Observed (Hohe Warte)')
ax.plot(w['time'], w['t_fc'], label='Forecast lead 1 day (ECMWF IFS)')
ax.set_ylabel('2 m temperature (deg C)')
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig('outputs/figures/sanity_check_vienna.png', dpi=150)
print('saved outputs/figures/sanity_check_vienna.png')