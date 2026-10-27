#Confirm the two documentation facts
import requests

URL = 'https://dataset.api.hub.geosphere.at/v1/station/historical/klima-v2-1h/metadata'
meta = requests.get(URL, timeout=60).json()
for key, value in meta.items():
    if key not in ('stations', 'parameters'):
        print(key, ':', value)
rr = [p for p in meta['parameters'] if p['name'] == 'rr'][0]
print(rr)