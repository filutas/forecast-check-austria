import pandas as pd
from src.metrics import temp_metrics

df = pd.read_parquet('data/processed/merged.parquet')
m = temp_metrics(df)
m.to_csv('outputs/metrics_temperature.csv', index=False)
print(m.groupby(['model', 'lead_days'])[['bias', 'mae', 'rmse']].mean().round(2))
print()
print(m[m['lead_days'] == 1].pivot(index='station', columns='model', values='bias').round(2))