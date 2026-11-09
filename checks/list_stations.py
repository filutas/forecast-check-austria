import requests
import pandas as pd

URL = 'https://dataset.api.hub.geosphere.at/v1/station/historical/klima-v2-1h/metadata'
meta = requests.get(URL, timeout=60).json()

# Make the tables readable in the terminal
pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 200)

# 1. Parameters: find air temperature and precipitation here
params = pd.DataFrame(meta['parameters'])
print('PARAMETER COLUMNS:', params.columns.tolist())
cols = [c for c in ['name', 'long_name', 'desc', 'unit'] if c in params.columns]
print(params[cols].to_string())

# 2. Stations
st = pd.DataFrame(meta['stations'])
print('\nSTATION COLUMNS:', st.columns.tolist())

wanted = ['Wien', 'Graz', 'Linz', 'Salzburg', 'Innsbruck', 'Klagenfurt', 'Sonnblick']
show = [c for c in ['id', 'name', 'state', 'altitude', 'lat', 'lon', 'valid_from', 'valid_to', 'is_active'] if c in st.columns]
for n in wanted:
    hits = st[st['name'].str.contains(n, case=False)]
    if 'is_active' in hits.columns:
        hits = hits[hits['is_active']]
    print('\n---', n, '---')
    print(hits[show].to_string(index=False))