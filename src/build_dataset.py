from pathlib import Path

import pandas as pd
import yaml

from src.forecasts import fetch_forecasts
from src.observations import fetch_station


def main():
    with open('config/config.yml', encoding='utf-8') as f:
        cfg = yaml.safe_load(f)
    start, end = cfg['period']['start'], cfg['period']['end']
    frames = []
    for st in cfg['stations']:
        obs = fetch_station(st['id'], start, end)
        print(st['name'], '| observation rows:', len(obs),
              '| missing temperature:', int(obs['t_obs'].isna().sum()),
              '| missing precipitation:', int(obs['p_obs'].isna().sum()))
        for model in cfg['models']:
            fc = fetch_forecasts(st['id'], st['lat'], st['lon'], model, start, end)
            merged = fc.merge(obs, on='time', how='inner')
            merged['station'] = st['name']
            merged['station_id'] = st['id']
            merged['model'] = model
            merged['elevation'] = st['elevation']
            frames.append(merged)
            print('   ', model, '| merged rows:', len(merged),
                  '| missing t_fc:', int(merged['t_fc'].isna().sum()),
                  '| missing p_fc:', int(merged['p_fc'].isna().sum()))
    out = pd.concat(frames, ignore_index=True)
    Path('data/processed').mkdir(parents=True, exist_ok=True)
    out.to_parquet('data/processed/merged.parquet')
    print('saved', out.shape)


if __name__ == '__main__':
    main()