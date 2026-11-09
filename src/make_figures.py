from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

from src.metrics import daily_precip, precip_scores, temp_metrics

FIG = Path('outputs/figures')
FIG.mkdir(parents=True, exist_ok=True)
df = pd.read_parquet('data/processed/merged.parquet')

m = temp_metrics(df)
m.to_csv('outputs/metrics_temperature.csv', index=False)
sc = precip_scores(daily_precip(df))
sc.to_csv('outputs/metrics_precip.csv', index=False)

# Figure 1: temperature MAE versus lead time, one line per model
fig, ax = plt.subplots(figsize=(7, 4))
for model, g in m.groupby('model'):
    avg = g.groupby('lead_days')['mae'].mean()
    ax.plot(avg.index, avg.values, marker='o', label=model)
ax.set_xticks([1, 2, 3, 4, 5])
ax.set_xlabel('Lead time (days)')
ax.set_ylabel('Mean absolute error of 2 m temperature (deg C)')
ax.set_title('Forecast error grows with lead time')
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(FIG / 'fig1_mae_vs_lead.png', dpi=150)

# Figure 2: temperature bias at lead 1 for every station and model
b = m[m['lead_days'] == 1].pivot(index='station', columns='model', values='bias')
ax = b.plot.bar(figsize=(8, 4.5))
ax.axhline(0, color='black', linewidth=0.8)
ax.set_ylabel('Bias (forecast minus observation, deg C)')
ax.set_title('Temperature bias by station (lead 1 day)')
plt.tight_layout()
plt.savefig(FIG / 'fig2_bias_by_station.png', dpi=150)

# Figure 3: rain day detection (POD) and false alarms (FAR) versus lead
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
for model, g in sc.groupby('model'):
    avg = g.groupby('lead_days')[['pod', 'far']].mean()
    axes[0].plot(avg.index, avg['pod'], marker='o', label=model)
    axes[1].plot(avg.index, avg['far'], marker='o', label=model)
axes[0].set_title('Probability of detection (rain day >= 1 mm)')
axes[1].set_title('False alarm ratio')
for a in axes:
    a.set_xticks([1, 2, 3, 4, 5])
    a.set_xlabel('Lead time (days)')
    a.set_ylim(0, 1)
    a.grid(alpha=0.3)
axes[0].legend()
fig.tight_layout()
fig.savefig(FIG / 'fig3_precip_scores.png', dpi=150)

print('Stations in precipitation scores:', sorted(sc['station'].unique()))
print(sc.groupby(['model', 'lead_days'])[['pod', 'far']].mean().round(2))
print('figures saved')