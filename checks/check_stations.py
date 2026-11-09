from src.observations import fetch_month

candidates = [
    ('Wien Hohe Warte', ['105', '5904']),
    ('Graz Universitaet', ['30', '16414']),
    ('Linz Stadt', ['56', '3202']),
    ('Salzburg Flughafen', ['131', '6300']),
    ('Innsbruck Flughafen', ['175', '11804']),
    ('Klagenfurt Flughafen', ['48', '20212']),
    ('Sonnblick', ['213', '15411']),
]

for name, ids in candidates:
    for sid in ids:
        try:
            df = fetch_month(sid, '2025-07-01T00:00', '2025-07-31T23:00')
            print(f'{name:25s} id {sid:>6s}  rows {len(df):4d}  tl valid {df.tl.notna().sum():4d}  rr valid {df.rr.notna().sum():4d}')
        except Exception as err:
            print(f'{name:25s} id {sid:>6s}  FAILED: {err}')